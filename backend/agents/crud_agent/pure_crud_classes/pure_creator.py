# Author: Vodohleb04
from abc import ABC, abstractmethod
from typing import List, Dict


class PureCreator(ABC):
    """
    https://sefon.pro/mp3/217283-pantera-10-s/
    Pure abstract class of knowledge base creator. Provides create queries for CRUD agent.
    All read queries for kb provided by child classes of this class.

    All methods work asynchronously.
    """

    @staticmethod
    @abstractmethod
    async def write_user(session, user_login: str) -> bool:
        """
        Try to write the user to the kb.

        :param session: async session of knowledge base driver
        :param user_login: login of the user to write to the kb. user_login must be unique

        return: Coroutine
        """
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    async def write_note(
            session, guide_login: str, country_names: List[int], title: str, category_names: List[str]
    ) -> bool:
        """
        Try to write the note to the kb.

        :param session: async session of the knowledge base.
        :param guide_login: str login of the author of the note (only guide can be the author of the note).
        :param country_names: List of the names of the countries, that are mentioned in the note.
        :param title: str unique title of the note.
        :param category_names: List[str] categories that are referred by the note.

        return: Coroutine
        """
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    async def write_route_for_note(
            session, note_title: str, landmark_info_position_dicts: List[Dict[str, str | int | float]]
    ) -> bool:
        """
        Try to write the route, that is connected with note.

        :param session: async session of the knowledge base.
        :param note_title: str title of the note that is connected with the route.
        :param landmark_info_position_dicts: List [
                Dict[
                    "name": <landmark_name>,
                    "position": <int_position_in_route>,
                    "latitude": <float_landmark_latitude>,
                    "longitude": <float_landmark_longitude>
                ]
            ]
            <int_position_in_route> starts from 0
            pairs of name of the landmark and its position in the route that are included in the route.

        return: Coroutine
        """
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    async def write_route_saved_by_user(
            session, user_login: str, landmark_info_position_dicts: List[Dict[str, str | int | float]]
    ) -> bool:
        """
        Try to write the route, that is saved by the user.

        :param session: async session of the knowledge base.
        :param user_login: str login of the user, who saved the route.
        :param landmark_info_position_dicts: List [
                Dict[
                    "name": <landmark_name>,
                    "position": <int_position_in_route>,
                    "latitude": <float_landmark_latitude>,
                    "longitude": <float_landmark_longitude>
                ]
            ]
            <int_position_in_route> starts from 0
            pairs of name of the landmark and its position in the route that are included in the route.

        return: Coroutine
        """
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    async def write_saved_relationship_for_existing_route(session, user_login: str, index_id: int) -> bool:
        """
        Try to write the route, that is connected with note.

        :param session: async session of the knowledge base.
        :param user_login: str login of the user, who saved the route.
        :param index_id: int unique id of route.

        return: Coroutine
        """
        raise NotImplementedError
