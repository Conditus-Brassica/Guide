from backend.broker.broker_initializer import BROKER
from backend.agents.recommendations_agent.trainer_initializer import TRAINER_AGENT



# Read tasks


@BROKER.task
async def get_actor_model():
    return await TRAINER_AGENT.get_actor_model()

@BROKER.task
async def set_actor_model(json_params):
    return await TRAINER_AGENT.set_actor_model(json_params)

@BROKER.task
async def get_critic_model():
    return await TRAINER_AGENT.get_critic_model()

@BROKER.task
async def set_critic_model(json_params):
    return await TRAINER_AGENT.set_critic_model(json_params)

@BROKER.task
async def get_tau():
    return await TRAINER_AGENT.get_tau()

@BROKER.task
async def set_tau(json_params):
    return await TRAINER_AGENT.set_tau(json_params)

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
async def fill_up_partial_record_no_index(json_params):
    return await TRAINER_AGENT.fill_up_partial_record_no_index(json_params)

@BROKER.task
async def fill_up_partial_record_list_no_index(json_params):
    return await TRAINER_AGENT.fill_up_partial_record_list_no_index(json_params)

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

