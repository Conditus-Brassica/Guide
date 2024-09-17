from recommendations_agent.actor_model import get_actor_model
from recommendations_agent.critic_model import get_critic_model
from recommendations_agent.trainer_agent import TrainerAgent
from recommendations_agent.trainer import Trainer
from recommendations_agent.sars_replay_buffer import SARSReplayBuffer
import numpy as np
import tensorflow as tf
import keras
from backend.agents.recommendations_agent.trainer_agent import TrainerAgent


if TrainerAgent.trainer_agent_exists():
    TRAINER_AGENT = TrainerAgent.get_trainer_agent()
    print("Trainer agent wasn't created")  # TODO remove
else:
    actor_model = get_actor_model(dtype=tf.float32, state_size=3, input_units=256 , action_size=1, hidden_units=[256])
    critic_model = get_critic_model(
        dtype=tf.float32, state_size=3, action_size=1, state_input_units=16, action_input_units=32, state_hidden_units=[32], concat_hidden_units=[256, 256]
    )

    target_actor_model = get_actor_model(dtype=tf.float32, state_size=3, input_units=256 , action_size=1, hidden_units=[256])
    target_actor_model.set_weights(actor_model.get_weights())

    target_critic_model = get_critic_model(
        dtype=tf.float32, state_size=3, action_size=1, state_input_units=16, action_input_units=32, state_hidden_units=[32], concat_hidden_units=[256, 256]
    )
    target_critic_model.set_weights(critic_model.get_weights())

    buffer = SARSReplayBuffer(state_size=3, action_size=1, dtype=np.float32)
    gamma = 0.99
    tau = 5e-3

    critic_lr = 0.002
    actor_lr = 0.001

    critic_optimizer = keras.optimizers.Adam(critic_lr)
    actor_optimizer = keras.optimizers.Adam(actor_lr)

    trainer = Trainer(
        actor_model, critic_model, gamma,
        actor_optimizer, critic_optimizer,
        target_actor_model, target_critic_model, tau,
        buffer,
        np.float32
    )

    TRAINER_AGENT = TrainerAgent(trainer)
    print("Trainer agent was created")  # TODO remove