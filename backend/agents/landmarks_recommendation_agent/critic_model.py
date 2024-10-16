# Author: Vodohleb04
from operator import concat
from typing import List
from keras import layers
import keras
import tensorflow as tf
import tensorflow

HE_INIT = keras.initializers.HeNormal()


def get_critic_model(
    dtype: tf.DType,
    state_size: int, action_size: int,
    state_input_units: int, action_input_units,
    state_hidden_units: List[int] = None,
    action_hidden_units: List[int] = None,
    concat_hidden_units: List[int] = None
):
    """
    Model to generate Q-value for the given state and action.
    Model is based on DDPG Critic model from https://arxiv.org/pdf/1509.02971.

    Check https://drive.google.com/file/d/1GQIfN6j1q9uASHh9LYubgxs5XPQtwQyy/view?usp=sharing to understand structure of Critic model.
    """
    def define_hidden_network(hidden_units: List[int], dtype: tf.DType):
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

    state_input = layers.Input((state_size,), dtype=dtype)
    state = layers.Dense(state_input_units, use_bias=False, kernel_initializer=HE_INIT, dtype=dtype)(state_input)
    state = layers.BatchNormalization(dtype=dtype)(state)
    state = layers.LeakyReLU(negative_slope=0.3)(state)
    if state_hidden_units:
        state = define_hidden_network(state_hidden_units, dtype)(state)
    
    action_input = layers.Input((action_size,), dtype=dtype)
    action = layers.Dense(action_input_units, use_bias=False, kernel_initializer=HE_INIT, dtype=dtype)(action_input)
    action = layers.BatchNormalization(dtype=dtype)(action)
    action = layers.LeakyReLU(negative_slope=0.3)(action)
    if action_hidden_units:
        action = define_hidden_network(action_hidden_units, dtype)(action)
    
    concat = layers.Concatenate()([state, action])
    if concat_hidden_units:
        concat = define_hidden_network(concat_hidden_units, dtype)(concat)

    critic_value = layers.Dense(1, use_bias=True, dtype=dtype)(concat)

    return keras.Model([state_input, action_input], critic_value)
    


if __name__ == "__main__":
    critic = get_critic_model(tf.float32, 3, 1, 16, 16, [32, 64], [32, 64], [256, 256])
    
    action = tf.convert_to_tensor([[0.53]], dtype=tf.float32)
    state = tf.convert_to_tensor([[1., 1., 1.]], dtype=tf.float32)

    critic_optim = keras.optimizers.Adam(learning_rate=5e-4)

    right = tf.convert_to_tensor(1, dtype=tf.float32)

    with tf.GradientTape() as tape:
        critic_value = critic([state, action])

        loss = tf.reduce_mean(tf.square(right - critic_value))
        print(loss)

    print(critic.trainable_weights)
    gradient = tape.gradient(loss, critic.trainable_weights)
    critic_optim.apply_gradients(zip(gradient, critic.trainable_weights))



