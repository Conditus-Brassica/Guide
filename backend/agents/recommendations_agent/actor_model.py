# Author: Vodohleb04
from typing import List
from keras import layers
import keras
import tensorflow as tf


HE_INIT = keras.initializers.HeNormal()
TANH_INIT = keras.initializers.RandomUniform(minval=-0.003, maxval=0.003)


class ActorModel(keras.Model):
    """
    Model to generate actions. Model works using Wolpertinger policy
    (check https://arxiv.org/pdf/1512.07679 for more details)

    The base for the Wolpertinger actor model is DDPG actor model from https://arxiv.org/pdf/1509.02971
    """

    def _init_hidden_layers(
        self, hidden_units: List[int], dtype: tf.DType
    ):
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

        self._hidden_network = keras.Sequential(hidden_layers)

    def __init__(
            self,
            dtype: tf.DType,
            input_units: int, action_size: int,
            hidden_units: List[int] | None = None
    ):
        super().__init__()
        self._hidden_network = None  # if hidden_units is None, else - Sequential

        self._input_dense = layers.Dense(
            input_units, use_bias=True, kernel_initializer=HE_INIT, dtype=dtype
        ) 

        if hidden_units:
            self._init_hidden_layers(hidden_units, dtype)  # _hidden_network = Sequential()

            self._output_dense = layers.Dense(
                action_size, use_bias=True, kernel_initializer=TANH_INIT, dtype=dtype
            )  # tanh activation
        else:
            self._output_dense = layers.Dense(
                action_size, use_bias=True, kernel_initializer=TANH_INIT, dtype=dtype
            )  # tanh activation

    def __call__(self, x: tf.Tensor):      
        x = self._input_dense(x)
        x = tf.nn.leaky_relu(x, alpha=0.3)

        if self._hidden_network:
            x = self._hidden_network(x)

        x = self._output_dense(x)
        x = tf.nn.tanh(x)
        return x


if __name__ == "__main__":
    a = ActorModel(tf.float32, 64, 1, [256, 256])
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