import numpy as np
import tensorflow as tf
from backend.agents.landmarks_recommendation_agent.ornstein_uhlenbeck_action_noise import OrnsteinUhlenbeckNoise
from backend.agents.landmarks_recommendation_agent.recommendations_agent import RecommendationsAgent


if RecommendationsAgent.recommendations_agent_exists():
    RECOMMENDATIONS_AGENT = RecommendationsAgent.get_recommendations_agent()
    print("Recommendations agent wasn't created")  # TODO remove
else:
    ou_noise = OrnsteinUhlenbeckNoise(
        np.float32,
        mean=np.zeros(1, dtype=np.float32),
        std_deviation=0.2 * np.ones(1, dtype=np.float32)
    )

    RECOMMENDATIONS_AGENT = RecommendationsAgent(tf_dtype=tf.float32, np_dtype=np.float32, noise_object=ou_noise)
    print("Recommendations agent was created")  # TODO remove