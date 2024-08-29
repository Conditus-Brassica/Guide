# Author: Vodohleb04
from operator import concat
from typing import List
from keras import layers
import keras
import tensorflow as tf

HE_INIT = keras.initializers.HeNormal()


class CriticModel(keras.Model):
    """
    Model to generate Q-value for the given state and action.
    Model is based on DDPG Critic model from https://arxiv.org/pdf/1509.02971.

    Check https://drive.google.com/file/d/1GQIfN6j1q9uASHh9LYubgxs5XPQtwQyy/view?usp=sharing to understand structure of Critic model.
    """
    @staticmethod
    def _define_hidden_network(hidden_units: List[int], dtype: tf.DType):
        hidden_layers = [
            None for _ in range(3 * len(hidden_units))
        ]
        i = 0
        while i < len(hidden_units):
            hidden_layers[3 * i] = layers.Dense(
                hidden_units[i], use_bias=False, kernel_initializer=HE_INIT, dtype=dtype
            )
            hidden_layers[3 * i + 1] = layers.BatchNormalization(dtype=dtype)
            hidden_layers[3 * i + 2] = layers.LeakyReLU(negative_slope=0.3)

            i += 1
        
        return keras.Sequential(hidden_layers)
        

    def __init__(
            self,
            dtype: tf.DType,
            state_input_units: int, action_input_units,
            state_hidden_units: List[int] | None = None,
            action_hidden_units: List[int] | None = None,
            concat_hidden_units: List[int] | None = None
        ):
        super().__init__()

        self._state_hidden_network = None
        self._action_hidden_network = None
        self._concat_hidden_network = None

        self._state_input_dense = layers.Dense(state_input_units, use_bias=False, kernel_initializer=HE_INIT, dtype=dtype)
        self._state_input_batch_norm = layers.BatchNormalization(dtype=dtype)

        if state_hidden_units:
            self._state_hidden_network = self._define_hidden_network(state_hidden_units, dtype)
        
        self._action_input_dense = layers.Dense(action_input_units, use_bias=False, kernel_initializer=HE_INIT, dtype=dtype)
        self._action_input_batch_norm = layers.BatchNormalization(dtype=dtype)
        
        if action_hidden_units:
            self._action_hidden_network = self._define_hidden_network(action_hidden_units, dtype)
        
        if state_hidden_units and action_hidden_units:
            concat_units = state_hidden_units[-1] + action_hidden_units[-1]
        elif state_hidden_units:
            concat_units = state_hidden_units[-1] + action_input_units
        elif action_hidden_units:
            concat_units = state_input_units + action_hidden_units[-1]
        else:
            concat_units = state_input_units + action_input_units
        self._concat_dense = layers.Dense(concat_units, use_bias=False, kernel_initializer=HE_INIT, dtype=dtype)
        self._concat_batch_norm = layers.BatchNormalization(dtype=dtype)

        if concat_hidden_units:
            self._concat_hidden_network = self._define_hidden_network(concat_hidden_units, dtype)

        self._concat_output_dense = layers.Dense(1, use_bias=True, dtype=dtype)

    
    def __call__(self, state, action):
        state = self._state_input_dense(state)
        state = self._state_input_batch_norm(state)
        state = tf.nn.leaky_relu(state, alpha=0.3)

        if self._state_hidden_network:
            state = self._state_hidden_network(state)

        action = self._action_input_dense(action)
        action = self._action_input_batch_norm(action)
        action = tf.nn.leaky_relu(action, alpha=0.3)

        if self._action_hidden_network:
            action = self._action_hidden_network(action)

        critic_value = tf.concat([state, action], axis=1)

        critic_value = self._concat_dense(critic_value)
        critic_value = self._concat_batch_norm(critic_value)
        critic_value = tf.nn.leaky_relu(critic_value, alpha=0.3)

        if self._concat_hidden_network:
            critic_value = self._concat_hidden_network(critic_value)
        
        critic_value = self._concat_output_dense(critic_value)

        return critic_value


# TODO make test
