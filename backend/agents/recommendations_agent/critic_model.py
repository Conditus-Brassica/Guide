# Author: Vodohleb04
from operator import concat
from typing import List
from keras import layers
import keras
import tensorflow as tf
import tensorflow

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

        if self._concat_hidden_network:
            critic_value = self._concat_hidden_network(critic_value)
        
        critic_value = self._concat_output_dense(critic_value)

        return critic_value


if __name__ == "__main__":
    critic = CriticModel(tf.float32, 16, 16, [32, 64], [32, 64], [256, 256])
    
    action = tf.convert_to_tensor([[0.53]], dtype=tf.float32)
    state = tf.convert_to_tensor([[1., 1., 1.]], dtype=tf.float32)

    critic_optim = keras.optimizers.Adam(learning_rate=5e-4)

    right = tf.convert_to_tensor(1, dtype=tf.float32)

    with tf.GradientTape() as tape:
        critic_value = critic(state, action)

        loss = tf.reduce_mean(tf.square(right - critic_value))
        print(loss)

    print(critic.trainable_weights)
    gradient = tape.gradient(loss, critic.trainable_weights)
    critic_optim.apply_gradients(zip(gradient, critic.trainable_weights))



