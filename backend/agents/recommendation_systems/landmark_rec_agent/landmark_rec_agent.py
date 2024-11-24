# Author: Vodohleb04
import asyncio
import tensorflow as tf
import keras
import numpy as np
from typing import Dict, List, Tuple
from jsonschema import validate, ValidationError
from aiologger.loggers.json import JsonLogger
import backend.agents.recommendation_systems.landmark_rec_agent.landmark_rec_json_validation as json_validation
from backend.agents.recommendation_systems.landmark_rec_agent.pure_landmark_rec_agent import PureLandmarkRecAgent
from backend.broker.abstract_agents_broker import AbstractAgentsBroker
from backend.broker.agents_tasks.crud_agent_tasks import crud_recommendations_by_coordinates_task
from backend.broker.agents_tasks.landmark_embeddings_crud_agent_tasks import get_landmarks_embeddings_task
from backend.broker.agents_tasks.landmark_trainer_tasks import (
    partial_record_list_with_next_state,
    fill_up_partial_record_reward_only_list,
    fill_up_partial_record_reward_only_replace_next_state_list,
    record_list,
    train, get_state,
    get_actor_model, get_critic_model, get_actor_model_config, get_critic_model_config
)


logger = JsonLogger.with_default_handlers(
    level="DEBUG",
    serializer_kwargs={'ensure_ascii': False},
)


class LandmarkRecAgent(PureLandmarkRecAgent):
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


    def _default_models_init(self):
        self._actor_critic_are_inited = False
        self._requires_training = True
        self._actor_model: keras.Model | None = None
        self._critic_model: keras.Model | None = None


    def _init_models_from_files(self, actor_weights_file, critic_weights_file):
        if actor_weights_file is None or critic_weights_file is None:
            raise ValueError("Both of models( actor and critic) must be inited from files or inited with none (in"
                             " the second case they will be inited by models used by trainer agent)")
        if not (isinstance(actor_weights_file, str) and actor_weights_file.endswith(".keras")):
            raise ValueError(f"Expected actor_weights_file to be name of file with .keras extension, "
                             f"but got {actor_weights_file} instead")
        if not (isinstance(critic_weights_file, str) and critic_weights_file.endswith(".keras")):
            raise ValueError(f"Expected critic_weights_file to be name of file with .keras extension, "
                             f"but got {critic_weights_file} instead")

        self._actor_model = keras.models.load_model(actor_weights_file)
        self._critic_model = keras.models.load_model(critic_weights_file)
        self._actor_critic_are_inited = True
        self._requires_training = False


    def __init__(
        self,
        tf_dtype: tf.DType, np_dtype: np.dtype, noise_object = None,
        watch_state_discount_factor: float = 0.9, visit_state_discount_factor: float = 0.9,
        actor_weights_file=None, critic_weights_file=None
    ):
        """

        ###
        1. tf_dtype: tensorflow.DType
            - dtype from tensorflow that is used in models layers.
        2. np.dtype: numpy.dtype
            - dtype from numpy that is used in models layers.
        3. *noise_object [DEFAULT = None]
            - Adds noise to the proto-action (is needed to solve exploration/exploitation problem). None by default.
                noise_object must be callable type (supports __call__ method) noise_object must return numpy.ndarray 
                or the other object whose type has a registered tensorflow.Tensor conversion function. 
        4. *watch_state_discount_factor: float [DEFAULT = 0.9]
            - discount factor of watch state (check RecommendationsAgent.count_new_watch_state method)
        5. *visit_state_discount_factor: float [DEFAULT = 0.9]
            - discount factor of visit state (check RecommendationsAgent.count_new_visit_state method)
        """
        if not self.recommendations_agent_exists():
            self._asyncio_tasks = set()

            if actor_weights_file is None and critic_weights_file is None:
                self._default_models_init()
            else:
                self._init_models_from_files(actor_weights_file, critic_weights_file)

            self._noise_object = noise_object

            self._watch_state_discount_factor = watch_state_discount_factor
            self._visit_state_discount_factor = visit_state_discount_factor

            self._min_reward = self.reward_function(0)
            self._max_reward = self.reward_function(5)

            self._tf_dtype = tf_dtype
            self._np_dtype = np_dtype
            
            self._single_recommendations_agent = self
        else:
            raise RuntimeError("Unexpected behaviour, this class can have only one instance")


    @staticmethod
    def reward_function(user_reward):
        """
            Counts immediate reward in Markov decision process. Takes user reward of the route.

            :param user_reward: float in range[0, 5] - reward, leaved by user.

            :returns: float
        """
        return 20 * (user_reward - 5)


    @property
    async def actor_model(self) -> keras.Model | None:
        return self._actor_model
    

    @actor_model.setter
    async def actor_model(self, actor_model: keras.Model):
        self._actor_model.set_weights(actor_model.get_weights())


    @property
    async def critic_model(self) -> keras.Model | None:
        return self._critic_model

    
    @critic_model.setter
    async def critic_model(self, critic_model: keras.Model):
        self._critic_model.set_weights(critic_model.get_weights())


    @staticmethod
    def _update_model(model, py_weigths, dtype):
        model.set_weights(
            [
                np.asarray(py_weigths[i], dtype=dtype)
                for i in range(len(py_weigths))
            ]
        )

    
    async def count_new_watch_state(self, json_params) -> List[float]:
        try:
            validate(json_params, json_validation.count_new_watch_state)
        except ValidationError as ex:
            await logger.error(f"count_new_watch_state, ValidationError({ex.args[0]})")
            return []  # raise ValidationError

        watch_state = np.asarray(json_params["watch_state"], dtype=self._np_dtype)
        new_landmarks_embeddings = await self._embeddings_for_landmarks(json_params["new_watched_landmarks"]) # returns List[embedding]
        new_landmarks_embeddings = np.asarray(new_landmarks_embeddings, dtype=self._np_dtype)

        for i in range(new_landmarks_embeddings.shape[0]):
            watch_state = watch_state * self._watch_state_discount_factor + new_landmarks_embeddings[i]

        return watch_state.tolist()
        
    
    async def count_new_visit_state(self, json_params: Dict) -> List[float]:
        try:
            validate(json_params, json_validation.count_new_visit_state)
        except ValidationError as ex:
            await logger.error(f"count_new_visit_state, ValidationError({ex.args[0]})")
            return []  # raise ValidationError

        visit_state = np.asarray(json_params["visit_state"], dtype=self._np_dtype)
        new_landmarks_embeddings = await self._embeddings_for_landmarks(json_params["new_visited_landmark"]) # returns List[embedding]
        new_landmarks_embeddings = np.asarray(new_landmarks_embeddings, dtype=self._np_dtype)

        for i in range(new_landmarks_embeddings.shape[0]):
            visit_state = visit_state * self._visit_state_discount_factor + new_landmarks_embeddings[i]

        return visit_state.tolist()
    
    
    def _concat_state(self, base_states: Tuple[np.ndarray], mask: Tuple[float] | None = None, return_tf_tensor=False):
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
    def _split_state(state: np.ndarray):
        """
        Split state on watch_state and visit_state.

        :return: Tuple[np.ndarray, np.ndarray] - watch_state, visit_state
        """
        return state[:int(state.shape[0] / 2)], state[:int(state.shape[0] / 2)]


    @staticmethod
    def _remove_nones_from_kb_result(kb_pre_recommendations: List) -> List:
        """Returns changed list, that doesn't include None values"""
        return [
            kb_pre_recommendations[i] for i in range(len(kb_pre_recommendations))
            if kb_pre_recommendations[i]["recommendation"]
        ]


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
    def _remove_duplicates_from_kb_result(kb_pre_recommendations: List) -> List:
        """Changes list"""
        result = []
        for i in range(len(kb_pre_recommendations)):
            for j in range(len(result)):
                if LandmarkRecAgent._landmarks_are_equal(
                    kb_pre_recommendations[i]["recommendation"], result[j]["recommendation"]
                ):
                    break
            else:
                result.append(kb_pre_recommendations[i])
        return result


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


    async def _kb_pre_recommendation_by_coordinates(self, json_params: Dict):
        recommendations_async_task = asyncio.create_task(
            AbstractAgentsBroker.call_agent_task(crud_recommendations_by_coordinates_task, json_params)
        )
        self._asyncio_tasks.add(recommendations_async_task)
        recommendations_async_task.add_done_callback(self._asyncio_tasks.discard)

        kb_pre_recommendation_asyncio_result = await recommendations_async_task
        logger.debug(
            f"Recommendations agent, find_recommendations_for_coordinates, "
            f"kb_pre_recommendation_asyncio_result: {kb_pre_recommendation_asyncio_result}"
        )
        kb_pre_recommendations = kb_pre_recommendation_asyncio_result.return_value

        kb_pre_recommendations = self._remove_nones_from_kb_result(kb_pre_recommendations)
        logger.debug(
            f"Recommendations agent, find_recommendations_by_coordinates, kb_pre_recommendations after None removed: {kb_pre_recommendations}"  
        )
        return kb_pre_recommendations


    @staticmethod
    def _cosine_distance(proto_action: tf.Tensor, real_actions: tf.Tensor):
        """
        Scos = (proto_action * real_actions[i]) / ( ||proto_action|| * ||real_actions[i]|| )

        returns: 1 - Scos(proto_actions, real_actions)
        """
        proto_action_length = tf.sqrt(
            tf.reduce_sum(tf.square(proto_action))
        )  # L2 norm of proto-action

        return 1 - tf.divide(
            tf.reduce_sum(tf.multiply(proto_action, real_actions), axis=1),  # scalar multiplication
            tf.multiply(
                proto_action_length,
                tf.sqrt(tf.reduce_sum(tf.square(real_actions), axis=1))  # L2 norms of real_actions
            )  # || proto_action || * || real_actions[i] ||
        )


    @staticmethod
    def _k_nearest_actions(proto_action: tf.Tensor, real_actions: tf.Tensor, k: int):
        """
            Finds k actions nearest to the proto-action from the given real_actions_tensor. Cosine distance is used to define distance.

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
        distances = LandmarkRecAgent._cosine_distance(proto_action, real_actions)

        # Finds k nearest actions
        min_distance_list = []

        for i in range(distances.shape[0]):
            if i < k:
                min_distance_list.append((distances[i], i))  # pair of distance and index in the real_actions
            else:
                max_from_min = max(min_distance_list, key=lambda x: x[0])  # finds maximal distance in the list of minimal distances

                if distances[i] < max_from_min[0]:  # max_from_min is pair (distance, index)
                    max_from_min_index = min_distance_list.index(max_from_min)
                    min_distance_list[max_from_min_index] = (distances[i], i)

        return [dist_index[1] for dist_index in min_distance_list]


    @staticmethod
    def _max_critic_values_indexes(critic_values, recommendations_amount: int):
        # Finds indexes of recommendations with the highest Critic value
        max_critic_values_list = []

        for i in range(critic_values.shape[0]):
            if i < recommendations_amount:
                max_critic_values_list.append((critic_values[i][0], i))  #  pair of critic value and index in the real_actions
            else:
                # finds minimal critic value in the list of maximal critic values
                min_from_max = min(max_critic_values_list, key=lambda x: x[0])
                
                if critic_values[i][0] > min_from_max[0]:  # critic_values shape is [n, 1]
                    min_from_max_index = max_critic_values_list.index(min_from_max)
                    max_critic_values_list[min_from_max_index] = (critic_values[i][0], i)
        return [value_index[1] for value_index in max_critic_values_list]


    def _wolpertinger_policy(
        self, state: tf.Tensor, real_actions: tf.Tensor, recommendations: List[Dict], recommendations_amount: int
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
        
        proto_action = tf.squeeze(proto_action, [0])  # actor_model returns shape (1, action_dim), but shape (action_dim) is needed

        real_actions_indexes = self._k_nearest_actions(proto_action, real_actions, k=recommendations_amount * 2)  # TODO check if 200% is good k
        recommendations = [recommendations[index] for index in real_actions_indexes]
        real_actions = tf.gather(real_actions, real_actions_indexes)

        # state_for_actions shape is [n, state_dim]. The same state is copied for multiple actions
        state_for_actions = tf.tile(state, [real_actions.shape[0], 1])

        critic_values = self._critic_model([state_for_actions, real_actions])  # critic_values shape is [n, 1]

        max_critic_value_index_list = self._max_critic_values_indexes(critic_values, recommendations_amount)
        recommendations = [recommendations[index] for index in max_critic_value_index_list]
        real_actions = tf.gather(real_actions, max_critic_value_index_list)
                
        return real_actions, recommendations


    async def _embeddings_for_landmarks(self, landmarks):
        json_params = {"landmarks": landmarks}
        embeddings_async_task = asyncio.create_task(
            AbstractAgentsBroker.call_agent_task(get_landmarks_embeddings_task, json_params)
        )
        self._asyncio_tasks.add(embeddings_async_task)
        embeddings_async_task.add_done_callback(self._asyncio_tasks.discard)

        embeddings_asyncio_result = await embeddings_async_task
        logger.debug(
            f"Recommendations agent, _embeddings_for_landmarks, "
            f"embeddings_for_landmarks: {embeddings_asyncio_result}"
        )

        return embeddings_asyncio_result.return_value


    def _count_next_states_for_actions(self, watch_state, visit_state, actions, count_using_tensorflow=True):
        if count_using_tensorflow:
            watch_state_to_concat = tf.tile(
                tf.expand_dims(watch_state, axis=0),
                [actions.shape[0], 1]
            )
            next_visit_state = actions + self._visit_state_discount_factor * visit_state
            return tf.concat((watch_state_to_concat, next_visit_state), axis=1)
        else:
            watch_state_to_concat = np.tile(
                np.expand_dims(watch_state, axis=0),
                [actions.shape[0], 1]
            )
            next_visit_state = actions + self._visit_state_discount_factor * visit_state
            return np.concatenate((watch_state_to_concat, next_visit_state), axis=1)


    @staticmethod
    async def _partial_record_list_with_next_state_task(state, actions, next_states):
        partial_record_list_async_task = asyncio.create_task(
            AbstractAgentsBroker.call_agent_task(
                partial_record_list_with_next_state,
                json_params={
                    "state": state.tolist(),
                    "action_list": [actions[i].numpy().tolist() for i in range(actions.shape[0])],
                    "next_state_list": [next_states[i].numpy().tolist() for i in range(next_states.shape[0])]
                }
            )
        )

        return (await partial_record_list_async_task).return_value


    async def _find_recommendations_by_coordinates(
        self, watch_state: np.ndarray, visit_state: np.ndarray, recommendations, maximum_amount_of_recommendations
    ):
        state = self._concat_state((watch_state, visit_state), return_tf_tensor=False)  # state shape is [state_dim]

        real_actions = await self._embeddings_for_landmarks(recommendations)
        real_actions = tf.convert_to_tensor(real_actions, dtype=self._tf_dtype)

        real_actions, recommendations = self._wolpertinger_policy(
            tf.expand_dims(
                tf.convert_to_tensor(state, dtype=self._tf_dtype), axis=0
            ),  # expands state shape to [1, state_dim]
            real_actions, recommendations, maximum_amount_of_recommendations
        )

        if self._requires_training:
            next_states = self._count_next_states_for_actions(watch_state, visit_state, real_actions)
            index_list, uuid_list = await self._partial_record_list_with_next_state_task(state, real_actions, next_states)

            for i in range(len(index_list)):
                recommendations[i]["row_index"] = index_list[i]
                recommendations[i]["row_uuid"] = uuid_list[i]
        else:
            logger.info("RecSys agent doesn't requires training. No SARS buffer record is required.")
 
        return recommendations


    async def _init_actor(self):
        actor_model_config_async_task = asyncio.create_task(
            AbstractAgentsBroker.call_agent_task(get_actor_model_config, {})
        )
        actor_model_weights_async_task = asyncio.create_task(
            AbstractAgentsBroker.call_agent_task(get_actor_model, {})
        )
        actor_model_config_async_result = await actor_model_config_async_task
        actor_model_weights_async_result = await actor_model_weights_async_task

        self._actor_model = keras.models.model_from_json(
            actor_model_config_async_result.return_value["actor_model_config"]
        )
        self._update_model(
            self._actor_model, actor_model_weights_async_result.return_value["actor_model"], self._np_dtype
        )

    
    async def _init_critic(self):
        critic_model_config_async_task = asyncio.create_task(
            AbstractAgentsBroker.call_agent_task(get_critic_model_config, {})
        )
        critic_model_weights_async_task = asyncio.create_task(
            AbstractAgentsBroker.call_agent_task(get_critic_model, {})
        )
        critic_model_config_async_result = await critic_model_config_async_task
        critic_model_weights_async_result = await critic_model_weights_async_task
        
        self._critic_model = keras.models.model_from_json(
            critic_model_config_async_result.return_value["critic_model_config"]
        )
        self._update_model(
            self._critic_model, critic_model_weights_async_result.return_value["critic_model"], self._np_dtype
        )

    
    async def _init_actor_critic_models(self):
        await self._init_actor()
        await self._init_critic()
        self._actor_critic_are_inited = True


    async def find_recommendations_by_coordinates(self, json_params: Dict):
        try:
            self._find_recommendations_validation(json_params)
        except ValidationError as ex:
            await logger.error(f"find_recommendations_by_coordinates, ValidationError({ex.args[0]})")
            return []  # raise ValidationError
        
        maximum_amount_of_recommendations = json_params["maximum_amount_of_recommendations"]
        json_params["limit"] = maximum_amount_of_recommendations * 4  # TODO if 400% is enough

        watch_state = np.asarray(json_params["watch_state"], dtype=self._np_dtype)
        visit_state = np.asarray(json_params["visit_state"], dtype=self._np_dtype)

        kb_pre_recommendations = await self._kb_pre_recommendation_by_coordinates(json_params)
        if not kb_pre_recommendations:
            return kb_pre_recommendations
        
        kb_pre_recommendations = self._remove_duplicates_from_kb_result(kb_pre_recommendations)
        logger.debug(
            f"Recommendations agent, find_recommendations_by_coordinates, kb_pre_recommendations after duplicates removed: {kb_pre_recommendations}"
        )

        if not self._actor_critic_are_inited:
            await self._init_actor_critic_models()
            
        return await self._find_recommendations_by_coordinates(
            watch_state, visit_state, kb_pre_recommendations, maximum_amount_of_recommendations
        )


    def _give_reward_to_recommendations(
        self, primary_recommendations, result_recommendations, user_reward
    ):
        """
        Remove from result_recommendations landmarks that included in primary_recommendations
        (primary_recommendations and result_recommendations will be modified). Reward for result_recommendations,
        that were included by user wil be given in _post_result_recs_to_sars_buffer method.
        """
        reward = self.reward_function(user_reward)

        for primary_recommendation in primary_recommendations:
            for index_in_result in range(len(result_recommendations)):
                if self._landmarks_are_equal(primary_recommendation, result_recommendations[index_in_result]):
                    primary_recommendation["reward"] = reward
                    primary_recommendation["change_next_state"] = False
                    result_recommendations.pop(index_in_result)
                    break
            else:
                primary_recommendation["reward"] = self._min_reward  # Min reward for landmarks, removed from route by user
                primary_recommendation["change_next_state"] = True
        return primary_recommendations, result_recommendations
    

    @staticmethod
    async def _fill_up_partial_record_reward_only_list_task(row_index_list, row_uuid_list, reward_list):
        fill_up_partial_record_reward_only_list_task = asyncio.create_task(
            AbstractAgentsBroker.call_agent_task(
                fill_up_partial_record_reward_only_list,
                json_params={
                    "row_index_list": row_index_list, "row_uuid_list": row_uuid_list, "reward_list": reward_list
                }
            )
        )
        return (await fill_up_partial_record_reward_only_list_task).return_value


    @staticmethod
    async def _fill_up_partial_record_reward_only_replace_next_state_list_task(row_index_list, row_uuid_list, reward_list):
        fill_up_partial_record_reward_only_replace_next_state_list_task = asyncio.create_task(
            AbstractAgentsBroker.call_agent_task(
                fill_up_partial_record_reward_only_replace_next_state_list,
                json_params={
                    "row_index_list": row_index_list, "row_uuid_list": row_uuid_list, "reward_list": reward_list
                }
            )
        )
        return (await fill_up_partial_record_reward_only_replace_next_state_list_task).return_value


    @staticmethod
    async def _get_state_task(row_index, row_uuid):
        get_state_async_task = asyncio.create_task(
            AbstractAgentsBroker.call_agent_task(
                get_state, {"row_index": row_index, "row_uuid": row_uuid}
            )
        )
        return (await get_state_async_task).return_value
    

    @staticmethod
    async def _record_list_task(sars_tuple_list):
        record_list_async_task = asyncio.create_task(
            AbstractAgentsBroker.call_agent_task(
                record_list, {"sars_tuple_list": sars_tuple_list}
            )
        )
        return (await record_list_async_task).return_value


    async def _define_state_using_primary_uuids(
        self, primary_recommendations, uuid_correct_list, uuid_correct_list_with_state_replace
    ):
        state = None
        for i in range(len(uuid_correct_list)):
            if uuid_correct_list[i]:
                state = await self._get_state_task(
                    primary_recommendations[i]["row_index"], primary_recommendations[i]["row_uuid"]
                )
                if state is not None:
                    return state

        for i in range(len(uuid_correct_list_with_state_replace)):
            if uuid_correct_list_with_state_replace[i]:
                state = await self._get_state_task(
                    primary_recommendations[i]["row_index"], primary_recommendations[i]["row_uuid"]
                )
                if state is not None:
                    return state

        return state


    @staticmethod
    def _post_primary_recs_to_sars_buffer_debug_messages(uuid_correct_list, uuid_correct_list_with_state_replace):
        logger.debug(
            f"_post_primary_recs_to_sars_buffer; "
            f"filled_up {uuid_correct_list.count(True)}/{len(uuid_correct_list)} of primary recommendations "
            f"without replace of next_state"
        )
        logger.debug(
            f"_post_primary_recs_to_sars_buffer; "
            f"filled_up {uuid_correct_list_with_state_replace.count(True)}/{len(uuid_correct_list_with_state_replace)} "
            f"of primary recommendations with replace of next_state"
        )


    async def _post_primary_recs_to_sars_buffer(self, primary_recommendations):
        """
        returns: state
            state: numpy.ndarray | None (array, if at least one partial record was filled up, state(n) of this record)
        """
        row_index_list = []
        row_uuid_list = []
        reward_list = []

        change_next_state_row_index_list = []
        change_next_state_row_uuid_list = []
        change_next_state_reward_list = []
        for i in range(len(primary_recommendations)):
            if primary_recommendations[i]["change_next_state"]:
                change_next_state_row_index_list.append(primary_recommendations[i]["row_index"])
                change_next_state_row_uuid_list.append(primary_recommendations[i]["row_uuid"])
                change_next_state_reward_list.append(primary_recommendations[i]["reward"])
            else:
                row_index_list.append(primary_recommendations[i]["row_index"])
                row_uuid_list.append(primary_recommendations[i]["row_uuid"])
                reward_list.append(primary_recommendations[i]["reward"])

        uuid_correct_list = await self._fill_up_partial_record_reward_only_list_task(
            row_index_list, row_uuid_list, reward_list
        )
        uuid_correct_list_with_state_replace = await self._fill_up_partial_record_reward_only_replace_next_state_list_task(
            change_next_state_row_index_list, change_next_state_row_uuid_list, change_next_state_reward_list
        )

        self._post_primary_recs_to_sars_buffer_debug_messages(uuid_correct_list, uuid_correct_list_with_state_replace)

        return await self._define_state_using_primary_uuids(
            primary_recommendations, uuid_correct_list, uuid_correct_list_with_state_replace
        )


    async def _post_result_recs_to_sars_buffer(self, result_recommendations, state: None | List[float]):
        if result_recommendations and state is not None:
            actions = await self._embeddings_for_landmarks(result_recommendations)

            reward = self._max_reward

            watch_state, visit_state = self._split_state(np.asarray(state, dtype=self._np_dtype))

            next_state_list = self._count_next_states_for_actions(
                watch_state, visit_state, actions, count_using_tensorflow=False
            ).tolist()

            sars_tuple_list = []
            for i in range(len(result_recommendations)):
                sars_tuple_list.append((state, actions[i], reward, next_state_list[i]))

            await self._record_list_task(sars_tuple_list)

            logger.debug(f"_post_result_recs_to_sars_buffer; {len(result_recommendations)} records added from landmarks, given by user")
    

    @staticmethod
    async def _start_training(repeat_amount):
        logger.debug(f"{repeat_amount} training cycles")
        train_async_task = asyncio.create_task(
            AbstractAgentsBroker.call_agent_task(
                train, {"repeat_amount": repeat_amount}
            )
        )
        return (await train_async_task).return_value


    async def post_result_of_recommendations(self, json_params):
        logger.debug(f"post_result_of_recommendations")
        if not self._requires_training:
            logger.info("RecSys agent doesn't requires training.")
            return

        try:
            self._post_result_of_recommendations_validation(json_params)
        except ValidationError as ex:
            await logger.error(f"post_result_of_recommendations, ValidationError({ex.args[0]})")
            return  # raise ValidationError

        primary_recommendations, result_recommendations = self._give_reward_to_recommendations(
            json_params["primary_recommendations"],
            json_params["result_recommendations"],
            json_params["user_reward"]
        )
        
        state = await self._post_primary_recs_to_sars_buffer(primary_recommendations)
        await self._post_result_recs_to_sars_buffer(result_recommendations, state)
        
        new_models_json = await self._start_training(
            len(primary_recommendations) + len(result_recommendations)
        )
        self._update_model(self._actor_model, new_models_json["actor_model"], self._np_dtype)
        self._update_model(self._critic_model, new_models_json["critic_model"], self._np_dtype)

