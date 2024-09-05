# Author: Vodohleb04
from typing import Tuple
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
            sars_buffer: SARSReplayBuffer
    ):
        self._actor_model = actor_model
        self._critic_model = critic_model

        self._gamma = gamma

        self._actor_optimizer = actor_optimizer
        self._critic_optimizer = critic_optimizer
        
        self._target_actor_model = target_actor_model
        self._target_critic_model = target_critic_model 
        self.tau = tau

        self._sars_buffer = sars_buffer
        
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

    @property
    def tau(self) -> float:
        return self._tau
    
    @tau.setter
    def tau(self, tau: float):
        self._tau = tau

    async def partial_record(self, state: np.ndarray, action: np.ndarray):
        """
        Is used to write first part of sars tuple. This tuple will be saved, but won't be used in training samples

        ###
        1. state: numpy.ndarray
        2. action: numpy.ndarray

        returns: Tuple[int, uuid] - index of row in buffer and uuid of row.
        """
        
        return self._sars_buffer.partial_record(state, action)
    
    async def fill_up_partial_record(self, row_index, row_uuid, reward: np.ndarray, next_state: np.ndarray):
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

    async def fill_up_partial_record_no_index(self, row_uuid, reward: np.ndarray, next_state: np.ndarray):
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
        
    async def record(self, sars_tuple: Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]):
        """
        SARS - state, action, reward, state (next state)
        If the buffer is full, the oldest record will be replaced with the new one
        """
        return self._sars_buffer.record(sars_tuple)

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


    async def train(self):
        state_batch, action_batch, reward_batch, next_state_batch = (
            self._sars_buffer.sample_sars_batch(return_tf_tensors=True)
        )

        self._train_critic(state_batch, action_batch, reward_batch, next_state_batch)
        self._train_actor(state_batch)

        self._update_target_model(
            self._target_actor_model, self._actor_model, self._tau
        )
        self._update_target_model(
            self._target_critic_model, self._critic_model, self._tau
        )
    
