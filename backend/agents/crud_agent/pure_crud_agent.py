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

    # Read queries
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
    async def get_landmarks_by_coordinates_and_name(cls, json_params: Dict):
        """
        Returns from kb landmarks with given coordinates and name.
        Works asynchronously.

        :param json_params: Dict in form {
                "coordinates_name_list": List [
                    Dict [
                        "latitude": float,
                        "longitude": float,
                        "name": str
                    ]
                ],
                "optional_limit": int | None
            }
        :return: Coroutine
            List [
                Dict[
                    "landmark": Dict | None,
                    "categories_names": List[str] | [] (empty list),
                    "in_regions": List["str"] | []
                ]
            ],  where categories_names are categories of landmark, in_regions - names of regions, where landmark is located
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def get_landmarks_by_name_list(cls, json_params: Dict):
        """
        Returns from kb landmarks with given names.
        Works asynchronously.

        :param json_params: Dict in form {
                "landmark_names": List[str]
            }
        :return: Coroutine
            List [
                Dict[
                    "landmark": Dict | None,
                    "categories_names": List[str] | [] (empty list),
                    "in_regions": List["str"] | []
                ]
            ],  where categories_names are categories of landmark, in_regions - names of regions, where landmark is located
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def get_landmarks_by_name(cls, json_params: Dict):
        """
        Returns from kb landmarks with the names that starts with the given name.
        Works asynchronously.

        :param json_params: Dict in form {
                "landmark_name": str,
                "limit": int
            }
        :return: Coroutine
            List [
                Dict[
                    "landmark": Dict | None,
                    "categories_names": List[str] | [] (empty list),
                    "in_regions": List["str"] | []
                ]
            ],  where categories_names are categories of landmark, in_regions - names of regions, where landmark is located
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
    async def get_map_sectors_structure_of_region(cls, json_params: Dict):
        """
            Returns map sectors structure of the given region.
            Works asynchronously.


            :param json_params: Dict in form {
                "region_name": str
            }
            :return: Coroutine
            List[
                Dict[
                    "map_sector_name": str | None,
                    "tl_latitude": float | None,
                    "tl_longitude": float | None,
                    "br_latitude": float | None,
                    "br_longitude: float | None"
                    "neighbour_map_sector_names": List[str] | (empty list)
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
    async def get_route_landmarks_by_index_id(cls, json_params: Dict):
        """
            Returns list landmarks of the route with the given index_id (unique id of route). Landmarks are returned in
            the order that corresponds to the order of appearance of landmarks in the route.
            Works asynchronously.

            :param json_params: Dict in form {
                "index_id": int
            }
            :return: Coroutine
            List[
                Dict[
                    "landmark": Dict | None,
                ]
            ]
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def get_routes_saved_by_user(cls, json_params: Dict):
        """
            Returns routes with its landmarks (returns landmarks in the order that corresponds to the order of
            appearance of landmarks in the route).
            Works asynchronously.

            :param json_params: Dict in form {
                "user_login": str
            }
            :return: Coroutine
            List[
                Dict[
                    "route": Dict | None,
                    "route_landmarks": List[Dict | None] | None
                ]
            ]
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def get_range_of_routes_saved_by_user(cls, json_params: Dict):
        """
            Returns range of routes with its landmarks (returns landmarks in the order that corresponds to the order of
            appearance of landmarks in the route). Range looks like (skip, skip + limit].
            skip=0 return result from the very beginning.
            Works asynchronously.

            :param json_params: Dict in form {
                "user_login": str,
                "skip": int,
                "limit": int
            }
            :return: Coroutine
            List[
                Dict[
                    "route": Dict | None,
                    "route_landmarks": List[Dict | None] | None
                ]
            ]
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def get_note_by_title(cls, json_params: Dict):
        """
            Returns note with its routes (returns routes with theirs landmarks in the order that corresponds to the
            order of appearance of landmarks in the route) by title of the note.
            Works asynchronously.

            :param json_params: Dict in form {
                "note_title": str
            }
            :return: Coroutine
            List[
                Dict[
                    "note": Dict | None,
                    "route": Dict | None,
                    "route_landmarks": List[Dict | None] | None,
                    "note_category_names": List[str | None] | None
                ]
            ]
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def get_notes_in_range(cls, json_params: Dict):
        """
            Returns range of notes of all categories with their routes (with landmarks in the order that corresponds to
            the order of appearance of landmarks in the route). Range looks like (skip, skip + limit].
            Works asynchronously.

            :param json_params: Dict in form {
                "skip": int
                "limit": int
            }
            :return: Coroutine
            List[
                Dict[
                    "note": Dict | None,
                    "route": Dict | None,
                    "route_landmarks": List[Dict | None] | None,
                    "note_category_names": List[str | None] | None
                ]
            ]
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def get_notes_of_categories_in_range(cls, json_params: Dict):
        """
            Returns range of notes of the given categories with their routes (with landmarks in the order that
            corresponds to the order of appearance of landmarks in the route). Range looks like (skip, skip + limit].
            Works asynchronously.

            :param json_params: Dict in form {
                "note_categories_names": List[str]
                "skip": int
                "limit": int
            }
            :return: Coroutine
            List[
                Dict[
                    "note": Dict | None,
                    "route": Dict | None,
                    "route_landmarks": List[Dict | None] | None,
                    "note_category_names": List[str | None] | None
                ]
            ]
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def get_recommendations_by_coordinates(cls, json_params: Dict):
        """
            Returns recommended landmarks for given coordinates. Returns recommended landmark.
            Works asynchronously.

            :param json_params: Dict in form {
                "coordinates_of_points": List [
                    Dict [
                        "latitude": float,
                        "longitude": float
                    ]
                ],
                "limit": int
            },
            :return: Coroutine
            List[
                Dict[
                    Dict[
                        "recommendation": Dict | None,
                    ]
                ]
            ]
        """
        raise NotImplementedError

    # Write queries

    @classmethod
    @abstractmethod
    async def put_user(cls, json_params: Dict):
        """
            Puts user to kb.
            Works asynchronously.

            :param json_params: Dict in form {"user_login": str}
            :return: Coroutine bool True if everything is fine, False otherwise
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def put_note(cls, json_params: Dict):
        """
            Puts note, created by guide to kb.
            Works asynchronously.

            :param json_params: Dict in form {
                "guide_login": str,
                "country_names": List[str],
                "note_title": str,
                "note_category_names": List[str]
            }
            :return: Coroutine bool True if everything is fine, False otherwise
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def put_route_for_note(cls, json_params: Dict):
        """
            Puts route corresponding to the given note to kb.
            Works asynchronously.

            :param json_params: Dict in form {
                "note_title": str,
                "landmark_info_position_dicts": List[
                    Dict [
                        "name": str,
                        "position": int,
                        "latitude": float,
                        "longitude": float
                    ]
                ], where name is name of landmark and position is position in route of corresponding landmark (starts from 0)
            }

            :return: Coroutine bool True if everything is fine, False otherwise
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def put_route_saved_by_user(cls, json_params: Dict):
        """
            Puts route saved by user to kb.
            Works asynchronously.

            :param json_params: Dict in form {
                "user_login": str,
                "landmark_info_position_dicts": List[
                    Dict [
                        "name": str,
                        "position": int,
                        "latitude": float,
                        "longitude": float
                    ]
                ], where name is name of landmark and position is position in route of corresponding landmark (starts from 0)
            }

            :return: Coroutine bool True if everything is fine, False otherwise
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    async def put_saved_relationship_for_existing_route(cls, json_params: Dict):
        """
            Marks route with the given index_id as saved by user.
            Works asynchronously.

            :param json_params: Dict in form {
                "user_login": str,
                "index_id": int
            }

            :return: Coroutine bool True if everything is fine, False otherwise
        """
        raise NotImplementedError
