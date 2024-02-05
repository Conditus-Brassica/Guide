import asyncio

from backend.broker.broker_initializer import BROKER
from backend.agents.route_builder_agent.route_builder_initializer import ROUTE_BUILDER_AGENT


@BROKER.task
async def build_route(route_params):
    """
    Get completed route.
    :param route_params:
     {
     "categories_names":["category1","category2",...],
     "user_login": string,
     "start_end_points":["coordinates":[{"latitude": float, "longitude": float}]]
     }
    :return: tuple(final_route: "coordinates":[{"latitude": float, "longitude": float}, {"latitude": float, "longitude": float}],
        landmarks: {
                     "coordinates_of_points": List [
                        Dict [
                            "latitude": float,
                            "longitude": float
                        ]
                    ],
                    "categories_names": List[str],
                    "user_login": str,
                    "amount_of_recommendations_for_point": int,
                    "maximum_amount_of_recommendations": int,
                    "optional_limit": int | None,
                }
    )
    """
    return await ROUTE_BUILDER_AGENT.build_route(route_params)
