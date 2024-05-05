#Author: Vodohleb04
from typing import List, Dict
from aiologger.loggers.json import JsonLogger
from neo4j import AsyncSession
from backend.agents.crud_agent.pure_crud_classes.pure_reader import PureReader


logger = JsonLogger.with_default_handlers(
    level="INFO",
    serializer_kwargs={'ensure_ascii': False},
)


class Reader(PureReader):
    """
    Reader part of CRUDAgent. All read queries to knowledgebase are located here.
    Implements PureReader.
    All methods work asynchronously.
    """

    @staticmethod
    async def _read_categories_of_region(tx, region_name: str, optional_limit: int = None):
        """Transaction handler for read_categories_of_region"""
        result = await tx.run(
            """
            CALL {
                CALL db.index.fulltext.queryNodes('region_name_fulltext_index', $region_name)
                    YIELD score, node AS region
                RETURN region
                    ORDER BY score DESC
                    LIMIT 1
            }
            OPTIONAL MATCH  
                (region)
                    -[:INCLUDE]->*
                (located_at:Region)
                    <-[:LOCATED]-
                (:Landmark)
                    -[:REFERS]->
                (category:LandmarkCategory)
            RETURN DISTINCT category, located_at;
            """,
            region_name=region_name
        )
        try:
            if optional_limit:
                result_values = [record.data("category", "located_at") for record in await result.fetch(optional_limit)]
            else:
                result_values = [record.data("category", "located_at") async for record in result]
        except IndexError as ex:
            await logger.error(f"Index error, args: {ex.args[0]}")
            result_values = []
        await logger.debug(f"method:\t_read_categories_of_region,\nresult:\t{await result.consume()}")
        return result_values

    @staticmethod
    async def read_categories_of_region(session: AsyncSession, region_name: str, optional_limit: int = None):
        result = await session.execute_read(Reader._read_categories_of_region, region_name, optional_limit)
        await logger.debug(f"method:\tread_categories_of_region,\nresult:\t{result}")
        return result

    @staticmethod
    async def _read_landmarks_in_map_sectors(tx, map_sectors_names: List[str], optional_limit: int = None):
        """Transaction handler for read_categories_of_region"""
        result = await tx.run(
            """
            UNWIND $map_sectors_names AS sector_name
            CALL {
                WITH sector_name
                CALL db.index.fulltext.queryNodes('map_sector_name_fulltext_index', sector_name)
                    YIELD score, node AS sector
                RETURN sector
                    ORDER BY score DESC
                    LIMIT 1
            }
            OPTIONAL MATCH (landmark: Landmark)-[:IN_SECTOR]->(sector)
            RETURN
                landmark,
                sector,
                COLLECT {
                    MATCH (landmark)-[:REFERS]->(category:LandmarkCategory)
                    RETURN category.name AS category_name
                } AS categories_names
                ORDER BY sector.name;
            """,
            map_sectors_names=map_sectors_names
        )
        try:
            if optional_limit:
                result_values = [
                    record.data("landmark", "categories_names", "sector")
                    for record in await result.fetch(optional_limit)
                ]
            else:
                result_values = [record.data("landmark", "categories_names", "sector") async for record in result]
        except IndexError as ex:
            await logger.error(f"Index error, args: {ex.args[0]}")
            result_values = []

        await logger.debug(f"method:\t_read_landmarks_in_map_sectors,\nresult:\t{await result.consume()}")
        return result_values

    @staticmethod
    async def read_landmarks_in_map_sectors(
            session: AsyncSession, map_sectors_names: List[str], optional_limit: int = None
    ):
        result = await session.execute_read(Reader._read_landmarks_in_map_sectors, map_sectors_names, optional_limit)
        await logger.debug(f"method:\tread_landmarks_in_map_sectors,\nresult:\t{result}")
        return result

    @staticmethod
    async def _read_landmarks_by_coordinates(tx, coordinates: List[Dict[str, float]], optional_limit: int = None):
        """Transaction handler for read_landmarks_by_coordinates"""
        result = await tx.run(
            """
            UNWIND $coordinates AS coordinate
            OPTIONAL MATCH (landmark: Landmark)
                WHERE
                    landmark.latitude = toFloat(coordinate.latitude) AND 
                    landmark.longitude = toFloat(coordinate.longitude)
            RETURN
                landmark,
                COLLECT {
                    MATCH (landmark)-[:REFERS]->(category:LandmarkCategory)
                    RETURN category.name AS category_name
                } AS categories_names;
            """,
            coordinates=coordinates
        )
        try:
            if optional_limit:
                result_values = [
                    record.data("landmark", "categories_names") for record in await result.fetch(optional_limit)
                ]
            else:
                result_values = [record.data("landmark", "categories_names") async for record in result]
        except IndexError as ex:
            await logger.error(f"Index error, args: {ex.args[0]}")
            result_values = []

        await logger.debug(f"method:\t_read_landmarks_by_coordinates,\nresult:\t{await result.consume()}")
        return result_values

    @staticmethod
    async def read_landmarks_by_coordinates(
            session: AsyncSession, coordinates: List[Dict[str, float]], optional_limit: int = None
    ):
        result = await session.execute_read(Reader._read_landmarks_by_coordinates, coordinates, optional_limit)
        await logger.debug(f"method:\tread_landmarks_by_coordinates,\nresult:\t{result}")
        return result

    @staticmethod
    async def _read_landmarks_refers_to_categories(tx, categories_names: List[str], optional_limit: int = None):
        """Transaction handler for read_landmarks_refers_to_categories"""
        result = await tx.run(
            """
            UNWIND $categories_names AS category_name
            CALL {
                WITH category_name
                CALL db.index.fulltext.queryNodes('landmark_category_name_fulltext_index', category_name)
                    YIELD score, node AS category
                RETURN category
                    ORDER BY score DESC
                    LIMIT 1
            }
            OPTIONAL MATCH (landmark: Landmark)-[:REFERS]->(category)
            RETURN DISTINCT landmark, category
                ORDER BY landmark.name;
            """,
            categories_names=categories_names
        )
        try:
            if optional_limit:
                result_values = [record.data("landmark", "category") for record in await result.fetch(optional_limit)]
            else:
                result_values = [record.data("landmark", "category") async for record in result]
        except IndexError as ex:
            await logger.error(f"Index error, args: {ex.args[0]}")
            result_values = []

        await logger.debug(f"method:\t_read_landmarks_refers_to_categories,\nresult:\t{await result.consume()}")
        return result_values

    @staticmethod
    async def read_landmarks_refers_to_categories(
            session: AsyncSession, categories_names: List[str], optional_limit: int = None
    ):
        result = await session.execute_read(
            Reader._read_landmarks_refers_to_categories, categories_names, optional_limit
        )
        await logger.debug(f"method:\read_landmarks_refers_to_categories,\nresult:\t{result}")
        return result

    @staticmethod
    async def _read_landmarks_by_names(tx, landmark_names: List[str], optional_limit: int = None):
        """Transaction handler for read_landmarks_by_names"""
        result = await tx.run(
            """
            UNWIND $landmark_names AS landmark_name
            CALL {
                WITH landmark_name
                MATCH (landmark: Landmark)
                    WHERE landmark.name STARTS WITH landmark_name
                RETURN landmark
                    ORDER BY landmark.name ASC
                    LIMIT 1
            }
            RETURN
                landmark,
                COLLECT {
                    MATCH (landmark)-[:REFERS]->(category:LandmarkCategory)
                    RETURN category.name AS category_name
                } AS categories_names;
            """,
            landmark_names=landmark_names
        )
        try:
            if optional_limit:
                result_values = [
                    record.data("landmark", "categories_names") for record in await result.fetch(optional_limit)
                ]
            else:
                result_values = [record.data("landmark", "categories_names") async for record in result]
        except IndexError as ex:
            await logger.error(f"Index error, args: {ex.args[0]}")
            result_values = []

        await logger.debug(f"method:\t_read_landmarks_by_names,\nresult:\t{await result.consume()}")
        return result_values

    @staticmethod
    async def read_landmarks_by_names(session: AsyncSession, landmark_names: List[str], optional_limit: int = None):
        result = await session.execute_read(Reader._read_landmarks_by_names, landmark_names, optional_limit)
        await logger.debug(f"method:\tread_landmarks_by_names,\nresult:\t{result}")
        return result

    @staticmethod
    async def _read_landmarks_of_categories_in_region(
            tx, region_name: str, categories_names: List[str], optional_limit
    ):
        """Transaction handler for read_landmarks_of_categories_in_region"""
        result = await tx.run(
            """
            CALL db.index.fulltext.queryNodes('region_name_fulltext_index', $region_name)
                YIELD score, node AS region
            WITH score, region
                ORDER BY score DESC
                LIMIT 1
            UNWIND $categories_names AS category_name
            CALL {
                WITH category_name
                CALL db.index.fulltext.queryNodes("landmark_category_name_fulltext_index", category_name)
                    YIELD score, node AS category
                RETURN category
                    ORDER BY score DESC
                    LIMIT 1
            }
            OPTIONAL MATCH
                (region)
                    -[:INCLUDE]->*
                (final_region:Region)
                    <-[:LOCATED]-
                (landmark:Landmark)
                    -[:REFERS]->
                (category)
            RETURN landmark, final_region AS located_at, category; 
            """,
            region_name=region_name,
            categories_names=categories_names
        )
        try:
            if optional_limit:
                result_values = [
                    record.data("landmark", "located_at", "category") for record in await result.fetch(optional_limit)
                ]
            else:
                result_values = [record.data("landmark", "located_at", "category") async for record in result]
        except IndexError as ex:
            await logger.error(f"Index error, args: {ex.args[0]}")
            result_values = []

        await logger.debug(f"method:\t_read_landmarks_of_categories_in_region,\nresult:\t{await result.consume()}")
        return result_values

    @staticmethod
    async def read_landmarks_of_categories_in_region(
            session: AsyncSession, region_name: str, categories_names: List[str], optional_limit: int = None
    ):
        result = await session.execute_read(
            Reader._read_landmarks_of_categories_in_region, region_name, categories_names, optional_limit
        )
        await logger.debug(f"method:\tread_landmarks_of_categories_in_region,\nresult:\t{result}")
        return result

    @staticmethod
    async def _read_recommendations_for_landmark_by_region(
            tx, user_login: str, current_latitude: float,  current_longitude: float, current_name: str,
            amount_of_recommendations: int
    ):
        """Transaction handler for read_recommendations_for_landmark_by_region"""
        result = await tx.run(
            """
            MATCH (current_landmark: Landmark) 
                WHERE
                    current_landmark.latitude = $current_latitude AND
                    current_landmark.longitude = $current_longitude AND
                    current_landmark.name STARTS WITH $current_name
            OPTIONAL MATCH
                (category:LandmarkCategory)<-[current_landmark_category_ref:REFERS]-(current_landmark)
                    -[:LOCATED]->
                (:Region)((:Region&!State)-[:INCLUDE|NEIGHBOUR_REGION]-(:Region&!State)){0,4}(:Region)
                    <-[:LOCATED]-
                (recommendation:Landmark)-[recommendation_landmark_category_ref:REFERS]->(category)
            OPTIONAL MATCH (userAccount: UserAccount WHERE userAccount.login = $user_login)
            OPTIONAL MATCH (userAccount)-[wish_ref:WISH_TO_VISIT]->(recommendation)
            OPTIONAL MATCH (userAccount)-[visited_ref:VISITED]->(recommendation)
            WITH 
                recommendation,
                recommendation_landmark_category_ref,
                current_landmark_category_ref,
                wish_ref,
                visited_ref
            ORDER BY 
                current_landmark_category_ref.main_category_flag DESC,
                recommendation_landmark_category_ref.main_category_flag DESC,
                point.distance(
                    point({latitude: $current_latitude, longitude: $current_longitude}),
                    point({latitude: recommendation.latitude, longitude: recommendation.longitude})
                ) ASC
            LIMIT $amount_of_recommendations
            RETURN DISTINCT 
                recommendation,
                COLLECT {
                    MATCH (recommendation)
                        -[refer:REFERS WHERE refer.main_category_flag = True]->
                    (category:LandmarkCategory)
                    RETURN category.name AS category_name
                } AS main_categories_names,
                COLLECT {
                    MATCH (recommendation)
                        -[refer:REFERS WHERE refer.main_category_flag = False]->
                    (category:LandmarkCategory)
                    RETURN category.name AS category_name
                } AS subcategories_names,
                point.distance(
                    point({latitude: $current_latitude, longitude: $current_longitude}),
                    point({latitude: recommendation.latitude, longitude: recommendation.longitude})
                ) AS distance,
                CASE
                    WHEN wish_ref IS NULL THEN False
                    ELSE True
                END AS wish_to_visit,
                CASE
                    WHEN visited_ref.amount IS NULL THEN 0
                    ELSE visited_ref.amount
                END AS visited_amount;
            """,
            user_login=user_login, current_latitude=current_latitude, current_longitude=current_longitude,
            current_name=current_name, amount_of_recommendations=amount_of_recommendations
        )
        try:
            result_values = []
            async for record in result:
                result_values.append(
                    record.data(
                        "recommendation", "main_categories_names", "subcategories_names", "distance", "wish_to_visit",
                        "visited_amount"
                    )
                )
        except IndexError as ex:
            await logger.error(f"Index error, args: {ex.args[0]}")
            result_values = []

        await logger.debug(f"method:\t_read_recommendations_for_landmark_by_region,\nresult:\t{await result.consume()}")
        return result_values

    @staticmethod
    async def read_recommendations_for_landmark_by_region(
            session: AsyncSession, user_login: str, current_latitude: float, current_longitude: float,
            current_name: str, amount_of_recommendations: int
    ):
        result = await session.execute_read(
            Reader._read_recommendations_for_landmark_by_region, user_login,  current_latitude, current_longitude,
            current_name, amount_of_recommendations
        )
        await logger.debug(f"method:\tread_recommendations_for_landmark_by_region,\nresult:\t{result}")
        return result

    @staticmethod
    async def _read_landmarks_by_region(tx, region_name: str, optional_limit: int = None):
        """Transaction handler for read_landmarks_by_region"""
        result = await tx.run(
            """
            CALL db.index.fulltext.queryNodes('region_name_fulltext_index', $region_name)
                YIELD score, node AS region
            WITH score, region
                ORDER BY score DESC
                LIMIT 1
            OPTIONAL MATCH
                (region)
                    -[:INCLUDE]->*
                (final_region:Region)
                    <-[:LOCATED]-
                (landmark:Landmark)
            RETURN
                landmark,
                COLLECT {
                    MATCH (landmark)-[:REFERS]->(category:LandmarkCategory)
                    RETURN category.name AS category_name
                } AS categories_names,
                final_region AS located_at;
            """,
            region_name=region_name
        )
        try:
            if optional_limit:
                result_values = [
                    record.data("landmark", "categories_names", "located_at")
                    for record in await result.fetch(optional_limit)
                ]
            else:
                result_values = [
                    record.data("landmark", "categories_names", "located_at") async for record in result
                ]
        except IndexError as ex:
            await logger.error(f"Index error, args: {ex.args[0]}")
            result_values = []

        await logger.debug(f"method:\t_read_landmarks_by_region,\nresult:\t{await result.consume()}")
        return result_values

    @staticmethod
    async def read_landmarks_by_region(session: AsyncSession, region_name: str, optional_limit: int = None):
        result = await session.execute_read(Reader._read_landmarks_by_region, region_name, optional_limit)
        await logger.debug(f"method:\tread_landmarks_by_region,\nresult:\t{result}")
        return result

    @staticmethod
    async def _read_map_sectors_of_points(
            tx, coordinates_of_points: List[Dict[str, float]], optional_limit: int = None
    ):
        """Transaction handler for read_map_sectors_of_points"""

        result = await tx.run(
            """
            UNWIND $coordinates_of_points AS coordinates_of_point
            OPTIONAL MATCH (mapSector: MapSector)
                WHERE
                    mapSector.tl_longitude <= toFloat(coordinates_of_point.longitude) AND
                    mapSector.tl_latitude >= toFloat(coordinates_of_point.latitude) AND
                    point.withinBBox(
                        point({latitude: coordinates_of_point.latitude, longitude: coordinates_of_point.longitude, crs:'WGS-84'}),
                        point({latitude: mapSector.br_latitude, longitude: mapSector.tl_longitude, crs:'WGS-84'}),
                        point({latitude: mapSector.tl_latitude, longitude: mapSector.br_longitude, crs:'WGS-84'})
                    )
            RETURN mapSector AS map_sector, coordinates_of_point AS of_point;
            """,
            coordinates_of_points=coordinates_of_points
        )
        try:
            if optional_limit:
                result_values = [record.data("map_sector", "of_point") for record in await result.fetch(optional_limit)]
            else:
                result_values = [record.data("map_sector", "of_point") async for record in result]
        except IndexError as ex:
            await logger.error(f"Index error, args: {ex.args[0]}")
            result_values = []

        await logger.debug(f"method:\t_read_map_sectors_of_points,\nresult:\t{await result.consume()}")
        return result_values

    @staticmethod
    async def read_map_sectors_of_points(
            session: AsyncSession, coordinates_of_points: List[Dict[str, float]], optional_limit: int = None
    ):
        result = await session.execute_read(
            Reader._read_map_sectors_of_points, coordinates_of_points, optional_limit
        )
        await logger.debug(f"method:\tread_map_sectors_of_points,\nresult:\t{result}")
        return result

    @staticmethod
    async def _read_map_sectors_structure_of_region(tx, region_name: str):
        """Transaction handler for read_map_sectors_structure_of_region"""

        result = await tx.run(
            """
            CALL db.index.fulltext.queryNodes('region_name_fulltext_index', $region_name)
                YIELD score, node AS region
            MATCH (region)-[:DIVIDED_ON_SECTORS]->(:CountryMapSectors)-[:INCLUDE_SECTOR]->(mapSector:MapSector)
            RETURN 
                mapSector.name AS name,
                mapSector.tl_latitude AS tl_latitude,
                mapSector.tl_longitude AS tl_longitude,
                mapSector.br_latitude AS br_latitude,
                mapSector.br_longitude AS br_longitude,
                COLLECT {
                    MATCH (mapSector)-[:NEIGHBOUR_SECTOR]-(neighbour_map_sector:MapSector)
                    RETURN neighbour_map_sector.name AS neighbour_map_sector_name
                } AS neighbour_map_sector_names
            """,
            region_name=region_name
        )
        try:
            result_values = [
                record.data(
                    "name", "tl_latitude", "tl_longitude", "br_latitude", "br_longitude", "neighbour_map_sector_names"
                ) async for record in result
            ]
        except IndexError as ex:
            await logger.error(f"Index error, args: {ex.args[0]}")
            result_values = []

        await logger.debug(f"method:\t_read_map_sectors_structure_of_region,\nresult:\t{await result.consume()}")
        return result_values

    @staticmethod
    async def read_map_sectors_structure_of_region(session: AsyncSession, region_name: str):
        result = await session.execute_read(Reader._read_map_sectors_structure_of_region, region_name)
        await logger.debug(f"method:\tread_map_sectors_structure_of_region,\nresult:\t{result}")
        return result

    @staticmethod
    async def _read_landmarks_of_categories_in_map_sectors(
            tx, map_sectors_names: List[str], categories_names: List[str], optional_limit: int = None
    ):
        """Transaction handler for read_landmarks_of_categories_in_map_sectors"""
        result = await tx.run(
            """
            UNWIND $map_sectors_names AS map_sector_name
            CALL {
                WITH map_sector_name
                CALL db.index.fulltext.queryNodes('map_sector_name_fulltext_index', map_sector_name)
                    YIELD score, node AS mapSector
                RETURN mapSector
                    ORDER BY score DESC
                    LIMIT 1
            }
            WITH mapSector
            UNWIND $categories_names AS category_name
            CALL {
                WITH category_name
                CALL db.index.fulltext.queryNodes("landmark_category_name_fulltext_index", category_name)
                    YIELD score, node AS category
                RETURN category
                    ORDER BY score DESC
                    LIMIT 1
            }
            OPTIONAL MATCH
                (mapSector)
                    <-[:IN_SECTOR]-
                (landmark:Landmark)
                    -[:REFERS]->
                (category)
            RETURN landmark, mapSector AS map_sector, category;
            """,
            map_sectors_names=map_sectors_names,
            categories_names=categories_names
        )
        try:
            if optional_limit:
                result_values = [
                    record.data("landmark", "map_sector", "category") for record in await result.fetch(optional_limit)
                ]
            else:
                result_values = [record.data("landmark", "map_sector", "category") async for record in result]
        except IndexError as ex:
            await logger.error(f"Index error, args: {ex.args[0]}")
            result_values = []

        await logger.debug(f"method:\t_read_landmarks_of_categories_in_map_sectors,\nresult:\t{await result.consume()}")
        return result_values

    @staticmethod
    async def read_landmarks_of_categories_in_map_sectors(
            session: AsyncSession, map_sectors_names: List[str], categories_names: List[str], optional_limit: int = None
    ):
        result = await session.execute_read(
            Reader._read_landmarks_of_categories_in_map_sectors,
            map_sectors_names,
            categories_names,
            optional_limit
        )
        await logger.debug(f"method:\tread_landmarks_of_categories_in_map_sectors,\nresult:\t{result}")
        return result

    @staticmethod
    async def _read_route_landmarks_by_index_id(tx, index_id: int):
        """Transaction handler for read_route_landmarks_by_index_id"""
        result = await tx.run(
            """    
            MATCH (route: Route) WHERE route.index_id = $index_id
            MATCH (landmark: Landmark)<-[part_of_route: PART_OF_ROUTE]-(route) 
            RETURN landmark
                ORDER BY part_of_route.position ASC
            """,
            index_id=index_id
        )
        try:
            result_values = [record.data("landmark") async for record in result]
        except IndexError as ex:
            await logger.error(f"Index error, args: {ex.args[0]}")
            result_values = []

        await logger.debug(f"method:\t_read_route_landmarks_by_index_id,\nresult:\t{await result.consume()}")
        return result_values

    @staticmethod
    async def read_route_landmarks_by_index_id(session, index_id: int):
        result = await session.execute_read(
            Reader._read_route_landmarks_by_index_id, index_id
        )
        await logger.debug(f"method:\tread_route_landmarks_by_index_id,\nresult:\t{result}")
        return result

    @staticmethod
    async def _read_routes_saved_by_user(tx, user_login: str):
        """Transaction handler for read_routes_saved_by_user"""
        result = await tx.run(
            """    
            OPTIONAL MATCH (userAccount: UserAccount WHERE userAccount.login STARTS WITH $user_login)
            WITH userAccount
                ORDER BY userAccount.login ASC
                LIMIT 1
            
            OPTIONAL MATCH (route: Route)<-[:ROUTE_SAVED_BY_USER]-(userAccount)
            
            RETURN 
                route,
                COLLECT {
                    OPTIONAL MATCH (landmark: Landmark)<-[part_of_route: PART_OF_ROUTE]-(route)
                    RETURN landmark
                        ORDER BY part_of_route.position ASC
                } AS route_landmarks
                    ORDER BY route.index_id
            """,
            user_login=user_login
        )
        try:
            result_values = [record.data("route", "route_landmarks") async for record in result]
        except IndexError as ex:
            await logger.error(f"Index error, args: {ex.args[0]}")
            result_values = []

        await logger.debug(f"method:\t_read_routes_saved_by_user,\nresult:\t{await result.consume()}")
        return result_values

    @staticmethod
    async def read_routes_saved_by_user(session, user_login: str):
        result = await session.execute_read(Reader._read_routes_saved_by_user, user_login)
        await logger.debug(f"method:\tread_routes_saved_by_user,\nresult:\t{result}")
        return result

    @staticmethod
    async def _read_range_of_routes_saved_by_user(tx, user_login: str, skip: int, limit: int):
        """Transaction handler for read_range_of_routes_saved_by_user"""
        result = await tx.run(
            """    
            OPTIONAL MATCH (userAccount: UserAccount WHERE userAccount.login STARTS WITH $user_login)
            WITH userAccount
                ORDER BY userAccount.login ASC
                LIMIT 1

            OPTIONAL MATCH (route: Route)<-[:ROUTE_SAVED_BY_USER]-(userAccount)

            RETURN 
                route,
                COLLECT {
                    OPTIONAL MATCH (landmark: Landmark)<-[part_of_route: PART_OF_ROUTE]-(route)
                    RETURN landmark
                        ORDER BY part_of_route.position ASC
                } AS route_landmarks
                    ORDER BY route.index_id
                    SKIP $skip
                    LIMIT $limit
            """,
            user_login=user_login,
            skip=skip,
            limit=limit
        )
        try:
            result_values = [record.data("route", "route_landmarks") async for record in result]
        except IndexError as ex:
            await logger.error(f"Index error, args: {ex.args[0]}")
            result_values = []

        await logger.debug(f"method:\t_read_range_of_routes_saved_by_user,\nresult:\t{await result.consume()}")
        return result_values

    @staticmethod
    async def read_range_of_routes_saved_by_user(session, user_login: str, skip: int, limit: int):
        result = await session.execute_read(Reader._read_range_of_routes_saved_by_user, user_login, skip, limit)
        await logger.debug(f"method:\tread_range_of_routes_saved_by_user,\nresult:\t{result}")
        return result

    @staticmethod
    async def _read_note_by_title(tx, note_title: str):
        """Transaction handler for read_note_by_title"""
        result = await tx.run(
            """    
            CALL db.index.fulltext.queryNodes('note_title_fulltext_index', $note_title)
                YIELD score, node AS note
            WITH note
                ORDER BY score DESC
                LIMIT 1
            OPTIONAL MATCH (route: Route)<-[:ROUTE_FOR_NOTE]-(note)
            RETURN
                note,
                route,
                COLLECT {
                    OPTIONAL MATCH (landmark: Landmark)<-[part_of_route: PART_OF_ROUTE]-(route)
                    RETURN landmark
                        ORDER BY part_of_route.position ASC
                } AS route_landmarks,
                COLLECT {
                    OPTIONAL MATCH (note_category: NoteCategory)<-[:NOTE_REFERS]-(note)
                    RETURN note_category.name
                } AS note_category_names
                    ORDER BY route.index_id
            """,
            note_title=note_title
        )
        try:
            result_values = []
            async for record in result:
                record = record.data("note", "route", "route_landmarks", "note_category_names")
                if record["note"] is not None:
                    record["note"]["last_update"] = record["note"]["last_update"].to_native()
                result_values.append(record)
        except IndexError as ex:
            await logger.error(f"Index error, args: {ex.args[0]}")
            result_values = []

        await logger.debug(f"method:\t_read_note_by_title,\nresult:\t{await result.consume()}")
        return result_values

    @staticmethod
    async def read_note_by_title(session, note_title: str):
        result = await session.execute_read(Reader._read_note_by_title, note_title)
        await logger.debug(f"method:\tread_note_by_title,\nresult:\t{result}")
        return result

    @staticmethod
    async def _read_notes_in_range(tx, skip: int, limit: int):
        """Transaction handler for read_notes_in_range"""
        result = await tx.run(
            """
            MATCH (note: Note)
            WITH note
                ORDER BY note.last_update DESC
                SKIP $skip
                LIMIT $limit
            OPTIONAL MATCH (route: Route)<-[:ROUTE_FOR_NOTE]-(note)
            RETURN
                note,
                route,
                COLLECT {
                    OPTIONAL MATCH (landmark: Landmark)<-[part_of_route: PART_OF_ROUTE]-(route)
                    RETURN landmark
                        ORDER BY part_of_route.position ASC
            } AS route_landmarks,
            COLLECT {
                OPTIONAL MATCH (note_category: NoteCategory)<-[:NOTE_REFERS]-(note)
                RETURN note_category.name
            } AS note_category_names
                ORDER BY 
                    note.last_update DESC,
                    route.index_id ASC
            """,
            skip=skip, limit=limit
        )
        try:
            result_values = []
            async for record in result:
                record = record.data("note", "route", "route_landmarks", "note_category_names")
                if record["note"] is not None:
                    record["note"]["last_update"] = record["note"]["last_update"].to_native()
                result_values.append(record)
        except IndexError as ex:
            await logger.error(f"Index error, args: {ex.args[0]}")
            result_values = []

        await logger.debug(f"method:\t_read_notes_in_range,\nresult:\t{await result.consume()}")
        return result_values

    @staticmethod
    async def read_notes_in_range(session, skip: int, limit: int):
        result = await session.execute_read(Reader._read_notes_in_range, skip, limit)
        await logger.debug(f"method:\tread_notes_in_range,\nresult:\t{result}")
        return result

    @staticmethod
    async def _read_notes_of_categories_in_range(tx, note_categories_names: List[str], skip: int, limit: int):
        """Transaction handler for read_notes_of_categories_in_range"""
        result = await tx.run(
            """
            UNWIND $note_categories_names AS note_category_name
                CALL {
                    WITH note_category_name
                    CALL db.index.fulltext.queryNodes("note_category_name_fulltext_index", note_category_name)
                        YIELD score, node AS note_category
                    RETURN note_category
                        ORDER BY score DESC
                        LIMIT 1
                }
                MATCH (note: Note)-[:NOTE_REFERS]->(note_category)
                WITH DISTINCT note
                    ORDER BY note.last_update DESC
                    SKIP $skip
                    LIMIT $limit
                OPTIONAL MATCH (route: Route)<-[:ROUTE_FOR_NOTE]-(note)
                RETURN
                    note,
                    route,
                    COLLECT {
                        OPTIONAL MATCH (landmark: Landmark)<-[part_of_route: PART_OF_ROUTE]-(route)
                        RETURN landmark
                            ORDER BY part_of_route.position ASC
                    } AS route_landmarks,
                    COLLECT {
                        OPTIONAL MATCH (note_category: NoteCategory)<-[:NOTE_REFERS]-(note)
                        RETURN note_category.name
                    } AS note_category_names
                        ORDER BY 
                            note.last_update DESC,
                            route.index_id ASC
            """,
            note_categories_names=note_categories_names, skip=skip, limit=limit
        )
        try:
            result_values = []
            async for record in result:
                record = record.data("note", "route", "route_landmarks", "note_category_names")
                if record["note"] is not None:
                    record["note"]["last_update"] = record["note"]["last_update"].to_native()
                result_values.append(record)
        except IndexError as ex:
            await logger.error(f"Index error, args: {ex.args[0]}")
            result_values = []

        await logger.debug(f"method:\t_read_notes_of_categories_in_range,\nresult:\t{await result.consume()}")
        return result_values

    @staticmethod
    async def read_notes_of_categories_in_range(session, note_categories_names: List[str], skip: int, limit: int):
        result = await session.execute_read(
            Reader._read_notes_of_categories_in_range, note_categories_names, skip, limit
        )
        await logger.debug(f"method:\tread_notes_of_categories_in_range,\nresult:\t{result}")
        return result

    @staticmethod
    async def _read_recommendations_by_coordinates_and_categories(
            tx,
            coordinates_of_points: List[Dict[str, float]],
            categories_names: List[str],
            user_login: str,
            amount_of_recommendations_for_point: int,
            optional_limit: int | None
    ):
        """Transaction handler for read_recommendations_by_coordinates_and_categories"""
        result = await tx.run(
            """
            OPTIONAL MATCH (userAccount: UserAccount WHERE userAccount.login STARTS WITH $user_login)
            WITH userAccount
                ORDER BY userAccount.login ASC
                LIMIT 1
                        
            UNWIND $coordinates_of_points AS coordinates_of_point
            CALL {
                WITH coordinates_of_point, userAccount
                OPTIONAL MATCH (mapSector: MapSector)
                    WHERE
                        mapSector.tl_longitude <= toFloat(coordinates_of_point.longitude) AND
                        mapSector.tl_latitude >= toFloat(coordinates_of_point.latitude) AND
                        point.withinBBox(
                            point({latitude: coordinates_of_point.latitude, longitude: coordinates_of_point.longitude, crs:'WGS-84'}),
                            point({latitude: mapSector.br_latitude, longitude: mapSector.tl_longitude, crs:'WGS-84'}),
                            point({latitude: mapSector.tl_latitude, longitude: mapSector.br_longitude, crs:'WGS-84'})
                        )
                        
                WITH mapSector, coordinates_of_point, userAccount
                UNWIND $categories_names AS category_name
                CALL {
                    WITH category_name
                    CALL db.index.fulltext.queryNodes("landmark_category_name_fulltext_index", category_name)
                        YIELD score, node AS category
                    RETURN category
                        ORDER BY score DESC
                        LIMIT 1
                }
                
                OPTIONAL MATCH
                    (mapSector) ((:MapSector)-[:NEIGHBOUR_SECTOR]-(:MapSector)){0,1} (recommendationSector: MapSector)
                        <-[:IN_SECTOR]-
                    (recommendedLandmark:Landmark)
                        -[recommendation_landmark_category_ref:REFERS]->
                    (category)
                    
                OPTIONAL MATCH (userAccount)-[wish_ref:WISH_TO_VISIT]->(recommendedLandmark)
                OPTIONAL MATCH (userAccount)-[visited_ref:VISITED]->(recommendedLandmark)
                
                WITH DISTINCT
                    coordinates_of_point,
                    recommendedLandmark AS recommendation,
                    recommendation_landmark_category_ref,
                    category,
                    wish_ref,
                    visited_ref,
                    point.distance(
                        point({latitude: coordinates_of_point.latitude, longitude: coordinates_of_point.longitude, crs:'WGS-84'}),
                        point({latitude: recommendedLandmark.latitude, longitude: recommendedLandmark.longitude})
                    ) AS distance,
                    userAccount
                ORDER BY distance ASC
                LIMIT $amount_of_recommendations_for_point
                
                RETURN
                    recommendation,
                    COLLECT {
                        MATCH (recommendation)
                            -[main_category_refer:REFERS WHERE main_category_refer.main_category_flag = True]->
                        (main_category:LandmarkCategory)
                        RETURN main_category.name AS main_category_name
                    } AS main_categories_names,
                    COLLECT {
                        MATCH (recommendation)
                            -[subcategory_refer:REFERS WHERE subcategory_refer.main_category_flag = False]->
                        (subcategory:LandmarkCategory)
                        RETURN subcategory.name AS subcategory_name
                    } AS subcategories_names,
                    distance,
                    CASE
                        WHEN wish_ref IS NULL THEN False
                        ELSE True
                    END AS wish_to_visit,
                    CASE
                        WHEN visited_ref.amount IS NULL THEN 0
                        ELSE visited_ref.amount
                    END AS visited_amount
            } 
            RETURN DISTINCT
                recommendation,
                main_categories_names,
                subcategories_names,
                distance,
                wish_to_visit,
                visited_amount
            """,
            coordinates_of_points=coordinates_of_points, categories_names=categories_names, user_login=user_login,
            amount_of_recommendations_for_point=amount_of_recommendations_for_point
        )
        try:
            if optional_limit:
                result_values = [
                    record.data(
                        "recommendation", "main_categories_names", "subcategories_names", "distance", "wish_to_visit",
                        "visited_amount"
                    ) for record in await result.fetch(optional_limit)
                ]
            else:
                result_values = [
                    record.data(
                        "recommendation", "main_categories_names", "subcategories_names", "distance", "wish_to_visit",
                        "visited_amount"
                    ) async for record in result
                ]
        except IndexError as ex:
            await logger.error(f"Index error, args: {ex.args[0]}")
            result_values = []

        await logger.debug(
            f"method:\t_read_recommendations_by_coordinates_and_categories,\nresult:\t{await result.consume()}"
        )
        return result_values

    @staticmethod
    async def read_recommendations_by_coordinates_and_categories(
            session: AsyncSession,
            coordinates_of_points: List[Dict[str, float]],
            categories_names: List[str],
            user_login: str,
            amount_of_recommendations_for_point: int,
            optional_limit: int = None
    ):
        result = await session.execute_read(
            Reader._read_recommendations_by_coordinates_and_categories, coordinates_of_points, categories_names,
            user_login, amount_of_recommendations_for_point, optional_limit
        )
        await logger.debug(f"method:\tread_recommendations_by_coordinates_and_categories,\nresult:\t{result}")
        return result

