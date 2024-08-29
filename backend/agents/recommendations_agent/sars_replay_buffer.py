# Author: Vodohleb04
from typing import Tuple
import tensorflow as tf
import numpy as np


class SARSReplayBuffer:
    """Buffer to save SARS records (check https://arxiv.org/pdf/1509.02971 to get more information)"""
    def __init__(self, state_size, action_size, dtype, buffer_capacity=1e6, batch_size=64):
        self.buffer_capacity = int(buffer_capacity)
        self.batch_size = batch_size

        self.current_index = 0
        self.buffer_is_filled = False

        self.state_buffer = np.zeros((self.buffer_capacity, state_size), dtype=dtype)
        self.action_buffer = np.zeros((self.buffer_capacity, action_size), dtype=dtype)
        self.reward_buffer = np.zeros((self.buffer_capacity, 1), dtype=dtype)
        self.next_state_buffer = np.zeros((self.buffer_capacity, state_size), dtype=dtype)

    def record(self, sars_tuple: Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]) -> None:
        """
        SARS - state, action, reward, state (next state)
        If the buffer is full, the oldest record will be replaced with the new one
        """
        self.state_buffer[self.current_index] = sars_tuple[0]
        self.action_buffer[self.current_index] = sars_tuple[1]
        self.reward_buffer[self.current_index] = sars_tuple[2]
        self.next_state_buffer[self.current_index] = sars_tuple[3]

        self.current_index += 1
        if self.current_index == self.buffer_capacity:
            self.buffer_is_filled = True
            self.current_index = 0

    def sample_sars_batch(self, return_tf_tensors=False) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """
        Samples random batch of SARS from the replay buffer
        """
        if self.buffer_is_filled:
            buffer_range = self.buffer_capacity
        else:
            buffer_range = self.current_index
        batch_indices = np.random.choice(buffer_range, size=self.batch_size)

        if return_tf_tensors:
            return (
                tf.convert_to_tensor(self.state_buffer[batch_indices]),
                tf.convert_to_tensor(self.action_buffer[batch_indices]),
                tf.convert_to_tensor(self.reward_buffer[batch_indices]),
                tf.convert_to_tensor(self.next_state_buffer[batch_indices])
            )
        else:
            return (
                self.state_buffer[batch_indices],
                self.action_buffer[batch_indices],
                self.reward_buffer[batch_indices],
                self.next_state_buffer[batch_indices]
            )
