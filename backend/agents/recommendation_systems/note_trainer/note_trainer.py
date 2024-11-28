# Author: Vodohleb04
import threading
from typing import Tuple, List
import keras
import tensorflow as tf
import numpy as np
from backend.agents.recommendation_systems.sars_replay_buffer import SARSReplayBuffer
from backend.broker.abstract_agents_broker import AbstractAgentsBroker
from backend.broker.agents_tasks.note_embeddings_crud_agent_tasks import get_nearest_one_for_notes_batch


class NoteTrainer:
    
    def  __init__(
            self,
            actor_model: keras.Model, critic_model: keras.Model, gamma: float,
            actor_optimizer: keras.optimizers.Optimizer, critic_optimizer: keras.optimizers.Optimizer,
            target_actor_model: keras.Model, target_critic_model: keras.Model, tau: float,
            sars_buffer: SARSReplayBuffer,
            np_dtype: np.dtype, tf_dtype: tf.DType,
            actor_save_file: str, critic_save_file: str,
            target_actor_save_file: str, target_critic_save_file: str,
            save_period: int = 50
    ):
        """
        :param actor_model: keras.Model
            - Actor network, counts action from the given state in terms of Markov decision process (check https://arxiv.org/pdf/1509.02971 for more details).
        :param critic_model: keras.Model
            - Critic network, counts Q-value from the given state and action (check https://arxiv.org/pdf/1509.02971 for more details).
        :param gamma: float
            - discount factor of reward
        :param actor_optimizer: keras.optimizers.Optimizer
            - Optimizer for actor_model
        :param critic_optimizer: keras.optimizers.Optimizer
            - Optimizer for critic_model
        :param target_actor_model: keras.Model
            - Target actor model (check https://arxiv.org/pdf/1509.02971 for more details)
        :param target_critic_model: keras.Model
            - Target critic model (check https://arxiv.org/pdf/1509.02971 for more details)
        :param tau: float
            - Coefficient used in updating target weights  target_weight = (1 - tau) * target_weight + tau * original_model_weight
            (check https://arxiv.org/pdf/1509.02971 for more details)
        :param sars_buffer: SARSReplayBuffer
            - Replay buffer to save state-action-reward-next_state tuples (check https://arxiv.org/pdf/1509.02971 for more details)
        :param np_dtype: np.dtype
            - np.dtype used in SARSReplayBuffer and models (tensorflow.DType equivalent is used in models)
        :param tf_dtype: tf.DType
            -tf.DType used in tensorflow models
        :param actor_save_file: str
            - path to the file, where actor_model will be saved
        :param critic_save_file: str
            - path to the file, where critic_model will be saved
        :param target_actor_save_file: str
            - path to the file, where target_actor_model will be saved
        :param target_critic_save_file: str
            - path to the file, where target_critic_model will be saved
        :param save_period: int [DEFAULT=50]
            - amount of training repeats between save of the models and SARSReplayBuffer
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
        self.tf_dtype = tf_dtype

        self._actor_save_file = actor_save_file
        self._critic_save_file = critic_save_file
        self._target_actor_save_file = target_actor_save_file
        self._target_critic_save_file = target_critic_save_file
        self._save_period = save_period
        self._after_last_save = 0


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


    def partial_record_with_next_state(self, state: np.ndarray, action: np.ndarray, next_state: np.ndarray):
        return self._sars_buffer.partial_record_with_next_state(state, action, next_state)


    def partial_record_list_with_next_state(
            self, state: np.ndarray, action_list: List[np.ndarray], next_state_list: List[np.ndarray]
    ):
        index_list = []
        uuid_list = []

        for i in range(len(action_list)):
            index, uuid = self._sars_buffer.partial_record_with_next_state(state, action_list[i], next_state_list[i])
            index_list.append(index)
            uuid_list.append(uuid)

        return index_list, uuid_list


    def fill_up_partial_record_reward_only(self, row_index, row_uuid, reward: np.ndarray):
        return self._sars_buffer.fill_up_partial_record_reward_only(row_index, row_uuid, reward)


    def fill_up_partial_record_reward_only_list(self, row_index_list, row_uuid_list, reward_list: np.ndarray):
        if len(row_index_list) != len(row_uuid_list) or len(row_index_list) != len(reward_list):
            raise ValueError(
                "row_index_list, row_uuid_list and reward_list must be lists of the same length"
            )
        record_filled_up_list = []

        for i in range(len(row_index_list)):
            record_filled_up_list.append(
                self._sars_buffer.fill_up_partial_record_reward_only(
                    row_index_list[i], row_uuid_list[i], reward_list[i]
                )
            )

        return record_filled_up_list


    @staticmethod
    def _update_target_model(target_model, original_model, tau):
        target_weights = target_model.get_weights()
        original_weights = original_model.get_weights()

        for i in range(len(target_weights)):
            target_weights[i] = (1 - tau) * target_weights[i] + tau * original_weights[i] 

        target_model.set_weights(target_weights)


    async def _get_nearest_one_for_notes_batch(self, proto_action):
        json_params = {"notes_embeddings": proto_action.numpy().tolist()}
        embeddings = await AbstractAgentsBroker.call_agent_task(get_nearest_one_for_notes_batch, json_params)
        embeddings = embeddings.return_value

        real_actions = tf.convert_to_tensor(embeddings["embeddings"], dtype=self.tf_dtype)
        return real_actions


    async def _train_critic(
            self, state_batch: tf.Tensor, action_batch: tf.Tensor, reward_batch: tf.Tensor, next_state_batch: tf.Tensor
        ):
        with tf.GradientTape() as critic_tape:
            proto_action_batch = self._target_actor_model(next_state_batch)
            target_action_batch = await self._get_nearest_one_for_notes_batch(proto_action_batch)
            y = reward_batch + self._gamma * self._target_critic_model([next_state_batch, target_action_batch])  # r + g*Q'(s_n, A'(s_n))

            critic_value = self._critic_model([state_batch, action_batch])
            
            critic_loss = tf.reduce_mean(tf.square(y - critic_value))
        critic_gradients = critic_tape.gradient(critic_loss, self._critic_model.trainable_weights)
        self._critic_optimizer.apply_gradients(zip(critic_gradients, self._critic_model.trainable_weights))


    def _train_actor(self, state_batch: tf.Tensor):
        with tf.GradientTape() as actor_tape:
            action_batch = self._actor_model(state_batch)
            critic_value = self._critic_model([state_batch, action_batch])

            actor_loss = -tf.reduce_mean(critic_value)
        actor_gradients = actor_tape.gradient(actor_loss, self._actor_model.trainable_weights)
        self._actor_optimizer.apply_gradients(zip(actor_gradients, self._actor_model.trainable_weights))


    def _save_models_and_buffer(self):
        save_threads = [
            threading.Thread(target=self._sars_buffer.save, args=()),
            threading.Thread(target=self._actor_model.save, args=(self._actor_save_file,)),
            threading.Thread(target=self._critic_model.save, args=(self._critic_save_file,)),
            threading.Thread(target=self._target_actor_model.save, args=(self._target_actor_save_file,)),
            threading.Thread(target=self._target_critic_model.save, args=(self._target_critic_save_file,)),
        ]
        for i in range(len(save_threads)):
            save_threads[i].start()
        for i in range(len(save_threads)):
            save_threads[i].join()


    async def train(self, repeat_amount: int = 1):
        if repeat_amount <= 0:
            raise ValueError(f"repeat_amount is expected to be int value > 0, got {repeat_amount} instead")
        if self._sars_buffer.completed_record_exist():
            for _ in range(repeat_amount):
                state_batch, action_batch, reward_batch, next_state_batch = (
                    self._sars_buffer.sample_sars_batch(return_tf_tensors=True)
                )

                await self._train_critic(state_batch, action_batch, reward_batch, next_state_batch)
                self._train_actor(state_batch)

                self._update_target_model(self._target_actor_model, self._actor_model, self._tau)
                self._update_target_model(self._target_critic_model, self._critic_model, self._tau)

                self._after_last_save += 1
            if self._after_last_save == self._save_period:
                self._save_models_and_buffer()
                self._after_last_save = 0
