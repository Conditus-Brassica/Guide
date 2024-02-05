import asyncio

from backend.agents.route_builder_agent.pure_route_builder_agent import PureRouteBuilder
from backend.broker.abstract_agents_broker import AbstractAgentsBroker
from backend.broker.agents_tasks.recommendations_agent_tasks import \
    find_recommendations_for_coordinates_and_categories_task
from backend.broker.agents_tasks.route_generating_tasks import get_optimized_route_task, \
    get_optimized_route_main_points_task


class RouteBuilderAgent(PureRouteBuilder):
    _single_route_builder = None

    @classmethod
    def get_route_builder_agent(cls):
        return cls._single_route_builder

    @classmethod
    def route_builder_agent_exists(cls) -> bool:
        if cls._single_route_builder:
            return True
        else:
            return False

    def __init__(self):
        """
        Init method for RouteBuilderAgent.
        """
        if not self._single_route_builder:
            self._single_route_builder = self
        else:
            raise RuntimeError("Unexpected behaviour, this class can have only one instance")

    async def build_route(self, route_params):
        """
        Get completed route.
        :param route_params:
         {
         "categories_names":["category1","category2",...],
         "user_login": string,
         "start_end_points":["coordinates":[{"latitude": float, "longitude": float}]]
         }
        :return: tuple(final_route: "coordinates":[
                                                    {"latitude": float, "longitude": float},
                                                     {"latitude": float, "longitude": float}
                                                    ],
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
        pre_route_task = asyncio.create_task(
            AbstractAgentsBroker.call_agent_task(get_optimized_route_main_points_task, route_params['start_end_points'])
        )

        pre_route = await pre_route_task
        pre_route = pre_route.return_value
        param_dict = dict()

        param_dict['coordinates_of_points'] = pre_route['coordinates']
        param_dict['categories_names'] = route_params['categories_names']
        param_dict['user_login'] = route_params['user_login']
        param_dict['maximum_amount_of_recommendations'] = int(len(pre_route['coordinates']) * 4)
        param_dict['optional_limit'] = int(len(pre_route['coordinates']) * 6)
        param_dict['amount_of_recommendations_for_point'] = 3

        landmarks_task = asyncio.create_task(
            AbstractAgentsBroker.call_agent_task(find_recommendations_for_coordinates_and_categories_task, param_dict)
        )
        landmarks = await landmarks_task
        landmarks = landmarks.return_value

        print("Penis ", landmarks)

        formatted_landmarks = self.__format_landmarks(landmarks)

        formatted_landmarks['coordinates'].append(
            {"latitude": route_params['start_end_points']['coordinates'][-1]['latitude'],
             "longitude": route_params['start_end_points']['coordinates'][-1]['longitude']})

        formatted_landmarks['coordinates'].insert(0, {
            "latitude": route_params['start_end_points']['coordinates'][0]['latitude'],
            "longitude": route_params['start_end_points']['coordinates'][0]['longitude']})

        final_route_task = (
            AbstractAgentsBroker.call_agent_task(get_optimized_route_task, formatted_landmarks)
        )

        final_route = await final_route_task

        final_route = final_route.return_value

        return final_route, landmarks

    @staticmethod
    def __format_landmarks(landmarks):
        """
        Formats landmarks dict
        :param landmarks: [{"recommendation": {"latitude": float, "longitude": float, "name": str} | None}, ...]
        :return: {"coordinates":[{"latitude": float}, "longitude": float], ...}
        """
        formatted = {}
        coordinates = []
        for i in landmarks:
            curr_coordinates = dict()
            if i["recommendation"] is not None:
                curr_coordinates['latitude'] = i['recommendation']['latitude']
                curr_coordinates['longitude'] = i['recommendation']['longitude']
                coordinates.append(curr_coordinates)

        formatted['coordinates'] = coordinates

        return dict(formatted)
