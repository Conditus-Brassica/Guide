# Author: Vodohleb04
from typing import Tuple
import tensorflow as tf
import numpy as np


class SARSReplayBuffer:
    """Buffer to save SARS records (check https://arxiv.org/pdf/1509.02971 to get more information)"""
    def __init__(self, state_size, action_size, dtype, buffer_capacity=1e6, batch_size=64):
        self._buffer_capacity = int(buffer_capacity)
        self._batch_size = batch_size

        self._current_index = 0
        self._buffer_is_filled = False

        self._state_buffer = np.zeros((self._buffer_capacity, state_size), dtype=dtype)
        self._action_buffer = np.zeros((self._buffer_capacity, action_size), dtype=dtype)
        self._reward_buffer = np.zeros((self._buffer_capacity, 1), dtype=dtype)
        self._next_state_buffer = np.zeros((self._buffer_capacity, state_size), dtype=dtype)

    def record(self, sars_tuple: Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]) -> None:
        """
        SARS - state, action, reward, state (next state)
        If the buffer is full, the oldest record will be replaced with the new one
        """
        self._state_buffer[self._current_index] = sars_tuple[0]
        self._action_buffer[self._current_index] = sars_tuple[1]
        self._reward_buffer[self._current_index] = sars_tuple[2]
        self._next_state_buffer[self._current_index] = sars_tuple[3]

        self._current_index += 1
        if self._current_index == self._buffer_capacity:
            self._buffer_is_filled = True
            self._current_index = 0

    def sample_sars_batch(self, return_tf_tensors=False) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """
        Samples random batch of SARS from the replay buffer
        """
        if self._buffer_is_filled:
            buffer_range = self._buffer_capacity
        else:
            buffer_range = self._current_index
        batch_indices = np.random.choice(buffer_range, size=self._batch_size)

        if return_tf_tensors:
            return (
                tf.convert_to_tensor(self._state_buffer[batch_indices]),
                tf.convert_to_tensor(self._action_buffer[batch_indices]),
                tf.convert_to_tensor(self._reward_buffer[batch_indices]),
                tf.convert_to_tensor(self._next_state_buffer[batch_indices])
            )
        else:
            return (
                self._state_buffer[batch_indices],
                self._action_buffer[batch_indices],
                self._reward_buffer[batch_indices],
                self._next_state_buffer[batch_indices]
            )
