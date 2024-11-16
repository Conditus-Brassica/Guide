# Author: Vodohleb04
import threading
from copy import copy
from typing import Tuple, List
import keras
import tensorflow as tf
import numpy as np
from backend.agents.recommendation_systems.sars_replay_buffer import SARSReplayBuffer


class LandmarkTrainer:
    
    def  __init__(
            self,
            actor_model: keras.Model, critic_model: keras.Model, gamma: float,
            actor_optimizer: keras.optimizers.Optimizer, critic_optimizer: keras.optimizers.Optimizer,
            target_actor_model: keras.Model, target_critic_model: keras.Model, tau: float,
            sars_buffer: SARSReplayBuffer,
            np_dtype: np.dtype,
            actor_save_file: str, critic_save_file: str,
            target_actor_save_file: str, target_critic_save_file: str,
            save_period: int = 50
    ):
        """
        ###
        1. actor_model: keras.Model
            - Actor network, counts action from the given state in terms of Markov decision process (check https://arxiv.org/pdf/1509.02971 for more details).
        2. critic_model: keras.Model
            - Critic network, counts Q-value from the given state and action (check https://arxiv.org/pdf/1509.02971 for more details).
        3. gamma: float
            - discount factor of reward
        4. actor_optimizer: keras.optimizers.Optimizer
            - Optimizer for actor_model
        5. critic_optimizer: keras.optimizers.Optimizer
            - Optimizer for critic_model
        6. target_actor_model: keras.Model
            - Target actor model (check https://arxiv.org/pdf/1509.02971 for more details)
        7. target_critic_model: keras.Model
            - Target critic model (check https://arxiv.org/pdf/1509.02971 for more details)
        8. tau: float
            - Coefficient used in updating target weights  target_weight = (1 - tau) * target_weight + tau * original_model_weight
            (check https://arxiv.org/pdf/1509.02971 for more details)
        9. sars_buffer: SARSReplayBuffer
            - Replay buffer to save state-action-reward-next_state tuples (check https://arxiv.org/pdf/1509.02971 for more details)
        10. np_dtype: np.dtype
            - np.dtype used in SARSReplayBuffer and models (tensorflow.DType equivalent is used in models)
        11. actor_save_file: str
            - path to the file, where actor_model will be saved
        12. critic_save_file: str
            - path to the file, where critic_model will be saved
        13. target_actor_save_file: str
            - path to the file, where target_actor_model will be saved
        14. target_critic_save_file: str
            - path to the file, where target_critic_model will be saved
        15. save_period: int [DEFAULT=50]
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


    def partial_record(self, state: np.ndarray, action: np.ndarray):
        return self._sars_buffer.partial_record(state, action)


    def partial_record_list(self, state: np.ndarray, action_list: List[np.ndarray]):
        """
        Is used to write first part of sars tuple. This tuple will be saved, but won't be used in training samples
        Common state for multiple actions

        ###
        1. state: numpy.ndarray
        2. action_list: List[numpy.ndarray]

        returns: Tuple[List[int], List[uuid.hex]] - indices of rows in buffer and hex of uuids of the rows in buffer.
        """
        index_list = []
        uuid_list = []

        for i in range(len(action_list)):
            index, uuid = self._sars_buffer.partial_record(state, action_list[i])
            index_list.append(index)
            uuid_list.append(uuid)
            
        return index_list, uuid_list
    

    def fill_up_partial_record(self, row_index, row_uuid, reward: np.ndarray, next_state: np.ndarray):
        """
        Is used to write the last part of sars tuple. If the given hex of uuid was found in buffer, reward and next_state will be saved
            and the row may be used in training batch.

        1. row_index: int
            - index of the row in buffer (such index is returned as result of partial_record method) 
        2. row_uuid: uuid.hex
            - hex of uuid of the row in buffer (such hex of uuid is returned as result of partial_record method)
        3. reward: numpy.ndarray
        4. next_state: numpy.ndarray

        returns: bool - True if hex of uuid is correct, False otherwise
        """
        return self._sars_buffer.fill_up_partial_record(row_index, row_uuid, reward, next_state)  


    def fill_up_partial_record_list(
        self, row_index_list, row_uuid_list, reward_list: List[np.ndarray], next_state_list: List[np.ndarray]
    ):
        """
        Is used to write the last part of sars tuple. If the given hex of uuid was found in buffer, reward and next_state will be saved
            and the row may be used in training batch.

        1. row_index_list: List[int]
            - indices of the rows in buffer (such indices are returned as result of partial_record method) 
        2. row_uuid_list: List[uuid.hex]
            - hex of uuids of the rows in buffer (such hex of uuids are returned as result of partial_record method)
        3. reward_list: List[numpy.ndarray]
        4. next_state_list: List[numpy.ndarray]

        returns: List[bool] - True if hex of uuid is correct, False otherwise
        """
        if (len(row_index_list) != len(row_uuid_list) or
                len(row_index_list) != len(reward_list) or
                len(row_index_list) != len(next_state_list)
        ):
            raise ValueError(
                "row_index_list, row_uuid_list, reward_list and next_state_list must be lists of the same length"
            )
        record_filled_up_list = []
        
        for i in range(len(row_index_list)):
            record_filled_up_list.append(
                self._sars_buffer.fill_up_partial_record(
                    row_index_list[i], row_uuid_list[i], reward_list[i], next_state_list[i]
                )
            )

        return record_filled_up_list


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


    def fill_up_partial_record_reward_only_replace_next_state(self, row_index, row_uuid, reward: np.ndarray):
        return self._sars_buffer.fill_up_partial_record_reward_only_replace_next_state(row_index, row_uuid, reward)


    def fill_up_partial_record_reward_only_replace_next_state_list(
        self, row_index_list, row_uuid_list, reward_list: np.ndarray
    ):
        if len(row_index_list) != len(row_uuid_list) or len(row_index_list) != len(reward_list):
            raise ValueError(
                "row_index_list, row_uuid_list and reward_list must be lists of the same length"
            )
        record_filled_up_list = []

        for i in range(len(row_index_list)):
            record_filled_up_list.append(
                self._sars_buffer.fill_up_partial_record_reward_only_replace_next_state(
                    row_index_list[i], row_uuid_list[i], reward_list[i]
                )
            )

        return record_filled_up_list


    def record(self, sars_tuple: Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]):
        return self._sars_buffer.record(sars_tuple)
    

    def record_list(self, sars_tuple_list: List[Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]]):
        row_index_list = []
        row_uuid_list = []
        
        for i in range(len(sars_tuple_list)):
            row_index, row_uuid = self._sars_buffer.record(sars_tuple_list[i])
            row_index_list.append(row_index)
            row_uuid_list.append(row_uuid)

        return row_index_list, row_uuid_list


    def remove_record(self, row_index, row_uuid):
        return self._sars_buffer.remove_record(row_index, row_uuid)


    def remove_record_list(self, row_index_list, row_uuid_list):
        result = []
        for i in range(len(row_index_list)):
            result.append(self._sars_buffer.remove_record(row_index_list[i], row_uuid_list[i]))
        return result


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

                self._after_last_save += 1
            if self._after_last_save == self._save_period:
                self._save_models_and_buffer()
                self._after_last_save = 0

    
    def get_state(self, row_index: int, row_uuid) -> np.ndarray | None:
        return self._sars_buffer.get_state(row_index, row_uuid)
