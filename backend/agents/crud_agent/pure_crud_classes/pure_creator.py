# Author: Vodohleb04
from abc import ABC, abstractmethod
from typing import List


class PureCreator(ABC):
    """
    https://sefon.pro/mp3/217283-pantera-10-s/
    Pure abstract class of knowledge base creator. Provides create queries for CRUD agent.
    All read queries for kb provided by child classes of this class.

    All methods work asynchronously.
    """

    @staticmethod
    @abstractmethod
    async def write_user(session, user_login: str):
        """
        Try to write the user to the kb.

        :param session: async session of knowledge base driver
        :param user_login: login of the user to write to the kb. user_login must be unique

        return: Coroutine
        """
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    async def write_note(session, guide_login: str, country_codes: List[int], title: str, categories: List[str]):
        """
        Try to write the note to the kb.

        :param session: async session of the knowledge base.
        :param guide_login: str login of the author of the note (only guide can be the author of the note).
        :param country_codes: List of the codes of the countries, that are mentioned in the note.
        :param title: str unique title of the note.
        :param categories: List[str] categories that are referred by the note.

        return: Coroutine
        """
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    async def write_route_for_note(session, note_title: str, landmarks_names: List[str]):
        """
        Try to write the route, that is connected with note.

        :param session: async session of the knowledge base.
        :param note_title: str title of the note that is connected with the route.
        :param landmarks_names: List[str] names of the landmarks that are included in the route. Order of the landmarks
            names does matter on the order of the route

        return: Coroutine
        """
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    async def write_route_saved_by_user(session, user_login: str, landmarks_names: List[str]):
        """
        Try to write the route, that is saved by the user.

        :param session: async session of the knowledge base.
        :param user_login: str login of the user, who saved the route.
        :param landmarks_names: List[str] names of the landmarks that are included in the route. Order of the landmarks
            names does matter on the order of the route

        return: Coroutine
        """
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    async def write_saved_note_relationship(session, user_login: str, note_title: str):
        """
        Try to write the route, that is connected with note.

        :param session: async session of the knowledge base.
        :param user_login: str login of the user, who saved the route.
        :param note_title: str title of the note that is connected with the route.

        return: Coroutine
        """
        raise NotImplementedError
