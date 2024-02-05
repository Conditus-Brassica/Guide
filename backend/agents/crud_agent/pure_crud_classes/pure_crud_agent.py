#Author: Vodohleb04
"""
PureCrudAgent modul
https://sefon.pro/mp3/474614-sektor-gaza-narkoman/
"""
from typing import Dict
from abc import ABC, abstractmethod


class PureCRUDAgent(ABC):
    """
    Pure abstract class of CRUDAgent. Provides methods for commands from the other agents.
    All work with kb provided by child classes of this class.

    All methods work asynchronously.
    """

    # _single_crud = None

    @classmethod
    @abstractmethod
    async def close(cls) -> None:
        """Method to close the connection to the kb."""
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def get_crud(cls):
        """
        Method to take crud agent object. Returns None in case when crud is not exists.
        :return: None | PureCRUDAgent
        """
        # return cls._single_crud
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def crud_exists(cls) -> bool:
        """Method to check if crud object already exists"""
        raise NotImplementedError
        # if cls._single_crud:
        #     return True
        # else:
        #     return False

    @classmethod
    @abstractmethod
    async def get_categories_of_region(cls, json_params: Dict):
        """
        Returns from kb categories of region with included regions. Finds region by its name.
        Works asynchronously.

        :param json_params: Dict in form {
                "region_name": str,
                "optional_limit": int | None
            }
        :return: Coroutine
            List[
                {
                    "category": {"name": str} | None,
                    "located_at": {"name": str} | None
                }
            ]
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def get_landmarks_in_map_sectors(cls, json_params: Dict):
        """
        Returns from kb landmarks, located in passed map sectors. Finds map sectors by their names.
        Works asynchronously.

        :param json_params: Dict in form {
                "map_sectors_names": List[str],
                "optional_limit": int | None
            }
        :return: Coroutine
            List [
                {
                    "landmark": Dict | None,
                    "sector": Dict | None,
                    "categories_names": List[str] | [] (empty list)
                }
            ], where categories_names are categories of landmark
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def get_landmarks_refers_to_categories(cls, json_params: Dict):
        """
        Returns from kb landmarks, that refers to given categories. Finds categories by their names.
        Works asynchronously.

        :param json_params: Dict in form {
                "categories_names": List[str],
                "optional_limit": int | None
            }
        :return: Coroutine
            List [
                {
                    "landmark": Dict | None,
                    "category": Dict | None
                }
            ]
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def get_landmarks_by_coordinates(cls, json_params: Dict):
        """
        Returns from kb landmarks with given coordinates.
        Works asynchronously.

        :param json_params: Dict in form {
                "coordinates": List [
                    Dict [
                        "latitude": float,
                        "longitude": float
                    ]
                ],
                "optional_limit": int | None
            }
        :return: Coroutine
            List [
                Dict[
                    "landmark": Dict | None,
                    "categories_names": List[str] | [] (empty list)
                ]
            ],  where categories_names are categories of landmark
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def get_landmarks_by_names(cls, json_params: Dict):
        """
        Returns from kb landmarks with given names.
        Works asynchronously.

        :param json_params: Dict in form {
                "landmark_names": List[str],
                "optional_limit": int | None
            }
        :return: Coroutine
            List [
                Dict[
                    "landmark": Dict | None,
                    "categories_names": List[str] | [] (empty list)
                ]
            ],  where categories_names are categories of landmark
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def get_landmarks_of_categories_in_region(cls, json_params: Dict):
        """
        Returns from kb landmarks, located in given region, that refer to given categories.
        Finds region by its name. Finds categories by their names.
        Works asynchronously.

        :param json_params: Dict in form {
                "region_name": str,
                "categories_names": List[str],
                "optional_limit": int | None
            }
        :return: Coroutine
            List [
                Dict[
                    "landmark": Dict | None,
                    "located_at": Dict | None,
                    "category": Dict | None
                ]
            ], where "located_at" is the region, where landmark is located
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def get_landmarks_by_region(cls, json_params: Dict):
        """
        Returns from kb landmarks, located in region. Finds region by its name.
        Works asynchronously.

        :param json_params: Dict in form {
                "region_name": str,
                "optional_limit": int | None
            }
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

    @classmethod
    @abstractmethod
    async def get_recommendations_for_landmark_by_region(cls, json_params: Dict):
        """
            Returns recommended landmarks for given landmark and given user. Finds given landmark by its name and
            coordinates; finds user by his/her login. Returns recommended landmark, categories of recommended landmark,
            distance from current_landmark to recommended landmark in meters, category of the given landmark, node of
            the given User account, "wish" mark, if user left it on recommended landmark (else None), "visited" mark
            with the amount of visits, if user already visited this landmark (else None)/
            Works asynchronously.

            :param json_params: Dict in form {
                "user_login": str,
                "current_latitude": float,
                "current_longitude": float,
                "current_name": str,
                "amount_of_recommendations": int
            }, where current_name is the name of given landmark
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

    @classmethod
    @abstractmethod
    async def get_map_sectors_of_points(cls, json_params: Dict):
        """
            Returns map sectors where given points are located.
            Works asynchronously.

            :param json_params: Dict in form {
                "coordinates_of_points": List[
                    Dict [
                        "longitude": float,
                        "latitude": float
                    ]
                ],
                "optional_limit": int | None
            }
            :return: Coroutine
            List[
                Dict[
                    "of_point": Dict ["longitude": float, "latitude": float]
                    "map_sector": Dict | None,
                ]
            ]
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def get_landmarks_of_categories_in_map_sectors(cls, json_params: Dict):
        """
            Returns landmarks that refer to the given categories and are located in the given map sectors.
            Finds map sectors by names. Finds categories by names.
            Works asynchronously.

            :param json_params: Dict in form {
                "map_sectors_names": List[str],
                "categories_names": List[str],
                "optional_limit": int | None
            }
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

    @classmethod
    @abstractmethod
    async def get_recommendations_by_coordinates_and_categories(cls, json_params: Dict):
        """
            Returns recommended landmarks for given user, given coordinates and given categories. Finds given landmark
            by its name and coordinates; finds user by his/her login. Returns recommended landmark, categories of
            recommended landmark, node of the given User account, "wish" mark, if user left it on recommended landmark
            (else None), "visited" mark with the amount of visits, if user already visited this landmark (else None)/
            Works asynchronously.

            :param json_params: Dict in form {
                "coordinates_of_points": List [
                    Dict [
                        "latitude": float,
                        "longitude": float
                    ]
                ],
                "categories_names": List[str],
                "user_login": str,
                "amount_of_recommendations_for_point": int,
                "amount_of_additional_recommendations_for_point": int,
                "optional_limit": int | None
            }, where current_name is the name of given landmark
            :return: Coroutine
            List[
                Dict[
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
            ]
        """
        raise NotImplementedError
