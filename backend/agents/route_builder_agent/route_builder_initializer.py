from backend.agents.route_builder_agent.route_builder_agent import RouteBuilderAgent

if RouteBuilderAgent.route_builder_agent_exists():
    ROUTE_BUILDER_AGENT = RouteBuilderAgent.get_route_builder_agent()
    print("RouteBuilderAgent wasn't created")
else:
    ROUTE_BUILDER_AGENT = RouteBuilderAgent()
    print("RouteBuilderAgent was created")
