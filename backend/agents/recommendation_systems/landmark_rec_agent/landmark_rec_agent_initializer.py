import numpy as np
import tensorflow as tf
from backend.agents.recommendation_systems.ornstein_uhlenbeck_action_noise import OrnsteinUhlenbeckNoise
from backend.agents.recommendation_systems.landmark_rec_agent.landmark_rec_agent import LandmarkRecAgent


if LandmarkRecAgent.recommendations_agent_exists():
    LANDMARK_REC_AGENT = LandmarkRecAgent.get_recommendations_agent()
    print("Recommendations agent wasn't created")  # TODO remove
else:
    ou_noise = OrnsteinUhlenbeckNoise(
        np.float32,
        mean=np.zeros(1, dtype=np.float32),
        std_deviation=0.2 * np.ones(1, dtype=np.float32)
    )

    LANDMARK_REC_AGENT = LandmarkRecAgent(tf_dtype=tf.float32, np_dtype=np.float32, noise_object=ou_noise)
    print("Recommendations agent was created")  # TODO remove