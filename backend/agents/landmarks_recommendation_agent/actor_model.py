# Author: Vodohleb04
from typing import List
from keras import layers
import keras
import tensorflow as tf


HE_INIT = keras.initializers.HeNormal()
TANH_INIT = keras.initializers.RandomUniform(minval=-0.003, maxval=0.003)


def get_actor_model(
    dtype: tf.DType,
    state_size:int, input_units: int, action_size: int,
    hidden_units = None
):
    """
    Model to generate actions. Model works using Wolpertinger policy
    (check https://arxiv.org/pdf/1512.07679 for more details)

    The base for the Wolpertinger actor model is DDPG actor model from https://arxiv.org/pdf/1509.02971
    """

    def init_hidden_layers(hidden_units: List[int], dtype: tf.DType):
        hidden_layers = [
            None for _ in range(2 * len(hidden_units))
        ]
        
        i = 0
        while i < len(hidden_units):
            hidden_layers[2 * i] = layers.Dense(
                hidden_units[i], use_bias=True, kernel_initializer=HE_INIT, dtype=dtype
            )
            hidden_layers[2 * i + 1] = layers.LeakyReLU(negative_slope=0.3)

            i += 1

        return keras.Sequential(hidden_layers)

    input_state = layers.Input((state_size,), dtype=dtype)
    
    hidden =  layers.Dense(input_units, use_bias=True, kernel_initializer=HE_INIT, dtype=dtype)(input_state)
    hidden = layers.LeakyReLU(negative_slope=0.3)(hidden)

    if hidden_units:
        hidden = init_hidden_layers(hidden_units, dtype)(hidden)  # _hidden_network = Sequential()

    output = layers.Dense(
        action_size, use_bias=True, kernel_initializer=TANH_INIT, dtype=dtype, activation="tanh"
    )(hidden)


    return keras.Model(input_state, output)


if __name__ == "__main__":
    a = get_actor_model(tf.float32, 3, 64, 1, [256, 256])
    print(a.trainable_weights)

    state = tf.convert_to_tensor([[1., 1., 1.]], dtype=tf.float32)

    opt = keras.optimizers.Adam(learning_rate=5e-4)

    right = tf.convert_to_tensor(1, dtype=tf.float32)

    with tf.GradientTape() as tape:
        action = a(state)

        loss = tf.reduce_mean(tf.square(right - action))

    print(a.trainable_weights)
    grad = tape.gradient(loss, a.trainable_weights)
    opt.apply_gradients(zip(grad, a.trainable_weights))

    print(loss)