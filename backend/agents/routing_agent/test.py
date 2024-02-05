import asyncio

from backend.broker.abstract_agents_broker import AbstractAgentsBroker
from backend.broker.agents_tasks.route_generating_tasks import get_optimized_route_main_points_task, \
    get_optimized_route_task

import folium

#  "start_end_points":["coordinates":[{"latitude": float, "longitude": float}]]

m = folium.Map(location=[53.85125284688566, 27.567630112777685], zoom_start=7)


async def main():
    coord = {
        "coordinates": [
            {
                "latitude": 53.13069674685768,
                "longitude": 25.967160840243956
            },
            {
                "latitude": 53.871045,
                "longitude": 30.299173
            }
        ]
    }

    pre_route_task = asyncio.create_task(
        AbstractAgentsBroker.call_agent_task(get_optimized_route_main_points_task, coord)
    )

    route_1 = await pre_route_task
    route_1 = route_1.return_value

    route_list = list()

    print(route_1)
    for i in route_1["coordinates"]:
        route_list.append([i['latitude'], i['longitude']])

    folium.PolyLine(
        locations=route_list,
        color="blue",
        weight=5
    ).add_to(m)

    coord = {
        "coordinates": [  # Kobrin +-
            {
                "latitude": 53.13069674685768,
                "longitude": 25.967160840243956
            },
            {  # Baranavichy
                "latitude": 53.133729,
                "longitude": 26.048505
            },
            {  # Mozir
                "latitude": 52.0181377384975,
                "longitude": 29.24470341900513
            },
            {  # Svetlagorsk
                "latitude": 52.63047029088026,
                "longitude": 29.731127278387117
            },
            {  # Mogilev
                "latitude": 53.871045,
                "longitude": 30.299173
            }
        ]
    }

    route_list = []

    route_task = asyncio.create_task(
        AbstractAgentsBroker.call_agent_task(get_optimized_route_task, coord)
    )

    route_2 = await route_task

    route_2 = route_2.return_value

    print("route 2", route_2, "\n\n")

    for i in route_2["coordinates"]:
        route_list.append([i['latitude'], i['longitude']])

    folium.PolyLine(
        locations=route_list,
        color="red",
        weight=5
    ).add_to(m)

    m.show_in_browser()


if __name__ == "__main__":
    asyncio.run(main())
