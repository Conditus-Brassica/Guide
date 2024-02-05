import asyncio

import openrouteservice as ors

from typing import Dict
from aiologger.loggers.json import JsonLogger

from backend.agents.routing_agent import api_key
from backend.agents.routing_agent.pure_routing_agent import PureRoutingAgent

logger = JsonLogger.with_default_handlers(
    level="DEBUG",
    serializer_kwargs={'ensure_ascii': False},
)


class RoutingAgent(PureRoutingAgent):
    """
    Agent for finding route points.
    Usage: when you need to create optimized
    route between several points.

    Uses api_key in api_key.py
    """

    __single_routing_agent = None

    @classmethod
    def get_routing_agent(cls):
        """
        Method to take route generating agent object. Returns None in case when route generating agent is not exists.
        :return: None | PureRoutingAgent
        """
        return cls.__single_routing_agent

    @classmethod
    def routing_agent_exists(cls) -> bool:
        """
        Method to check if route generating agent exists.
        :return: Boolean
        """
        if cls.__single_routing_agent:
            return True
        else:
            return False

    def __init__(self, client: ors.Client):
        if not self.__single_routing_agent:
            self._client_ = client
            self._landmarks = []
            self.__single_routing_agent = self
        else:
            raise RuntimeError("Unexpected behaviour, this class can have only one instance")

    async def get_optimized_route(self, landmark_list: Dict):
        """
        Method finds all optimized route points for provided points.
        :param landmark_list: ["coordinates": [latitude: float, longitude: float], ...]
        :return: route points list: {"coordinates": [{"latitude": float, "longitude": float}, ...]}
        """
        for i in landmark_list['coordinates']:
            self._landmarks.append([i['latitude'], i['longitude']])

        self._landmarks = self._reverse_coordinates(self._landmarks)

        route = await self._create_optimized_route()

        route = self._reverse_coordinates(route)

        self._landmarks = []
        return self._coordinates_wrap(route)

    async def get_optimized_route_main_points(self, landmark_list: Dict):
        """
        Method finds all optimized route points for provided points.
        Return one point per 30 km.
        :param landmark_list: {"coordinates": [{"latitude": float, "longitude": float}, ...]}
        :return: route points list: {"coordinates": [{"latitude": float, "longitude": float}, ...]}
        """
        for i in landmark_list['coordinates']:
            self._landmarks.append([i['latitude'], i['longitude']])

        await logger.debug(self._landmarks)

        self._landmarks = self._reverse_coordinates(self._landmarks)

        await logger.debug(self._landmarks)

        route = await self._create_optimized_route()

        main_points = []
        k = 0
        main_points.append(route[0])
        for i in route:
            if k == 260:
                main_points.append(i)  # 260 - points every 60 km of route
                k = 0
            k += 1

        main_points.append(route[-1])

        if len(route) < 260:
            main_points.append(route[0])
            main_points.append(route[-1])

        main_points = self._reverse_coordinates(main_points)
        await logger.debug(f"main points arrr {main_points}")
        self._landmarks = []
        return self._coordinates_wrap(main_points)

    @staticmethod
    def _reverse_coordinates(coordinates_list: list):
        """
        Method revere coordinates because of osm (longitude, latitude),
        but normally it should be (latitude, longitude).
        :param coordinates_list:
        :return: list of reversed coordinates
        """
        coordinates_list = [list(reversed(coord)) for coord in coordinates_list]

        return coordinates_list

    async def _create_optimized_route(self):
        """
        Interaction with OpenRoutService API
        :return:
        """
        while True:
            try:
                route = self._client_.directions(
                    coordinates=self._landmarks,
                    profile='driving-car',
                    format='geojson',
                    validate=False,
                    optimize_waypoints=True,
                    radiuses=[-1 for _ in range(len(self._landmarks))]
                )
                break
            except TypeError:
                await logger.error("ORS route proplems")

        # await asyncio.sleep(5)
        return route['features'][0]['geometry']['coordinates']

    @staticmethod
    def _coordinates_wrap(landmark_list: list):
        """
        Create dictionary from list.
        """
        coordinates_dictionary = dict()

        lst = []
        for i in landmark_list:
            lst.append({"latitude": i[0], "longitude": i[1]})

        coordinates_dictionary['coordinates'] = lst

        return coordinates_dictionary

# async def main():
#     a = RoutingAgent(ors.Client(key=api_key.__key__))
#     res = asyncio.create_task(
#         a.get_optimized_route([[52.19797604067352, 24.43870667812846], [54.490638791728756, 30.4701524897013],
#                                [53.93429515309309, 27.113365683855704], [53.8602548114542, 30.38039883179099],
#                                [54.490638791728756, 25.85681447311136]]))
#
#     print(await res)
#
#
# asyncio.run(main())

# async def main():
#     a = RoutingAgent()
#     res = asyncio.create_task(a.get_optimized_route_main_points(
#         [[52.19797604067352, 24.43870667812846], [54.490638791728756, 30.4701524897013],
#          [53.93429515309309, 27.113365683855704], [53.8602548114542, 30.38039883179099],
#          [54.490638791728756, 25.85681447311136]]))
#     print(len(await res))
#
#
# asyncio.run(main())
