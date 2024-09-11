# Author: Vodohleb04
import asyncio
import tensorflow as tf
import keras
import numpy as np
import backend.agents.recommendations_agent.recommendations_json_validation as json_validation
from typing import Dict, List, Tuple
from jsonschema import validate, ValidationError
from aiologger.loggers.json import JsonLogger
from backend.agents.recommendations_agent.pure_recommendations_agent import PureRecommendationsAgent
from backend.broker.abstract_agents_broker import AbstractAgentsBroker
from backend.broker.agents_tasks.crud_agent_tasks import crud_recommendations_by_coordinates_task
from backend.broker.agents_tasks.embeddings_crud_agent_tasks import get_landmarks_embeddings_task
from backend.broker.agents_tasks.trainer_tasks import partial_record, fill_up_partial_record, record


logger = JsonLogger.with_default_handlers(
    level="DEBUG",
    serializer_kwargs={'ensure_ascii': False},
)


class RecommendationsAgent(PureRecommendationsAgent):
    _single_recommendations_agent = None

    @classmethod
    def get_recommendations_agent(cls):
        """
        Method to take recommendations agent object. Returns None in case when recommendations agent is not exists.
        :return: None | PureRecommendationsAgent
        """
        return cls._single_recommendations_agent


    @classmethod
    def recommendations_agent_exists(cls) -> bool:
        """Method to check if recommendations agent object already exists"""
        if cls._single_recommendations_agent:
            return True
        else:
            return False


    def __init__(
        self,
        actor_model: keras.Model, critic_model: keras.Model, tf_dtype: tf.DType, np_dtype: np.dtype, noise_object = None,
        watch_state_discount_factor: float = 0.9, visit_state_discount_factor: float = 0.9,
        reward_function = None
    ):
        """

        ###
        1. actor_model: keras.Model
            - Actor network, counts action from the given state in terms of Markov decision process (check https://arxiv.org/pdf/1509.02971 for more details).
        2. critic_model: keras.Model
            - Critic network, counts Q-value from the given state and action (check https://arxiv.org/pdf/1509.02971 for more details).
        3. tf_dtype: tensorflow.DType
            - dtype from tensorflow that is used in models layers.
        4. np.dtype: numpy.dtype
            - dtype from numpy that is used in models layers.
        5. *noise_object [DEFAULT = None]
            - Adds noise to the proto-action (is needed to solve exploration/exploitation problem). None by default.
                noise_object must be callable type (supports __call__ method) noise_object must return numpy.ndarray 
                or the other object whose type has a registered tensorflow.Tensor conversion function. 
        6. *watch_state_discount_factor: float [DEFAULT = 0.9]
            - discount factor of watch state (check RecommendationsAgent.count_new_watch_state method)
        7. *visit_state_discount_factor: float [DEFAULT = 0.9]
            - discount factor of visit state (check RecommendationsAgent.count_new_visit_state method)
        8. *reward_function: [DEFAULT = None]
            - Callable object to count final reward using user_reward. 
                Requirements of function:   
                    -- reward_function(5) = 0;  
                    -- reward_function(x) < 0, if x < 5;    
                    -- reward function is strictly increasing function; 
                    -- reward function returns float;
            final_reward = reward_function(user_reward)
        """
        if not self.recommendations_agent_exists():
            self._actor_model = actor_model
            self._critic_model = critic_model
            self._noise_object = noise_object

            self._watch_state_discount_factor = watch_state_discount_factor
            self._visit_state_discount_factor = visit_state_discount_factor

            self._reward_function = reward_function

            if reward_function:
                self._min_reward = reward_function(0)
                self._max_reward = reward_function(5)
            else:
                self._min_reward = 0
                self._max_reward = 5

            self._tf_dtype = tf_dtype
            self._np_dtype = np_dtype
            
            self._single_recommendations_agent = self
        else:
            raise RuntimeError("Unexpected behaviour, this class can have only one instance")
      
        
    @property
    def actor_model(self) -> keras.Model:
        return self._actor_model
    

    @actor_model.setter
    async def actor_model(self, actor_model: keras.Model):
        self._actor_model.set_weights(actor_model.get_weights())


    @property
    def critic_model(self) -> keras.Model:
        return self._critic_model

    
    @critic_model.setter
    async def critic_model(self, critic_model: keras.Model):
        self._critic_model.set_weights(critic_model.get_weights())

    
    async def count_new_watch_state(
        self, new_watched_landmark: Dict, watch_state: np.ndarray
    ) -> np.ndarray:
        """
        Counts new watch state using old state. 
        s(n + 1) = s(n) * disc_fact + new_watched_landmark

        ###
        1. new_watched_landmark: Dict["name": str, "latitude": float, "longitude": float]
            - landmark, that causes changing of the state
        2. watch_state: numpy.ndarray
            - float ndarray, old state        
            returns: numpy.ndarray - new state
        """
        watch_state = watch_state.astype(dtype=self._np_dtype)
        new_landmark_embedding = await self._embeddings_for_landmarks(new_watched_landmark) # returns List[embedding]
        new_landmark_embedding = np.asarray(new_landmark_embedding[0], dtype=self._np_dtype)

        return watch_state * self._watch_state_discount_factor + new_landmark_embedding
        
    
    async def count_new_visit_state(
        self, new_visited_landmark: Dict, visit_state: np.ndarray
    ) -> np.ndarray:
        """
        Counts new visit state using old state. 
        s(n + 1) = s(n) * disc_fact + new_visited_landmark

        ###
        1. new_visited_landmark: Dict["name": str, "latitude": float, "longitude": float]
            - landmark, that causes changing of the state
        2. visit_state: numpy.ndarray
            - float ndarray, old state
        
            returns: numpy.ndarray - new state
        """
        visit_state = visit_state.astype(dtype=self._np_dtype)
        new_landmark_embedding = await self._embeddings_for_landmarks(new_visited_landmark) # returns List[embedding]
        new_landmark_embedding = np.asarray(new_landmark_embedding[0], dtype=self._np_dtype)

        return visit_state * self._visit_state_discount_factor + new_landmark_embedding
    
    
    async def concat_state(self, base_states: Tuple[np.ndarray], mask: Tuple[float] | None = None, return_tf_tensor=False):
        """
        Concatenate the given states in the given order.

        result = base_states[0] * mask[0] \\\/ base_states[1] * mask[1] \\\/ ... \\\/ base_states[n] * mask[n]
        ###
        1. base_states: Tuple[numpy.ndarray]
            - States to concatenate, presented in the numpy.ndarray
        2.* mask: Tuple[float] [DEFAULT] = None
            - Float factors in range [0, 1] to mask the states. 
        3.* return_tf_tensor: bool [DEFAULT = False]
            - Returns tensorflow.Tensor if True, numpy.ndarray otherwise
        """
        if mask:
            if len(base_states) != len(mask):
                raise ValueError(f"len of base_states and len of the mask must be equal, but they are: {len(base_states)}, {len(mask)}")
            else:
                base_states = list(base_states)
                for i in range(len(base_states)):
                    if mask[i] < 0 or mask[i] > 1:
                        raise ValueError("Mask factors must satisfy the expression 0 <= mask[i] <= 1")
                    base_states[i] = base_states[i] * mask[i]
        result = np.concatenate(base_states, axis=0, dtype=self._np_dtype)
        if return_tf_tensor:
            return tf.convert_to_tensor(result)
        else:
            return result

    @staticmethod
    def _outdated_remove_nones_from_kb_result(kb_pre_recommendations: List) -> List:
        """Changes list"""
        return [
            kb_pre_recommendations[i] for i in range(len(kb_pre_recommendations))
            if kb_pre_recommendations[i]["recommendation"]
        ]


    @staticmethod
    def _remove_nones_from_kb_result(kb_pre_recommendations: List) -> None:
        """Changes list"""
        i = 0
        len_bound = len(kb_pre_recommendations)
        while i < len_bound:
            if kb_pre_recommendations[i]["recommendation"] is None:
                kb_pre_recommendations.pop(i)
                len_bound -= 1
                continue
            i += 1


    @staticmethod
    def _landmarks_are_equal(left_landmark: Dict, right_landmark: Dict) -> bool:
        if left_landmark["name"] != right_landmark["name"]:
            return False
        if left_landmark["latitude"] != right_landmark["latitude"]:
            return False
        if left_landmark["longitude"] != right_landmark["longitude"]:
            return False
        return True


    @staticmethod
    def _remove_duplicates_from_kb_result(kb_pre_recommendations: List):
        """Changes list"""
        i = 0
        len_bound = len(kb_pre_recommendations)
        while i < len_bound:
            j = 0
            while j < len_bound:
                if i == j:
                    j += 1
                    continue
                if RecommendationsAgent._landmarks_are_equal(
                        kb_pre_recommendations[i]["recommendation"], kb_pre_recommendations[j]["recommendation"]
                ):
                    len_bound -= 1
                    kb_pre_recommendations.pop(j)
                    continue
                j += 1
            i += 1


    @staticmethod
    def _find_recommendations_validation(json_params):
        """This method checks values only of special params. Other values will be checked in target agent."""
        validate(json_params, json_validation.find_recommendations_for_coordinates)
        if json_params["maximum_amount_of_recommendations"] and json_params["maximum_amount_of_recommendations"] <= 0:
            raise ValidationError("maximum_amount_of_recommendations can\'t be less or equal to zero")


    @staticmethod
    def _post_result_of_recommendations_validation(json_params):
        """This method checks values only of special params. Other values will be checked in target agent."""
        validate(json_params, json_validation.post_result_of_recommendations)
        if json_params["user_reward"] and (
            json_params["user_reward"] < 0 or json_params["user_reward"] > 5
        ):
            raise ValidationError("user_reward must be value in range [0, 5]")


    @staticmethod
    async def _kb_pre_recommendation_by_coordinates(json_params: Dict):
        recommendations_async_task = asyncio.create_task(
            AbstractAgentsBroker.call_agent_task(crud_recommendations_by_coordinates_task, json_params)
        )
        kb_pre_recommendation_asyncio_result = await recommendations_async_task
        logger.debug(
            f"Recommendations agent, find_recommendations_for_coordinates, "
            f"kb_pre_recommendation_asyncio_result: {kb_pre_recommendation_asyncio_result}"
        )
        kb_pre_recommendations = kb_pre_recommendation_asyncio_result.return_value
        return kb_pre_recommendations


    @staticmethod
    def _k_nearest_actions(
        proto_action: tf.Tensor,
        real_actions: tf.Tensor,
        k: int
    ):
        """
            Finds k actions nearest to the proto-action from the given real_actions_tensor. L2 distance is used to define distance.

            ###
            1. proto_action: tensorflow.Tensor
                - Proto-action counted by actor_model.
            2. real_actions: tensorflow.Tensor
                - The actions in Markov decision process. Tensor of the real actions, returned from the database.
                    In recommendation system - objects, that can be recommended to the given user.
            3. k: int
                - The amount of the real actions that will be returned.
        """
        if k < 1:
            raise AttributeError("k must be int value grater then zero.")
        l2_distance = tf.sqrt(
            tf.reduce_sum(
                tf.square(real_actions, proto_action),
                axis=1
            )
        )
        
        # Finds k nearest actions
        min_distance_list = []
        for i in range(l2_distance.shape[0]):
            if len(min_distance_list) < k:
                min_distance_list.append((l2_distance[i], i))  # pair of distance and index in the real_actions
            else:
                max_from_min = max(min_distance_list, key=lambda x: x[0])  # finds maximal distance in the list of minimal distances

                if l2_distance[i] < max_from_min[0]:  # max_from_min is pair (distance, index)
                    max_from_min_index = min_distance_list.index(max_from_min)
                    min_distance_list[max_from_min_index] = (l2_distance[i], i)

        return [dist_index[1] for dist_index in min_distance_list]


    def _max_critic_values_indexes(self, critic_values, recommendations_amount: int):
        # Finds indexes of recommendations with the highest Critic value
        max_critic_values_list = []
        for i in range(critic_values.shape[0]):
            if len(max_critic_values_list) < recommendations_amount:
                max_critic_values_list.append((critic_values[i][0], i))  #  pair of critic value and index in the real_actions
            else:
                # finds minimal critic value in the list of maximal critic values
                min_from_max = min(max_critic_values_list, key=lambda x: x[0])
                
                if critic_values[i][0] > min_from_max[0]:  # critic_values shape is [n, 1]
                    min_from_max_index = max_critic_values_list.index(min_from_max)
                    max_critic_values_list[min_from_max_index] = (critic_values[i][0], i)
        return [value_index[1] for value_index in max_critic_values_list]


    def _wolpertinger_policy(
        self,
        state: tf.Tensor,
        real_actions: tf.Tensor,
        recommendations: List[Dict],
        recommendations_amount: int
    ):
        """
            Wolpertinger policy. Check https://arxiv.org/pdf/1512.07679 for more details.
            ### Parameters
            1. state: tensorflow.Tensor
                - The state in Markov decision process. In recommendation system - the current state of the given user.
            2. real_actions: tensorflow.Tensor
                - The actions in Markov decision process. Tensor of the real actions, returned from the database.
                    In recommendation system - objects, that can be recommended to the given user.
            3. recommendations_amount: int
                - The amount of the real actions that will be returned.

            returns: Tuple[tensorflow.Tensor, List[Dict]] - tensor of actions and corresponding recommendations
        """
        proto_action = self._actor_model(state)  # state shape is [1, state_dim]
        if self._noise_object:
            proto_action += tf.convert_to_tensor(self._noise_object())
            proto_action = tf.clip_by_value(proto_action, clip_value_min=-1., clip_value_max=1.)
        
        proto_action = tf.squeeze(proto_action, [0])  # actor_model returns shape (1, action_dim), but shape (action_dim) is needed

        real_actions_indexes = self._k_nearest_actions(proto_action, real_actions, k=recommendations_amount * 2)  # TODO check if 200% is good k
        recommendations = [recommendations[index] for index in real_actions_indexes]
        real_actions = tf.gather(real_actions, real_actions_indexes)

        # state_for_actions shape is [n, state_dim]. The same state is copied for multiple actions
        state_for_actions = tf.tile(state, [real_actions.shape[0], 1])

        critic_values = self._critic_model(state_for_actions, real_actions)  # critic_values shape is [n, 1]

        max_critic_values_indexes = self._max_critic_values_indexes(critic_values, recommendations_amount)
        recommendations = [recommendations[index] for index in max_critic_values_indexes]
        real_actions = tf.gather(real_actions, max_critic_values_indexes)
                
        return real_actions, recommendations

    async def _embeddings_for_landmarks(self, landmarks):
        json_params = {"landmarks": landmarks}
        embeddings_async_task = asyncio.create_task(
            AbstractAgentsBroker.call_agent_task(get_landmarks_embeddings_task, json_params)
        )
        embeddings_asyncio_result = await embeddings_async_task
        logger.debug(
            f"Recommendations agent, _embeddings_for_landmarks, "
            f"embeddings_for_landmarks: {embeddings_asyncio_result}"
        )

        return embeddings_asyncio_result.return_value


    async def _find_recommendations_by_coordinates(
        self, state: np.ndarray, recommendations, maximum_amount_of_recommendations
    ):
        # state shape is [state_dim]

        real_actions = await self._embeddings_for_landmarks(recommendations)
        real_actions = tf.convert_to_tensor(real_actions, dtype=self._tf_dtype)

        real_actions, recommendations = self._wolpertinger_policy(
            tf.expand_dims(
                tf.convert_to_tensor(state, dtype=self._tf_dtype), axis=0
            ),
            real_actions, recommendations, maximum_amount_of_recommendations
        )  # expands state shape to [1, state_dim]

        for i in range(len(recommendations)):
            partial_record_async_task = asyncio.create_task(
                AbstractAgentsBroker.call_agent_task(
                    partial_record,
                    {"state": state, "action": real_actions[i].numpy()}
                )
            )  # TODO partial record for list of landmarks
            partial_record_async_result = await partial_record_async_task
            index, uuid = partial_record_async_result.return_value
            recommendations[i]["buffer_index"] = index
            recommendations[i]["buffer_uuid"] = uuid
 
        return recommendations  # TODO get environment result and learning process


    async def find_recommendations_by_coordinates(self, json_params: Dict):
        try:
            self._find_recommendations_validation(json_params)
        except ValidationError as ex:
            await logger.error(f"find_recommendations_by_coordinates, ValidationError({ex.args[0]})")
            return []  # raise ValidationError
        
        maximum_amount_of_recommendations = json_params.pop("maximum_amount_of_recommendations")
        
        json_params["limit"] = maximum_amount_of_recommendations * 4  # TODO if 400% is enough
        
        state = await self.concat_state(
            (json_params.pop("watch_state"), json_params.pop("visit_state")), return_tf_tensor=False
        )            


        kb_pre_recommendations = await self._kb_pre_recommendation_by_coordinates(json_params)

        self._remove_nones_from_kb_result(kb_pre_recommendations)
        logger.debug(
            f"Recommendations agent, find_recommendations_by_coordinates, kb_pre_recommendations after None removed: {kb_pre_recommendations}"  
        )
        if not kb_pre_recommendations:
            return kb_pre_recommendations
        self._remove_duplicates_from_kb_result(kb_pre_recommendations)
        logger.debug(
            f"Recommendations agent, find_recommendations_by_coordinates, kb_pre_recommendations after duplicates removed: {kb_pre_recommendations}"
        )
        return await self._find_recommendations_by_coordinates(
            state, kb_pre_recommendations, maximum_amount_of_recommendations
        )


    def _count_final_reward(self, user_reward: float):
        if self._reward_function:
            return self._reward_function(user_reward)
        else:
            return user_reward
        

    def _give_reward_to_recommendations(
        self, primary_recommendations, result_recommendations, user_reward
    ):
        """
        Remove from result_recommendations landmarks that included in primary_recommendations 
        (primary_recommendations and result_recommendations will be modified) 
        """
        for primary_recommendation in primary_recommendations:
            for index_in_result in range(len(result_recommendations)):
                if self._landmarks_are_equal(primary_recommendation, result_recommendations[index_in_result]):
                    primary_recommendation["reward"] = user_reward
                    result_recommendations.pop(index_in_result)
                    break
                else:
                    primary_recommendation["reward"] = self._min_reward  # Min reward for landmarks, removed from route by user
        return primary_recommendations, result_recommendations
    

    async def _post_primary_recs_to_sars_buffer(self, primary_recommendations, next_state):
        """
        returns: Tuple[state, completed_records_amount]   
            state: numpy.ndarray | None (array, if at least one partial record was filled up, state(n) of this record)
            completed_records_amount: int (amount of partial record, that had been filled up)
        """
        completed_records_amount = 0
        state = None
        for primary_recommendation in primary_recommendations:
            fill_up_partial_record_async_task = asyncio.create_task(
                AbstractAgentsBroker.call_agent_task(
                    fill_up_partial_record,
                    {
                        "buffer_index": primary_recommendation["buffer_index"],
                        "buffer_uuid": primary_recommendation["buffer_uuid"],
                        "reward": self._np_dtype(primary_recommendation["reward"]),
                        "next_state": next_state
                    }
                )  # TODO fill_up for list of landmarks
            )
            fill_up_partial_record_async_result = await fill_up_partial_record_async_task
            uuid_correct = fill_up_partial_record_async_result.return_value
            if uuid_correct and not state:
                pass
                # TODO state = task to get state from this row(add methods to trainer and sars buffer)
            completed_records_amount += uuid_correct
        return state, completed_records_amount


    async def _post_result_recs_to_sars_buffer(self, result_recommendations, state: None | np.ndarray, next_state: np.ndarray):
        if state:
            pass
            # TODO get embeddings of result_recommendations
            # TODO add records (state, embedding of result recommendation, max_reward, next_state)
            # TODO record for list of landmarks (add method to trainer)

    @staticmethod
    async def _start_training(amount_of_repeats):
        pass
        # TODO start training

    async def post_result_of_recommendations(
            self, json_params
    ):
        try:
            self._post_result_of_recommendations_validation(json_params)
        except ValidationError as ex:
            await logger.error(f"post_result_of_recommendations, ValidationError({ex.args[0]})")
            return  # raise ValidationError
        user_reward = self._count_final_reward(json_params.pop("user_reward"))

        primary_recommendations, result_recommendations = self._give_reward_to_recommendations(
            json_params.pop("primary_recommendations"), json_params.pop("result_recommendations"), user_reward
        )

        next_state = await self.concat_state(
            (json_params.pop("new_watch_state"), json_params.pop("new_visit_state")), return_tf_tensor=False
        )
        
        state, filled_up_amount = await self._post_primary_recs_to_sars_buffer(primary_recommendations, next_state)
        await self._post_result_recs_to_sars_buffer(result_recommendations, state, next_state)

        await self._start_training(len(primary_recommendations) + len(result_recommendations))





 
# TODO state пользователя в качестве входного параметра при подсчёте достопримечательностей (либо получать с помощью запроса)
# TODO вовзрат в агента того, что он отправил + то, что оставил пользователь + оценка пользователя
# TODO после получения оценки пересчёт нового сотояния + дополнение частичной записи в буфере
# TODO если в буфере есть хотя бы одна полная запись, то выполняется запуск обучения
