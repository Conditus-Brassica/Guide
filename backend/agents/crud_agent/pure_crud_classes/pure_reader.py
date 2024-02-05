#Author: Vodohleb04
from abc import ABC, abstractmethod
from typing import List, Dict


class PureReader(ABC):
    """
        Pure abstract class of knowledge base reader. Provides queries for CRUD agent.
        All read queries for kb provided by child classes of this class.

        All methods work asynchronously.
    """

    @staticmethod
    @abstractmethod
    async def read_categories_of_region(session, region_name: str, optional_limit: int = None):
        """
        Returns from kb categories of region with included regions. Finds region by its name.
        Works asynchronously.

        :param session: async session of knowledge base driver
        :param region_name: str name of the given region
        :param optional_limit: int | None the maximum number of returning records (not specified if None is given)
        :return: Coroutine
            List[
                Dict["category": Dict]
            ]
        """
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    async def read_landmarks_in_map_sectors(session, map_sectors_names: List[str], optional_limit: int = None):
        """
        Returns from kb landmarks, located in passed map sectors. Finds map sectors by their names.
        Works asynchronously.

        :param session: async session of knowledge base driver
        :param map_sectors_names: List[str] names of map sectors, where target landmarks are located
        :param optional_limit: int | None the maximum number of returning records (not specified if None is given)
        :return: Coroutine
            List [
                {
                    "landmark": Dict | None,
                    "sector": Dict | None,
                    "categories_names": List[str] | [] (empty list)
                }
            ],  where categories_names are categories of landmark
        """
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    async def read_landmarks_by_coordinates(session, coordinates: List[Dict[str, float]], optional_limit: int = None):
        """
        Returns from kb landmarks with given coordinates.
        Works asynchronously.

        :param session: async session of knowledge base driver\
        :param coordinates:
            List[
                Dict [
                    "latitude": float,
                    "longitude": float
                ]
            ] coordinates of target landmarks
        :param optional_limit: int | None the maximum number of returning records (not specified if None is given)
        :return: Coroutine
            List [
                Dict[
                    "landmark": Dict | None,
                    "categories_names": List[str] | [] (empty list)
                ]
            ], where categories_names are categories of landmark
        """
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    async def read_landmarks_refers_to_categories(session, categories_names: List[str], optional_limit: int = None):
        """
        Returns from kb landmarks, that refers to given categories. Finds categories by their names
        Works asynchronously.

        :param session: async session of knowledge base driver
        :param categories_names: List[str] names of categories, that are referred by target landmarks
        :param optional_limit: int | None the maximum number of returning records (not specified if None is given)
        :return: Coroutine
            List [
                Dict["landmark": Dict, "category": Dict]
            ]
        """
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    async def read_landmarks_by_names(session, landmark_names: List[str], optional_limit: int = None):
        """
        Returns from kb landmarks with given names.
        Works asynchronously.

        :param session: async session of knowledge base driver
        :param landmark_names: List[str] names of target landmarks
        :param optional_limit: int | None the maximum number of returning records (not specified if None is given)
        :return: Coroutine
            List [
                Dict[
                    "landmark": Dict | None,
                    "categories_names": List[str] | [] (empty list)
                ]
            ], where categories_names are categories of landmark
        """
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    async def read_landmarks_of_categories_in_region(
            session, region_name: str, categories_names: List[str], optional_limit: int  = None
    ):
        """
        Returns from kb landmarks, located in given region, that refer to given categories.
        Finds region by its name. Finds categories by their names.
        Works asynchronously.

        :param session: async session of knowledge base driver
        :param region_name: str name of region where target landmarks are located or region that include such region
        :param categories_names: List[str] names of categories of target landmarks
        :param optional_limit: int | None the maximum number of returning records (not specified if None is given)
        :return: Coroutine
            List [
                Dict[
                    "landmark": Dict,
                    "located_at": Dict,
                    "category": Dict
                ]
            ], where "located_at" is the region, where landmark is located
        """
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    async def read_recommendations_for_landmark_by_region(
            session,
            user_login: str,
            current_latitude: float,
            current_longitude: float,
            current_name: str,
            amount_of_recommendations: int
    ):
        """
            Returns recommended landmarks for given landmark and given user. Finds given landmark by its name and
            coordinates; finds user by his/her login. Returns recommended landmark, categories of recommended landmark,
            distance from current_landmark to recommended landmark in meters, category of the given landmark, node of
            the given User account, "wish" mark, if user left it on recommended landmark (else None), "visited" mark
            with the amount of visits, if user already visited this landmark (else None)/
            Works asynchronously.

            :param session: async session of knowledge base driver
            :param user_login: str login of user for whom recommendations will be found
            :param current_latitude: float latitude of given landmark
            :param current_longitude: float longitude of given landmark
            :param current_name: str name of given landmark
            :param amount_of_recommendations: int max amount of recommended landmarks
            :return: Coroutine
            List[
                Dict[
                    "recommendation": Dict | None,
                    "main_categories_names": List[str] | [] (empty list),
                    "subcategories_names": List[str] | [] (empty list),
                    "distance": float | None,
                    "wish_to_visit": bool | None,
                    "visited_amount": int | None
                ]
            ]
        """
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    async def read_landmarks_by_region(session, region_name: str, optional_limit: int = None):
        """
        Returns from kb landmarks, located in region. Finds region by its name.
        Works asynchronously.

        :param session: async session of knowledge base driver
        :param region_name: str name of region where target landmarks are located or region that include such region
        :param optional_limit: int | None the maximum number of returning records (not specified if None is given)
        :return: Coroutine
            List[
                Dict[
                    "landmark": Dict | None,
                    "located_at": Dict | None,
                    "categories_names": List[str] | [] (empty list)
                ]
            ],  where "located_at" is the region, where landmark is located, categories_names are categories of landmark
        """
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    async def read_map_sectors_of_points(
            session, coordinates_of_points: List[Dict[str, float]], optional_limit: int = None
    ):
        """
        Returns from kb map sectors where given points are located.
        Works asynchronously.

        :param session: async session of knowledge base driver
        :param coordinates_of_points: List[Dict]. Dict represent point for which the map sector is defining.
        Must include latitude and longitude.
        :param optional_limit: int | None the maximum number of returning records (not specified if None is given)
        :return: Coroutine
            List[
                Dict[
                    "landmark": Dict,
                    "located_at": Dict
                ]
            ], where "located_at" is the region, where landmark is located
        """
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    async def read_landmarks_of_categories_in_map_sectors(
            session, map_sectors_names: List[str], categories_names: List[str], optional_limit: int = None
    ):
        """
        Returns from kb landmarks, that\'re located in the given map sectors and refer to the given categories.
        Works asynchronously.

        :param session: async session of knowledge base driver
        :param map_sectors_names: List[str] names of map sectors where landmarks are located.
        :param categories_names: List[str] names of categories that are referred by landmarks
        :param optional_limit: int | None the maximum number of returning records (not specified if None is given)
        :return: Coroutine
            List[
                Dict[
                    "landmark": Dict | None,
                    "map_sector": Dict | None,
                    "category": Dict | None
                ]
            ]
        """
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    async def read_recommendations_by_coordinates_and_categories(
            session,
            coordinates_of_points: List[Dict[str, float]],
            categories_names: List[str],
            user_login: str,
            amount_of_recommendations_for_point: int,
            amount_of_additional_recommendations_for_point: int,
            optional_limit: int | None
    ):
        """
            Returns recommended landmarks for given user, given coordinates and given categories. Finds given landmark
            by its name and coordinates; finds user by his/her login. Returns recommended landmark, categories of
            recommended landmark, node of the given User account, "wish" mark, if user left it on recommended landmark
            (else None), "visited" mark with the amount of visits, if user already visited this landmark (else None)/
            Works asynchronously.

            :param session: async session of knowledge base driver
            :param coordinates_of_points: List[
                Dict [
                    "latitude": float,
                    "longitude": float
                ]
            ] coordinates of given points
            :param categories_names: List[str] names of categories of target landmarks
            :param user_login: str login of user for whom recommendations will be found
            :param amount_of_recommendations_for_point: int max amount of recommended landmarks for every point
            :param amount_of_additional_recommendations_for_point: int max amount of recommendations from the neighbour
                or included regions for recommendation in this map sector (recommendations by region amount)
            :param optional_limit: int | None max amount of recommended landmarks
            :return: Coroutine
            List[
                Dict[
                    "recommendation": Dict | None,
                    "main_categories_names": List[str] | [] (empty list),
                    "subcategories_names": List[str] | [] (empty list),
                    "distance": float | None,
                    "user_account": Dict | None,
                    "wish_to_visit": bool | None,
                    "visited_amount": int | None,
                    "additional_recommendations": List[
                        Dict [
                            "recommendation": Dict | None,
                            "distance": float | None,
                            "main_categories_names": List[str] | [] (empty list),
                            "subcategories_names": List[str] | [] (empty list),
                            "wish_to_visit": bool | None,
                            "visited_amount": int | None
                        ]
                    ]
                ]
            ]
        """
        raise NotImplementedError
