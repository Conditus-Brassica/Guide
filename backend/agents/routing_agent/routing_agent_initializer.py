import openrouteservice as ors
from backend.agents.routing_agent.api_key import __key__
from backend.agents.routing_agent.routing_agent import RoutingAgent


if RoutingAgent.routing_agent_exists():
    ROUTING_AGENT = RoutingAgent.get_routing_agent()
    print("RoutingAgent wasn\'t created")
else:
    ors_client = ors.Client(key=__key__)
    ROUTING_AGENT = RoutingAgent(ors_client)
    print("RoutingAgent was created")
