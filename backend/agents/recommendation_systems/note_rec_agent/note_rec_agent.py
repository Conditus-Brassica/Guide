# Author: Vodohleb04
import asyncio
import tensorflow as tf
import keras
import numpy as np
from typing import Dict, List, Tuple
from jsonschema import validate, ValidationError
from aiologger.loggers.json import JsonLogger
import backend.agents.recommendation_systems.note_rec_agent.note_rec_json_validation as json_validation
from backend.agents.recommendation_systems.note_rec_agent.pure_note_rec_agent import PureNoteRecAgent
from backend.agents.recommendation_systems.note_rec_sys_user_reaction import UserReaction
from backend.broker.abstract_agents_broker import AbstractAgentsBroker
from backend.broker.agents_tasks.note_embeddings_crud_agent_tasks import get_notes_by_titles, get_nearest_notes

from backend.broker.agents_tasks.note_trainer_tasks import (
    partial_record_with_next_state, fill_up_partial_record_reward_only_list,
    train, get_actor_model, get_critic_model, get_actor_model_config, get_critic_model_config
)


logger = JsonLogger.with_default_handlers(
    level="DEBUG",
    serializer_kwargs={'ensure_ascii': False},
)


class NoteRecAgent(PureNoteRecAgent):
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
        state_discount_factor: float = 0.9,
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
        4. *state_discount_factor: float [DEFAULT = 0.9]
            - discount factor of state (check RecommendationsAgent.count_new_state method)
        """
        if not self.recommendations_agent_exists():
            self._asyncio_tasks = set()

            if actor_weights_file is None and critic_weights_file is None:
                self._default_models_init()
            else:
                self._init_models_from_files(actor_weights_file, critic_weights_file)

            self._noise_object = noise_object

            self._state_discount_factor = state_discount_factor

            self._tf_dtype = tf_dtype
            self._np_dtype = np_dtype
            
            self._single_recommendations_agent = self
        else:
            raise RuntimeError("Unexpected behaviour, this class can have only one instance")


    @staticmethod
    def reward_function(relative_interaction_time, user_reaction: UserReaction):
        """
            Counts immediate reward in Markov decision process. Takes user interaction time, relative to the expected
            reading time of the note, and takes user reaction that is Like, Neutral or Dislike.

            :param relative_interaction_time: float in range[0, 1] - user interaction time, relative to the expected
            reading time of the note
            :param user_reaction: Enum.UserReaction

            :returns: float
        """
        return 70 * min(relative_interaction_time * user_reaction.value - 1.5, 0)


    @staticmethod
    def _update_model(model, py_weigths, dtype):
        model.set_weights(
            [
                np.asarray(py_weigths[i], dtype=dtype)
                for i in range(len(py_weigths))
            ]
        )


    async def _embeddings_for_notes(self, note_titles_list):
        json_params = {"note_titles": note_titles_list}
        embeddings_async_task = asyncio.create_task(
            AbstractAgentsBroker.call_agent_task(get_notes_by_titles, json_params)
        )
        self._asyncio_tasks.add(embeddings_async_task)
        embeddings_async_task.add_done_callback(self._asyncio_tasks.discard)

        embeddings_asyncio_result = await embeddings_async_task
        await logger.debug(
            f"Recommendations agent, _embeddings_for_notes, "
            f"embeddings_for_landmarks: {embeddings_asyncio_result}"
        )

        return embeddings_asyncio_result.return_value


    async def count_new_state(self, json_params) -> List[float]:
        try:
            validate(json_params, json_validation.count_new_state)
        except ValidationError as ex:
            await logger.error(f"count_new_state, ValidationError({ex.args[0]})")
            return []  # raise ValidationError

        state = np.asarray(json_params["state"], dtype=self._np_dtype)

        note_titles = [new_note["title"] for new_note in json_params["new_notes"]]  # now it's list of notes titles

        embeddings = await self._embeddings_for_notes(note_titles) # returns Dict[note_title: embedding] (order is changed)

        new_notes_embeddings = [embeddings[note_title] for note_title in note_titles]  # now notes are in correct order
        new_notes_embeddings = np.asarray(new_notes_embeddings, dtype=self._np_dtype)

        for i in range(new_notes_embeddings.shape[0]):
            state = self._new_state_formula(state, new_notes_embeddings[i])

        return state.tolist()


    def _new_state_formula(self, state, new_note_embedding):
        return state * self._state_discount_factor + new_note_embedding


    @staticmethod
    def _make_recommendations_validation(json_params):
        """This method checks values only of special params. Other values will be checked in target agent."""
        validate(json_params, json_validation.make_recommendations)
        if json_params["maximum_amount_of_recommendations"] and json_params["maximum_amount_of_recommendations"] <= 0:
            raise ValidationError("maximum_amount_of_recommendations can\'t be less or equal to zero")


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


    async def _get_nearest_notes(self, proto_action: List[float], limit: int):
        json_params = {"note_embedding": proto_action, "limit": limit, "return_embeddings": True}
        embeddings_async_task = asyncio.create_task(
            AbstractAgentsBroker.call_agent_task(get_nearest_notes, json_params)
        )
        self._asyncio_tasks.add(embeddings_async_task)
        embeddings_async_task.add_done_callback(self._asyncio_tasks.discard)

        embeddings_asyncio_result = await embeddings_async_task
        await logger.debug(
            f"Recommendations agent, _get_nearest_notes, "
            f"embeddings_for_landmarks: {embeddings_asyncio_result}"
        )

        return embeddings_asyncio_result.return_value


    async def _wolpertinger_policy(self, state: tf.Tensor, recommendations_amount: int):
        """
            Wolpertinger policy. Check https://arxiv.org/pdf/1512.07679 for more details.
            ### Parameters
            :param state: tensorflow.Tensor
                - The state in Markov decision process. In recommendation system - the current state of the given user.
                    In recommendation system - objects, that can be recommended to the given user.
            :param recommendations_amount: int
                - The amount of the real actions that will be returned.

            returns: Tuple[tensorflow.Tensor, List[Dict]] - tensor of actions and corresponding recommendations
        """
        proto_action = self._actor_model(state)  # state shape is [1, state_dim]
        if self._noise_object:
            proto_action += tf.convert_to_tensor(self._noise_object())
        
        proto_action = tf.squeeze(proto_action, [0])  # actor_model returns shape (1, action_dim), but shape (action_dim) is needed

        embeddings_note_titles = await self._get_nearest_notes(
            proto_action.numpy().tolist(), recommendations_amount * 4
        )  # TODO Check if 400% is good
        real_actions = tf.convert_to_tensor(embeddings_note_titles["embeddings"], dtype=self._tf_dtype)
        recommendations = embeddings_note_titles["note_titles"]

        # state_for_actions shape is [n, state_dim]. The same state is copied for multiple actions
        state_for_actions = tf.tile(state, [real_actions.shape[0], 1])
        critic_values = self._critic_model([state_for_actions, real_actions])  # critic_values shape is [n, 1]

        max_critic_value_index_list = self._max_critic_values_indexes(critic_values, recommendations_amount)
        recommendations = [recommendations[index] for index in max_critic_value_index_list]
                
        return recommendations


    @staticmethod
    async def _partial_record_with_next_state_task(state, action, next_state):
        partial_record_list_async_task = asyncio.create_task(
            AbstractAgentsBroker.call_agent_task(
                partial_record_with_next_state,
                json_params={
                    "state": state,
                    "action": action,
                    "next_state": next_state
                }
            )
        )

        return (await partial_record_list_async_task).return_value


    async def _make_recommendations(self, state: np.ndarray, maximum_amount_of_recommendations):
        recommendations = await self._wolpertinger_policy(
            tf.expand_dims(
                tf.convert_to_tensor(state, dtype=self._tf_dtype), axis=0
            ),  # expands state shape to [1, state_dim]
            maximum_amount_of_recommendations
        )
 
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


    async def make_recommendations(self, json_params: Dict):
        try:
            self._make_recommendations_validation(json_params)
        except ValidationError as ex:
            await logger.error(f"make_recommendations, ValidationError({ex.args[0]})")
            return []  # raise ValidationError
        
        maximum_amount_of_recommendations = json_params["maximum_amount_of_recommendations"]

        state = np.asarray(json_params["state"], dtype=self._np_dtype)

        if not self._actor_critic_are_inited:
            await self._init_actor_critic_models()
            
        return await self._make_recommendations(state, maximum_amount_of_recommendations)


    async def interaction_with_note_started(self, json_params: Dict):
        try:
            validate(json_params, json_validation.interaction_with_note_started)
        except ValidationError as ex:
            await logger.error(f"interaction_with_note_started, ValidationError({ex.args[0]})")
            return {}  # raise ValidationError

        if not self._requires_training:
            await logger.info("RecSys agent doesn't require training. No sars records will be completed")
            return {}

        state = np.asarray(json_params["state"], dtype=self._np_dtype)

        note_embedding = await self._embeddings_for_notes([json_params["note_title"]])
        note_embedding = note_embedding["notes"][json_params["note_title"]]
        note_embedding = np.asarray(note_embedding, dtype=self._np_dtype)

        next_state = self._new_state_formula(state, note_embedding)
        index, uuid = await self._partial_record_with_next_state_task(
            state.tolist(), note_embedding.tolist(), next_state.tolist()
        )

        return {"row_uuid": uuid, "row_index": index}
    

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
    async def _start_training(repeat_amount):
        await logger.debug(f"{repeat_amount} training cycles")
        train_async_task = asyncio.create_task(
            AbstractAgentsBroker.call_agent_task(
                train, {"repeat_amount": repeat_amount}
            )
        )
        return (await train_async_task).return_value


    @staticmethod
    async def _interactions_with_notes_finished_debug_messages(uuid_correct_list):
        await logger.debug(
            f"_interactions_with_notes_finished; "
            f"filled_up {uuid_correct_list.count(True)}/{len(uuid_correct_list)} of finished interactions"
        )


    async def _interactions_with_notes_finished(self, json_params: Dict):
        row_uuid_list = []
        row_index_list = []
        reward_list = []
        for interaction in json_params["interactions"]:
            row_uuid_list.append(interaction["row_uuid"])
            row_index_list.append(interaction["row_index"])
            reward_list.append(
                self.reward_function(interaction["relative_interaction_time"], interaction["user_reaction"])
            )

        uuid_correct_list = await self._fill_up_partial_record_reward_only_list_task(
            row_index_list, row_uuid_list, reward_list
        )
        await self._interactions_with_notes_finished_debug_messages(uuid_correct_list)

        new_models_json = await self._start_training(len(json_params["interactions"]))

        self._update_model(self._actor_model, new_models_json["actor_model"], self._np_dtype)
        self._update_model(self._critic_model, new_models_json["critic_model"], self._np_dtype)


    async def interactions_with_notes_finished(self, json_params):
        await logger.debug(f"interactions_with_notes_finished")
        if not self._requires_training:
            await logger.info("RecSys agent doesn't requires training.")
            return

        try:
            validate(json_params, json_validation.interaction_with_note_finished)
        except ValidationError as ex:
            await logger.error(f"interactions_with_notes_finished, ValidationError({ex.args[0]})")
            return  # raise ValidationError

        await self._interactions_with_notes_finished(json_params)