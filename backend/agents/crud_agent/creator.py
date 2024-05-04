# Author: Vodohleb04
from typing import List, Dict

import neo4j
from aiologger.loggers.json import JsonLogger
from neo4j import AsyncSession, exceptions
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
    async def _write_user(tx, user_login: str) -> bool:
        result = await tx.run(
            """
            CREATE (newUserAccount: UserAccount {login: $user_login})
            """,
            user_login=user_login
        )
        result_summary = await (result.consume())
        counters = result_summary.counters
        if counters.nodes_created != 1:
            raise exceptions.Neo4jError("Unexpected behaviour: No nodes were created or to much nodes were created.")

    @staticmethod
    async def write_user(session: AsyncSession, user_login: str) -> bool:
        try:
            result = await session.execute_write(Creator._write_user, user_login)
            await logger.debug(f"method:\twrite_user,\nresult:\t{result}")
            return True
        except Exception as e:
            await logger.error(f"Error while writing user account, args: {e.args[0]}")
            return False

    @staticmethod
    async def _write_note(tx, guide_login: str, country_names: List[str], title, category_names):
        result = await tx.run(
            """
            MATCH (guideAccount: UserAccount&GuideAccount WHERE guideAccount.login STARTS WITH $guide_login)
            WITH guideAccount
                ORDER BY guideAccount.login ASC
                LIMIT 1
                
            CREATE (guideAccount)-[:AUTHOR]->(note: Note {title: $title, last_update: datetime(), id_code: guideAccount.last_note_id_code + 1})
            
            WITH guideAccount, note
    
            WITH 
                note,
                guideAccount,
                COLLECT {
                    UNWIND $country_names AS country_name
                        CALL {
                            WITH country_name
                            CALL db.index.fulltext.queryNodes('region_name_fulltext_index', country_name)
                                YIELD score, node AS region
                            RETURN region
                                ORDER BY score DESC
                                LIMIT 1
                        }
                        RETURN 'notes/' + toString(region.id_code) + '/' + toString(guideAccount.id_code) + '/' + toString(guideAccount.last_note_id_code + 1) + '/'
                } AS path_list
            
            SET note.path_list = path_list
            SET guideAccount.last_note_id_code = guideAccount.last_note_id_code + 1 
            WITH note
                    
            UNWIND $category_names AS note_category_name
                CALL {
                    WITH note_category_name
                    CALL db.index.fulltext.queryNodes('note_category_name_fulltext_index', note_category_name)
                        YIELD score, node AS noteCategory
                    RETURN noteCategory
                        ORDER BY score DESC
                        LIMIT 1
                }
                    
                CREATE (note)-[:NOTE_REFERS]->(noteCategory)
            RETURN DISTINCT size(note.path_list) AS path_list_size
            """,
            guide_login=guide_login, country_names=country_names, title=title, category_names=category_names
        )
        path_list_size = 0
        async for record in result:
            path_list_size = record.data("path_list_size")["path_list_size"]
        result_summary = await (result.consume())
        counters = result_summary.counters
        if counters.nodes_created != 1:
            raise exceptions.Neo4jError("Unexpected behaviour: No nodes were created or to much nodes were created.")
        if counters.relationships_created != len(category_names) + 1:  # Author -> Note and Note -> its categories
            raise exceptions.Neo4jError("Unexpected behaviour: Wrong amount of relationships, that were created.")
        if path_list_size != len(country_names):
            raise exceptions.Neo4jError(
                "Unexpected behaviour: Wrong amount of paths were added to node. Probably some of the given countries aren\'t exist"
            )

    @staticmethod
    async def write_note(
            session: AsyncSession, guide_login: str, country_names: List[str], title: str, category_names: List[str]
    ) -> bool:
        try:
            result = await session.execute_write(
                Creator._write_note, guide_login, country_names, title, category_names
            )
            await logger.debug(f"method:\twrite_note,\nresult:\t{result}")
            return True
        except Exception as e:
            await logger.error(f"Error while writing note, args: {e.args[0]}")
            return False

    @staticmethod
    async def _write_route_for_note(tx, note_title: str, landmarks_name_position_pairs: List[Dict[str, str | int]]):
        result = await tx.run(
            """
            CALL db.index.fulltext.queryNodes('note_title_fulltext_index', $note_title)
                YIELD score, node AS note
            WITH note
                ORDER BY score DESC
                LIMIT 1
            
            OPTIONAL MATCH (route: Route)
            WITH note, route
                ORDER BY route.index_id DESC
                LIMIT 1
            WITH 
                note,
                CASE 
                    WHEN route IS null THEN 0
                    WHEN route.index_id IS null THEN 0
                    ELSE route.index_id
                END AS last_route_index_id
            
            CREATE (route: Route {index_id: last_route_index_id + 1})<-[:ROUTE_FOR_NOTE]-(note)
            WITH route
            
            UNWIND $landmarks_name_position_pairs AS landmark_name_position_pair
                CALL {
                    WITH landmark_name_position_pair
                    CALL db.index.fulltext.queryNodes('landmark_name_fulltext_index', landmark_name_position_pair.name)
                        YIELD score, node AS landmark
                    RETURN landmark
                        ORDER BY score DESC
                        LIMIT 1
                }
                CREATE (route)-[:PART_OF_ROUTE {position: landmark_name_position_pair.position}]->(landmark)
            """,
            note_title=note_title,
            landmarks_name_position_pairs=landmarks_name_position_pairs
        )
        result_summary = await (result.consume())
        counters = result_summary.counters

        if counters.nodes_created != 1:
            raise exceptions.Neo4jError("Unexpected behaviour: No nodes were created or to much nodes were created.")
        if counters.relationships_created != len(landmarks_name_position_pairs) + 1:  # Note -> Route and Route -> its Landmarks
            raise exceptions.Neo4jError("Unexpected behaviour: Wrong amount of relationships, that were created.")
        if counters.properties_set != len(landmarks_name_position_pairs) + 1:  # index_id and position
            raise exceptions.Neo4jError(
                "Unexpected behaviour: Wrong amount properties that were set. Probably some of the given countries aren\'t exist"
            )

    @staticmethod
    async def write_route_for_note(
            session: AsyncSession, note_title: str, landmarks_name_position_pair: List[Dict[str, str | int]]
    ) -> bool:
        try:
            result = await session.execute_write(
                Creator._write_route_for_note, note_title, landmarks_name_position_pair
            )
            await logger.debug(f"method:\twrite_route_for_note,\nresult:\t{result}")
            return True
        except Exception as e:
            await logger.error(f"Error while writing route for note, args: {e.args[0]}")
            return False

    @staticmethod
    async def _write_route_saved_by_user(tx, user_login: str, landmarks_name_position_pairs: List[Dict[str, str | int]]):
        result = await tx.run(
            """
            OPTIONAL MATCH (userAccount: UserAccount WHERE userAccount.login STARTS WITH $user_login)
            WITH userAccount
                ORDER BY userAccount.login ASC
                LIMIT 1
            
            OPTIONAL MATCH (route: Route)
            WITH userAccount, route
                ORDER BY route.index_id DESC
                LIMIT 1
            WITH 
                userAccount,
                CASE 
                    WHEN route IS null THEN 0
                    WHEN route.index_id IS null THEN 0
                    ELSE route.index_id
                END AS last_route_index_id
            
            CREATE (route: Route {index_id: last_route_index_id + 1})<-[:ROUTE_SAVED_BY_USER]-(userAccount)
            WITH route
            
            UNWIND $landmarks_name_position_pairs AS landmark_name_position_pair
                CALL {
                    WITH landmark_name_position_pair
                    CALL db.index.fulltext.queryNodes('landmark_name_fulltext_index', landmark_name_position_pair.name)
                        YIELD score, node AS landmark
                    RETURN landmark
                        ORDER BY score DESC
                        LIMIT 1
                }
                CREATE (route)-[:PART_OF_ROUTE {position: landmark_name_position_pair.position}]->(landmark)
            """,
            user_login=user_login,
            landmarks_name_position_pairs=landmarks_name_position_pairs
        )
        result_summary = await (result.consume())
        counters = result_summary.counters

        if counters.nodes_created != 1:
            raise exceptions.Neo4jError("Unexpected behaviour: No nodes were created or to much nodes were created.")
        if counters.relationships_created != len(landmarks_name_position_pairs) + 1:  # User -> Route and Route -> its Landmarks
            raise exceptions.Neo4jError("Unexpected behaviour: Wrong amount of relationships, that were created.")
        if counters.properties_set != len(landmarks_name_position_pairs) + 1:  # index_id and position
            raise exceptions.Neo4jError(
                "Unexpected behaviour: Wrong amount properties that were set. Probably some of the given countries aren\'t exist"
            )

    @staticmethod
    async def write_route_saved_by_user(
            session: AsyncSession, user_login: str, landmarks_name_position_pairs: List[Dict[str, str | int]]
    ) -> bool:
        try:
            result = await session.execute_write(
                Creator._write_route_saved_by_user, user_login, landmarks_name_position_pairs
            )
            await logger.debug(f"method:\twrite_route_saved_by_user,\nresult:\t{result}")
            return True
        except Exception as e:
            await logger.error(f"Error while writing route for note, args: {e.args[0]}")
            return False

    @staticmethod
    async def _write_saved_route_from_note_relationship(tx, user_login: str, note_title: str):
        result = await tx.run(
            """
            OPTIONAL MATCH (userAccount: UserAccount WHERE userAccount.login STARTS WITH $user_login)
            WITH userAccount
                ORDER BY userAccount.login ASC
                LIMIT 1
                
            CALL db.index.fulltext.queryNodes('note_title_fulltext_index', $note_title)
                YIELD score, node AS note
            WITH userAccount, note
                ORDER BY score DESC
                LIMIT 1
                
            MATCH (route: Route)<-[:ROUTE_FOR_NOTE]-(note)
                
            CREATE (userAccount)-[:ROUTE_SAVED_BY_USER]->(route)
            """,
            user_login=user_login,
            note_title=note_title
        )
        result_summary = await (result.consume())
        counters = result_summary.counters

        if counters.relationships_created != 1:
            raise exceptions.Neo4jError("Unexpected behaviour: No relationship was created or to much nodes were created.")

    @staticmethod
    async def write_saved_route_from_note_relationship(session: AsyncSession, user_login: str, note_title: str) -> bool:
        try:
            result = await session.execute_write(
                Creator._write_saved_route_from_note_relationship, user_login, note_title
            )
            await logger.debug(f"method:\twrite_saved_route_from_note_relationship,\nresult:\t{result}")
            return True
        except Exception as e:
            await logger.error(f"Error while writing route for note, args: {e.args[0]}")
            return False


