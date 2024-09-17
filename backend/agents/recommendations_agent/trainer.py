# Author: Vodohleb04
from copy import copy
from typing import Tuple, List
import keras
import tensorflow as tf
import numpy as np
from backend.agents.recommendations_agent.sars_replay_buffer import SARSReplayBuffer


class Trainer:
    
    def  __init__(
            self,
            actor_model: keras.Model, critic_model: keras.Model, gamma: float,
            actor_optimizer: keras.optimizers.Optimizer, critic_optimizer: keras.optimizers.Optimizer,
            target_actor_model: keras.Model, target_critic_model: keras.Model, tau: float,
            sars_buffer: SARSReplayBuffer,
            np_dtype: np.dtype
    ):
        """
        1. actor_model: keras.Model
            - Actor network, counts action from the given state in terms of Markov decision process (check https://arxiv.org/pdf/1509.02971 for more details).
        2. critic_model: keras.Model
            - Critic network, counts Q-value from the given state and action (check https://arxiv.org/pdf/1509.02971 for more details).
        """
        self._actor_model = actor_model
        self._critic_model = critic_model

        self._gamma = gamma

        self._actor_optimizer = actor_optimizer
        self._critic_optimizer = critic_optimizer
        
        self._target_actor_model = target_actor_model
        self._target_critic_model = target_critic_model 
        self.tau = tau

        self._sars_buffer = sars_buffer
        
        self.np_dtype = np_dtype


    @property
    def actor_model(self) -> keras.Model:
        return self._actor_model
    

    @actor_model.setter
    def actor_model(self, actor_model: keras.Model):
        self._actor_model.set_weights(actor_model.get_weights())


    def get_actor_model_config(self):
        return self._actor_model.to_json()


    @property
    def critic_model(self) -> keras.Model:
        return self._critic_model
    
    
    @critic_model.setter
    def critic_model(self, critic_model: keras.Model):
        self._critic_model.set_weights(critic_model.get_weights())


    def get_critic_model_config(self):
        return self._critic_model.to_json()


    @property
    def tau(self) -> float:
        return self._tau


    @tau.setter
    def tau(self, tau: float):
        self._tau = tau


    def partial_record(self, state: np.ndarray, action: np.ndarray):
        """
        Is used to write first part of sars tuple. This tuple will be saved, but won't be used in training samples

        ###
        1. state: numpy.ndarray
        2. action: numpy.ndarray

        returns: Tuple[int, uuid] - index of row in buffer and uuid of row.
        """
        
        return self._sars_buffer.partial_record(state, action)


    def partial_record_list(self, state: np.ndarray, action_list: List[np.ndarray]):
        """
        Is used to write first part of sars tuple. This tuple will be saved, but won't be used in training samples
        Common state for multiple actions

        ###
        1. state: numpy.ndarray
        2. action_list: List[numpy.ndarray]

        returns: Tuple[List[int], List[uuid]] - indices of rows in buffer and uuids of rows in buffer.
        """
        index_list = [None for _ in range(len(action_list))]
        uuid_list = copy(index_list)

        for i in range(len(action_list)):
            index_list[i], uuid_list[i] = self._sars_buffer.partial_record(state, action_list[i])
            
        return index_list, uuid_list
    

    def fill_up_partial_record(self, row_index, row_uuid, reward: np.ndarray, next_state: np.ndarray):
        """
        Is used to write the last part of sars tuple. If the given uuid was found in buffer, reward and next_state will be saved
            and the row may be used in training batch.

        1. row_index: int
            - index of the row in buffer (such index is returned as result of partial_record method) 
        2. row_uuid: uuid
            - uuid of the row in buffer (such uuid is returned as result of partial_record method)
        3. reward: numpy.ndarray
        4. next_state: numpy.ndarray

        returns: bool - True if uuid is correct, False otherwise
        """
        return self._sars_buffer.fill_up_partial_record(row_index, row_uuid, reward, next_state)  


    def fill_up_partial_record_list(self, row_index_list, row_uuid_list, reward_list: List[np.ndarray], next_state: np.ndarray):
        """
        Is used to write the last part of sars tuple. If the given uuid was found in buffer, reward and next_state will be saved
            and the row may be used in training batch.

        1. row_index_list: List[int]
            - indices of the rows in buffer (such indices are returned as result of partial_record method) 
        2. row_uuid_list: List[uuid]
            - uuids of the rows in buffer (such uuids are returned as result of partial_record method)
        3. reward_list: List[numpy.ndarray]
        4. next_state: numpy.ndarray

        returns: List[bool] - True if uuid is correct, False otherwise
        """
        if len(row_index_list) != len(row_uuid_list) or len(row_index_list) != len(reward_list):
            raise ValueError("row_index_list, row_uuid_list and reward_list must be lists of the same length")
        record_filled_up_list = [None for _ in range(len(row_index_list))]
        
        for i in range(len(row_index_list)):
            record_filled_up_list[i] = self._sars_buffer.fill_up_partial_record(
                row_index_list[i], row_uuid_list[i], reward_list[i], next_state
            )

        return record_filled_up_list        


    def fill_up_partial_record_no_index(self, row_uuid, reward: np.ndarray, next_state: np.ndarray):
        """
        Is used to write the last part of sars tuple. If the given uuid was found in buffer, reward and next_state will be saved
            and the row may be used in training batch. Linear search is used to find out uuid.

        1. row_uuid: uuid
            - uuid of the row in buffer (such uuid is returned as result of partial_record method)
        2. reward: numpy.ndarray
        3. next_state: numpy.ndarray

        returns: bool - True if uuid was found out, False otherwise
        """
        return self._sars_buffer.fill_up_partial_record_no_index(row_uuid, reward, next_state)
    

    def fill_up_partial_record_list_no_index(self, row_uuid_list, reward_list: np.ndarray, next_state: np.ndarray):
        """
        Is used to write the last part of sars tuple. If the given uuid was found in buffer, reward and next_state will be saved
            and the row may be used in training batch. Linear search is used to find out uuid.

        1. row_uuid_list: List[uuid]
            - uuids of the rows in buffer (such uuids are returned as result of partial_record method)
        2. reward_list: numpy.ndarray
        3. next_state: numpy.ndarray

        returns: List[bool] - True if uuid was found out, False otherwise
        """
        if len(row_uuid_list) != len(reward_list):
            raise ValueError("row_uuid_list and reward_list must be lists of the same length")
        record_filled_up_list = [None for _ in range(len(row_uuid_list))]
        
        for i in range(len(row_uuid_list)):
            record_filled_up_list[i] = self._sars_buffer.fill_up_partial_record_no_index(
                row_uuid_list[i], reward_list[i], next_state
            )

        return record_filled_up_list


    def record(self, sars_tuple: Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]):
        """
        SARS - state, action, reward, state (next state)
        If the buffer is full, the oldest record will be replaced with the new one

        :returns: Tuple[int, uuid] - row index, row uuid
        """
        return self._sars_buffer.record(sars_tuple)
    

    def record_list(self, sars_tuple_list: List[Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]]):
        """
        SARS - state, action, reward, state (next state)
        If the buffer is full, the oldest record will be replaced with the new one

        :returns: Tuple[List[int], List[uuid]] - row index, row uuid
        """
        row_index_list = [None for i in range(len(sars_tuple_list))]
        row_uuid_list = copy(row_index_list)
        
        for i in range(len(sars_tuple_list)):
            row_index_list[i], row_uuid_list[i] = self._sars_buffer.record(sars_tuple_list[i])

        return row_index_list, row_uuid_list


    @staticmethod
    def _update_target_model(target_model, original_model, tau):
        target_weights = target_model.get_weights()
        original_weights = original_model.get_weights()

        for i in range(len(target_weights)):
            target_weights[i] = (1 - tau) * target_weights[i] + tau * original_weights[i] 

        target_model.set_weights(target_weights)


    def _train_critic(
            self, state_batch: tf.Tensor, action_batch: tf.Tensor, reward_batch: tf.Tensor, next_state_batch: tf.Tensor
        ):
        with tf.GradientTape() as critic_tape:
            target_action_batch = self._target_actor_model(next_state_batch)
            y = reward_batch + self._gamma * self._target_critic_model(next_state_batch, target_action_batch)  # r + g*Q'(s_n, A'(s_n))

            critic_value = self._critic_model(state_batch, action_batch)
            
            critic_loss = tf.reduce_mean(tf.square(y - critic_value))
        critic_gradients = critic_tape.gradient(critic_loss, self._critic_model.trainable_weights)
        self._critic_optimizer.apply_gradients(zip(critic_gradients, self._critic_model.trainable_weights))


    def _train_actor(self, state_batch: tf.Tensor):
        with tf.GradientTape() as actor_tape:
            action_batch = self._actor_model(state_batch)
            critic_value = self._critic_model(state_batch, action_batch)

            actor_loss = -tf.reduce_mean(critic_value)
        actor_gradients = actor_tape.gradient(actor_loss, self._actor_model.trainable_weights)
        self._actor_optimizer.apply_gradients(zip(actor_gradients, self._actor_model.trainable_weights))


    def train(self, repeat_amount: int = 1):
        if repeat_amount <= 0:
            raise ValueError(f"repeat_amount is expected to be int value > 0, got {repeat_amount} instead")
        if self._sars_buffer.completed_record_exist():
            for _ in range(repeat_amount):
                state_batch, action_batch, reward_batch, next_state_batch = (
                    self._sars_buffer.sample_sars_batch(return_tf_tensors=True)
                )

                self._train_critic(state_batch, action_batch, reward_batch, next_state_batch)
                self._train_actor(state_batch)

                self._update_target_model(self._target_actor_model, self._actor_model, self._tau)
                self._update_target_model(self._target_critic_model, self._critic_model, self._tau)
    

    def get_state(self, row_index: int, row_uuid) -> np.ndarray | None:
        return self._sars_buffer.get_state(row_index, row_uuid)
