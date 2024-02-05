from taskiq_redis import RedisAsyncResultBackend
from .agents_broker import AgentsBroker


#with open("backend/broker/basic_login.json", 'r') as fout:
#basic_login = json.load(fout)


if AgentsBroker.broker_exists():
    BROKER = AgentsBroker.get_broker()
    print("Broker wasn't created")  # TODO remove
else:
    BROKER = AgentsBroker(
        url="redis://localhost:6379"
    ).with_result_backend(RedisAsyncResultBackend(redis_url="redis://localhost:6379"))
    print("Broker was created")  # TODO remove
