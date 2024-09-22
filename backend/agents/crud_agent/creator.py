# Author: Vodohleb04
from typing import List, Dict

import neo4j
from aiologger.loggers.json import JsonLogger
from neo4j import AsyncSession, exceptions


logger = JsonLogger.with_default_handlers(
    level="INFO",
    serializer_kwargs={'ensure_ascii': False},
)


class Creator:
    """
    https://sefon.pro/mp3/217283-pantera-10-s/
    Creator part of CRUDAgent. All write queries to knowledgebase are located here.
    Implements PureCreator.
    All methods work asynchronously.
    """

    @staticmethod
    async def _write_user(tx, user_login: str) -> bool:
        """Transaction handler for write_user"""
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
    async def _write_note(tx, guide_login: str, country_names: List[str], note_title, note_category_names):
        """Transaction handler for write_note"""
        result = await tx.run(
            """
            MATCH (guideAccount: UserAccount&GuideAccount WHERE guideAccount.login STARTS WITH $guide_login)
            WITH guideAccount, datetime() AS now_time
                ORDER BY guideAccount.login ASC
                LIMIT 1
                
            CREATE (guideAccount)-[:AUTHOR]->(note: Note {title: $note_title, created_at: now_time, last_update: now_time, id_code: guideAccount.last_note_id_code + 1})
            
            WITH guideAccount, note
            
            WITH 
                note,
                guideAccount,
                COLLECT {
                    UNWIND $country_names AS country_name
                        CALL {
                            WITH country_name
                            MATCH (region: Region)
                                WHERE region.name STARTS WITH country_name
                            RETURN region
                                ORDER BY region.name
                                LIMIT 1
                        }
                        RETURN 'notes/' + toString(region.id_code) + '/' + toString(guideAccount.id_code) + '/' + toString(guideAccount.last_note_id_code + 1) + '/'
                } AS path_list
            
            SET note.path_list = path_list
            SET guideAccount.last_note_id_code = guideAccount.last_note_id_code + 1 
            WITH note
                    
            UNWIND $note_category_names AS note_category_name
                CALL {
                    WITH note_category_name
                    MATCH (noteCategory: NoteCategory)
                        WHERE noteCategory.name STARTS WITH note_category_name
                    RETURN noteCategory
                        ORDER BY noteCategory.name
                        LIMIT 1
                }
                    
                CREATE (note)-[:NOTE_REFERS]->(noteCategory)
            RETURN DISTINCT size(note.path_list) AS path_list_size
            """,
            guide_login=guide_login,
            country_names=country_names,
            note_title=note_title,
            note_category_names=note_category_names
        )
        path_list_size = 0
        async for record in result:
            path_list_size = record.data("path_list_size")["path_list_size"]
        result_summary = await (result.consume())
        counters = result_summary.counters
        if counters.nodes_created != 1:
            raise exceptions.Neo4jError("Unexpected behaviour: No nodes were created or to much nodes were created.")
        if counters.relationships_created != len(note_category_names) + 1:  # Author -> Note and Note -> its categories
            raise exceptions.Neo4jError("Unexpected behaviour: Wrong amount of relationships, that were created.")
        if path_list_size != len(country_names):
            raise exceptions.Neo4jError(
                "Unexpected behaviour: Wrong amount of paths were added to node. Probably some of the given countries aren\'t exist"
            )

    @staticmethod
    async def write_note(
            session: AsyncSession,
            guide_login: str,
            country_names: List[str],
            note_title: str,
            note_category_names: List[str]
    ) -> bool:
        try:
            result = await session.execute_write(
                Creator._write_note, guide_login, country_names, note_title, note_category_names
            )
            await logger.debug(f"method:\twrite_note,\nresult:\t{result}")
            return True
        except Exception as e:
            await logger.error(f"Error while writing note, args: {e.args[0]}")
            return False

    @staticmethod
    async def _write_route_for_note(
            tx, note_title: str, landmark_info_position_dicts: List[Dict[str, str | int | float]]
    ):
        """Transaction handler for write_route_for_note"""
        result = await tx.run(
            """
            MATCH (note: Note)
                WHERE note.title STARTS WITH $note_title
            WITH note
                ORDER BY note.title
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
            
            UNWIND $landmark_info_position_dicts AS landmark_info_position_dict
                CALL {
                    WITH landmark_info_position_dict
                    MATCH (landmark: Landmark) 
                        WHERE 
                            landmark.latitude = landmark_info_position_dict.latitude AND
                            landmark.longitude = landmark_info_position_dict.longitude AND
                            landmark.name STARTS WITH landmark_info_position_dict.name
                    RETURN landmark
                        ORDER BY landmark.name ASC
                        LIMIT 1
                }
                CREATE (route)-[:PART_OF_ROUTE {position: landmark_info_position_dict.position}]->(landmark)

            """,
            note_title=note_title,
            landmark_info_position_dicts=landmark_info_position_dicts
        )
        result_summary = await (result.consume())
        counters = result_summary.counters

        if counters.nodes_created != 1:
            raise exceptions.Neo4jError("Unexpected behaviour: No nodes were created or to much nodes were created.")
        if counters.relationships_created != len(landmark_info_position_dicts) + 1:  # Note -> Route and Route -> its Landmarks
            raise exceptions.Neo4jError("Unexpected behaviour: Wrong amount of relationships, that were created.")
        if counters.properties_set != len(landmark_info_position_dicts) + 1:  # index_id and position
            raise exceptions.Neo4jError(
                "Unexpected behaviour: Wrong amount properties that were set. Probably some of the given countries aren\'t exist"
            )

    @staticmethod
    async def write_route_for_note(
            session: AsyncSession, note_title: str, landmark_info_position_dicts: List[Dict[str, str | int | float]]
    ) -> bool:
        try:
            result = await session.execute_write(
                Creator._write_route_for_note, note_title, landmark_info_position_dicts
            )
            await logger.debug(f"method:\twrite_route_for_note,\nresult:\t{result}")
            return True
        except Exception as e:
            await logger.error(f"Error while writing route for note, args: {e.args[0]}")
            return False

    @staticmethod
    async def _write_route_saved_by_user(
            tx, user_login: str, landmark_info_position_dicts: List[Dict[str, str | int | float]]
    ):
        """Transaction handler for write_route_saved_by_user"""
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
            
            UNWIND $landmark_info_position_dicts AS landmark_info_position_dict
                CALL {
                    WITH landmark_info_position_dict
                    MATCH (landmark: Landmark) 
                        WHERE 
                            landmark.latitude = landmark_info_position_dict.latitude AND
                            landmark.longitude = landmark_info_position_dict.longitude AND
                            landmark.name STARTS WITH landmark_info_position_dict.name
                    RETURN landmark
                        ORDER BY landmark.name ASC
                        LIMIT 1
                }
                CREATE (route)-[:PART_OF_ROUTE {position: landmark_info_position_dict.position}]->(landmark)
            """,
            user_login=user_login,
            landmark_info_position_dicts=landmark_info_position_dicts
        )
        result_summary = await (result.consume())
        counters = result_summary.counters

        if counters.nodes_created != 1:
            raise exceptions.Neo4jError("Unexpected behaviour: No nodes were created or to much nodes were created.")
        if counters.relationships_created != len(landmark_info_position_dicts) + 1:  # User -> Route and Route -> its Landmarks
            raise exceptions.Neo4jError("Unexpected behaviour: Wrong amount of relationships, that were created.")
        if counters.properties_set != len(landmark_info_position_dicts) + 1:  # index_id and position
            raise exceptions.Neo4jError(
                "Unexpected behaviour: Wrong amount properties that were set. Probably some of the given countries aren\'t exist"
            )

    @staticmethod
    async def write_route_saved_by_user(
            session: AsyncSession, user_login: str, landmark_info_position_dicts: List[Dict[str, str | int | float]]
    ) -> bool:
        try:
            result = await session.execute_write(
                Creator._write_route_saved_by_user, user_login, landmark_info_position_dicts
            )
            await logger.debug(f"method:\twrite_route_saved_by_user,\nresult:\t{result}")
            return True
        except Exception as e:
            await logger.error(f"Error while writing route for note, args: {e.args[0]}")
            return False

    @staticmethod
    async def _write_saved_relationship_for_existing_route(tx, user_login: str, index_id: int):
        """Transaction handler for write_saved_relationship_for_existing_route"""
        result = await tx.run(
            """
            MATCH (userAccount: UserAccount WHERE userAccount.login STARTS WITH $user_login)
            WITH userAccount
                ORDER BY userAccount.login ASC
                LIMIT 1
                
            MATCH (route: Route) WHERE route.index_id = $index_id
                
            MERGE (userAccount)-[route_saved_by_user: ROUTE_SAVED_BY_USER]->(route)
            RETURN count(route_saved_by_user) AS amount_of_relationships
            """,
            user_login=user_login,
            index_id=index_id
        )
        amount_of_relationships = await result.single("amount_of_relationships")
        if amount_of_relationships.data("amount_of_relationships")["amount_of_relationships"] != 1:
            raise exceptions.Neo4jError("Unexpected behaviour: No relationship was created or to much relationships were created.")

    @staticmethod
    async def write_saved_relationship_for_existing_route(session: AsyncSession, user_login: str, index_id: int) -> bool:
        try:
            result = await session.execute_write(
                Creator._write_saved_relationship_for_existing_route, user_login, index_id
            )
            await logger.debug(f"method:\twrite_saved_relationship_for_existing_route,\nresult:\t{result}")
            return True
        except Exception as e:
            await logger.error(f"Error while writing route for note, args: {e.args[0]}")
            return False


