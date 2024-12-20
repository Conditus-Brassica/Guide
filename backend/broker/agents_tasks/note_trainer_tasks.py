from backend.broker.broker_initializer import BROKER
from backend.agents.recommendation_systems.note_trainer.note_trainer_initializer import TRAINER_AGENT


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
async def set_critic_model(json_params):
    return await TRAINER_AGENT.set_critic_model(json_params)

@BROKER.task
async def get_critic_model_config(json_params):
    return await TRAINER_AGENT.get_critic_model_config()

@BROKER.task
async def get_tau(json_params):
    return await TRAINER_AGENT.get_tau()

@BROKER.task
async def set_tau(json_params):
    return await TRAINER_AGENT.set_tau(json_params)

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
async def train(json_params):
    return await TRAINER_AGENT.train(json_params)





