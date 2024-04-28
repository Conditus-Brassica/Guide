# Author: Vodohleb04
from typing import List
from aiologger.loggers.json import JsonLogger
from neo4j import AsyncSession
from backend.agents.crud_agent.pure_crud_classes.pure_creator import PureCreator


logger = JsonLogger.with_default_handlers(
    level="INFO",
    serializer_kwargs={'ensure_ascii': False},
)


class Creator(PureCreator):
    """
    https://sefon.pro/mp3/217283-pantera-10-s/
    Creator part of CRUDAgent. All write queries to knowledgebase are located here.
    Implements PureCreator.
    All methods work asynchronously.
    """

    @staticmethod
    async def write_user(session, user_login: str) -> bool:
        # TODO
        query = """
            OPTIONAL MATCH (userAccount: UserAccount WHERE userAccount.login STARTS WITH $user_login)
            WITH userAccount
                ORDER BY userAccount.login ASC
                LIMIT 1
            
            CALL apoc.do.when(
                userAccount IS null,
                "
                    CREATE (newUserAccount: UserAccount {login: $user_login})
                    RETURN True
                ",
                "
                    RETURN False
                ",
                {user_login: $user_login}
                ) YIELD value AS newUserAccount
            RETURN newUserAccount
        """

    @staticmethod
    async def write_note(
            session, guide_login: str, country_codes: List[int], title: str, categories: List[str]
    ) -> bool:
        pass

    @staticmethod
    async def write_route_for_note(session, note_title: str, landmarks_names: List[str]) -> bool:
        pass

    @staticmethod
    async def write_route_saved_by_user(session, user_login: str, landmarks_names: List[str]) -> bool:
        pass

    @staticmethod
    async def write_saved_note_relationship(session, user_login: str, note_title: str) -> bool:
        pass


