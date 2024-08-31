#Author: Vodohleb04
from typing import List, Dict
from aiologger.loggers.json import JsonLogger
from neo4j import AsyncSession


logger = JsonLogger.with_default_handlers(
    level="INFO",
    serializer_kwargs={'ensure_ascii': False},
)


class Reader:
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
                MATCH (region: Region)
                    WHERE region.name STARTS WITH $region_name
                RETURN region
                    ORDER BY region.name
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
                MATCH (sector: MapSector)
                    WHERE sector.name STARTS WITH sector_name
                RETURN sector
                    ORDER BY sector.name
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
                MATCH (category: LandmarkCategory)
                    WHERE category.name STARTS WITH category_name
                RETURN category
                    ORDER BY category.name
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
    async def _read_landmarks_by_name_list(tx, landmark_names: List[str]):
        """Transaction handler for read_landmarks_by_name_list"""
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
            result_values = [record.data("landmark", "categories_names") async for record in result]
        except IndexError as ex:
            await logger.error(f"Index error, args: {ex.args[0]}")
            result_values = []

        await logger.debug(f"method:\t_read_landmarks_by_name_list,\nresult:\t{await result.consume()}")
        return result_values

    @staticmethod
    async def read_landmarks_by_name_list(session: AsyncSession, landmark_names: List[str]):
        result = await session.execute_read(Reader._read_landmarks_by_name_list, landmark_names)
        await logger.debug(f"method:\tread_landmarks_by_names,\nresult:\t{result}")
        return result

    @staticmethod
    async def _read_landmarks_by_name(tx, landmark_name: str, limit: int):
        """Transaction handler for read_landmarks_by_name"""
        result = await tx.run(
            """
            MATCH (landmark: Landmark)
                WHERE landmark.name STARTS WITH $landmark_name
            RETURN
                landmark,
                COLLECT {
                    MATCH (landmark)-[:REFERS]->(category:LandmarkCategory)
                    RETURN category.name AS category_name
                } AS categories_names 
                    ORDER BY landmark.name ASC
                    LIMIT $limit
            """,
            landmark_name=landmark_name,
            limit=limit
        )
        try:
            result_values = [record.data("landmark", "categories_names") async for record in result]
        except IndexError as ex:
            await logger.error(f"Index error, args: {ex.args[0]}")
            result_values = []

        await logger.debug(f"method:\t_read_landmarks_by_name,\nresult:\t{await result.consume()}")
        return result_values

    @staticmethod
    async def read_landmarks_by_name(session: AsyncSession, landmark_name: str, limit: int):
        result = await session.execute_read(Reader._read_landmarks_by_name, landmark_name, limit)
        await logger.debug(f"method:\tread_landmarks_by_names,\nresult:\t{result}")
        return result

    @staticmethod
    async def _read_landmarks_of_categories_in_region(
            tx, region_name: str, categories_names: List[str], optional_limit
    ):
        """Transaction handler for read_landmarks_of_categories_in_region"""
        result = await tx.run(
            """
            MATCH (region: Region)
                WHERE region.name STARTS WITH $region_name
            WITH region
                ORDER BY region.name
                LIMIT 1
            UNWIND $categories_names AS category_name
            CALL {
                WITH category_name
                MATCH (category: LandmarkCategory)
                    WHERE category.name STARTS WITH category_name
                RETURN category
                    ORDER BY category.name
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
    async def _read_landmarks_by_region(tx, region_name: str, optional_limit: int = None):
        """Transaction handler for read_landmarks_by_region"""
        result = await tx.run(
            """
            MATCH (region: Region)
                WHERE region.name STARTS WITH $region_name
            WITH region
                ORDER BY region.name
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
            MATCH (region: Region)
                WHERE region.name STARTS WITH $region_name
            WITH region
                ORDER BY region.name
                LIMIT 1
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
                MATCH (mapSector: MapSector)
                    WHERE mapSector.name STARTS WITH map_sector_name
                RETURN mapSector
                    ORDER BY mapSector.name
                    LIMIT 1
            }
            WITH mapSector
            UNWIND $categories_names AS category_name
            CALL {
                WITH category_name
                MATCH (category: LandmarkCategory)
                    WHERE category.name STARTS WITH category_name
                RETURN category
                    ORDER BY category.name
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
            MATCH (note: Note)
                WHERE note.title STARTS WITH $note_title
            WITH note
                ORDER BY note.title
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
                    MATCH (note_category: NoteCategory)
                        WHERE note_category.name STARTS WITH note_category_name
                    RETURN note_category
                        ORDER BY note_category.name
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
    async def _read_recommendations_by_coordinates(tx, coordinates_of_points: List[Dict[str, float]], limit: int):
        """Transaction handler for read_recommendations_by_coordinates"""
        result = await tx.run(
            """
            UNWIND $coordinates_of_points AS coordinates_of_point
                WITH coordinates_of_point
                OPTIONAL MATCH (mapSector: MapSector)
                    WHERE
                        mapSector.tl_longitude <= toFloat(coordinates_of_point.longitude) AND
                        mapSector.tl_latitude >= toFloat(coordinates_of_point.latitude) AND
                        point.withinBBox(
                            point({latitude: coordinates_of_point.latitude, longitude: coordinates_of_point.longitude, crs:'WGS-84'}),
                            point({latitude: mapSector.br_latitude, longitude: mapSector.tl_longitude, crs:'WGS-84'}),
                            point({latitude: mapSector.tl_latitude, longitude: mapSector.br_longitude, crs:'WGS-84'})
                        )
                OPTIONAL MATCH
                    (mapSector) ((:MapSector)-[:NEIGHBOUR_SECTOR]-(:MapSector)){0,1} (recommendationSector: MapSector)
                        <-[:IN_SECTOR]-
                    (recommendedLandmark:Landmark)
                
                WITH
                    recommendedLandmark AS recommendation,
                    point.distance(
                        point({latitude: coordinates_of_point.latitude, longitude: coordinates_of_point.longitude, crs:'WGS-84'}),
                        point({latitude: recommendedLandmark.latitude, longitude: recommendedLandmark.longitude})
                    ) AS distance
                ORDER BY distance ASC
                
                RETURN DISTINCT
                    recommendation    
                LIMIT $limit
            """,
            coordinates_of_points=coordinates_of_points, limit=limit
        )
        try:
            result_values = [record.data("recommendation") async for record in result]
        except IndexError as ex:
            await logger.error(f"Index error, args: {ex.args[0]}")
            result_values = []

        await logger.debug(
            f"method:\t_read_recommendations_by_coordinates_and_categories\nresult:\t{await result.consume()}"
        )
        return result_values

    @staticmethod
    async def read_recommendations_by_coordinates(
            session: AsyncSession, coordinates_of_points: List[Dict[str, float]], limit: int
    ):
        result = await session.execute_read(
            Reader._read_recommendations_by_coordinates, coordinates_of_points, limit
        )
        await logger.debug(f"method:\tread_recommendations_by_coordinates,\nresult:\t{result}")
        return result

