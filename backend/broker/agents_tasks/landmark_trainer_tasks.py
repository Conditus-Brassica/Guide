from backend.broker.broker_initializer import BROKER
from backend.agents.recommendation_systems.landmark_trainer.landmark_trainer_initializer import TRAINER_AGENT


@BROKER.task
async def get_actor_model(json_params):
    return await TRAINER_AGENT.get_actor_model()

@BROKER.task
async def set_actor_model(json_params):
    return await TRAINER_AGENT.set_actor_model(json_params)

@BROKER.task
async def get_actor_model_config(json_params):
    return await TRAINER_AGENT.get_actor_model_config()

@BROKER.task
async def get_critic_model(json_params):
    return await TRAINER_AGENT.get_critic_model()

@BROKER.task
async def get_critic_model_config(json_params):
    return await TRAINER_AGENT.get_critic_model_config()

@BROKER.task
async def partial_record(json_params):
    return await TRAINER_AGENT.partial_record(json_params)

@BROKER.task
async def partial_record_list(json_params):
    return await TRAINER_AGENT.partial_record_list(json_params)

@BROKER.task
async def fill_up_partial_record(json_params):
    return await TRAINER_AGENT.fill_up_partial_record(json_params)

@BROKER.task
async def fill_up_partial_record_list(json_params):
    return await TRAINER_AGENT.fill_up_partial_record_list(json_params)

@BROKER.task
async def partial_record_with_next_state(json_params):
    return await TRAINER_AGENT.partial_record_with_next_state(json_params)

@BROKER.task
async def partial_record_list_with_next_state(json_params):
    return await TRAINER_AGENT.partial_record_list_with_next_state(json_params)

@BROKER.task
async def fill_up_partial_record_reward_only(json_params):
    return await TRAINER_AGENT.fill_up_partial_record_reward_only(json_params)

@BROKER.task
async def fill_up_partial_record_reward_only_list(json_params):
    return await TRAINER_AGENT.fill_up_partial_record_reward_only_list(json_params)

@BROKER.task
async def fill_up_partial_record_reward_only_replace_next_state(json_params):
    return await TRAINER_AGENT.fill_up_partial_record_reward_only_replace_next_state(json_params)

@BROKER.task
async def fill_up_partial_record_reward_only_replace_next_state_list(json_params):
    return await TRAINER_AGENT.fill_up_partial_record_reward_only_replace_next_state_list(json_params)

@BROKER.task
async def record(json_params):
    return await TRAINER_AGENT.record(json_params)

@BROKER.task
async def record_list(json_params):
    return await TRAINER_AGENT.record_list(json_params)

@BROKER.task
async def train(json_params):
    return await TRAINER_AGENT.train(json_params)

@BROKER.task
async def get_state(json_params):
    return await TRAINER_AGENT.get_state(json_params)

@BROKER.task
async def remove_record(json_params):
    return await TRAINER_AGENT.remove_record(json_params)

@BROKER.task
async def remove_record_list(json_params):
    return await TRAINER_AGENT.remove_record_list(json_params)




