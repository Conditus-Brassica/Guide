#Author: Vodohleb04
"""
CRUD Agent modul
https://sefon.pro/mp3/474614-sektor-gaza-narkoman/
"""
import asyncio
from typing import Dict, List
from jsonschema import ValidationError, validate
from neo4j import AsyncDriver
from aiologger.loggers.json import JsonLogger
from backend.agents.crud_agent.pure_crud_agent import PureCRUDAgent
from backend.agents.crud_agent.reader import Reader
from backend.agents.crud_agent.creator import Creator
from backend.agents.crud_agent.crud_json_validation import *


logger = JsonLogger.with_default_handlers(
    level="DEBUG",
    serializer_kwargs={'ensure_ascii': False},
)


class CRUDAgent(PureCRUDAgent):
    _single_crud = None
    _kb_driver = None
    _knowledgebase_name = None

    @classmethod
    async def close(cls):
        if cls._kb_driver:
            await cls._kb_driver.close()
            await logger.info("Driver closed")

    @classmethod
    def get_crud(cls):
        """
        Method to take crud agent object. Returns None in case when crud is not exists.
        :return: None | PureCRUDAgent
        """
        return cls._single_crud

    @classmethod
    def crud_exists(cls) -> bool:
        """Method to check if crud object already exists"""
        if cls._single_crud:
            return True
        else:
            return False

    @classmethod
    def _class_init(cls, async_kb_driver: AsyncDriver, knowledgebase_name: str):
        """
        :param async_kb_driver: async driver of knowledge base
        :param knowledgebase_name: name of knowledgebase to query
        """
        cls._kb_driver = async_kb_driver
        cls._knowledgebase_name = knowledgebase_name

    def __init__(self, async_kb_driver: AsyncDriver, knowledgebase_name: str):
        """
        :param async_kb_driver: async driver of knowledge base
        :param knowledgebase_name: name of knowledgebase to query
        """
        if not self._single_crud:
            self._class_init(async_kb_driver, knowledgebase_name)
            self._single_crud = self
        else:
            raise RuntimeError("Unexpected behaviour, this class can have only one instance")

    # Read queries
    @classmethod
    async def get_categories_of_region(cls, json_params: Dict):
        async def session_runner(region_name: str, optional_limit: int = None):
            async with cls._kb_driver.session(database=cls._knowledgebase_name) as session:
                return await Reader.read_categories_of_region(session, region_name, optional_limit)

        try:
            validate(json_params, get_categories_of_region_json)
            json_params["optional_limit"] = json_params.get("optional_limit", None)
            if json_params["optional_limit"] and json_params["optional_limit"] <= 0:
                raise ValidationError("optional_limit can\'t be less or equal to zero")
            return await asyncio.shield(
                session_runner(json_params["region_name"], json_params["optional_limit"])
            )
        except ValidationError as ex:
            await logger.error(f"Validation error on json, args: {ex.args[0]}, json_params: {json_params}")
            return []  # raise ValidationError

    @classmethod
    async def get_landmarks_in_map_sectors(cls, json_params: Dict):
        async def session_runner(map_sectors_names: List[str], optional_limit: int = None):
            async with cls._kb_driver.session(database=cls._knowledgebase_name) as session:
                return await Reader.read_landmarks_in_map_sectors(session, map_sectors_names, optional_limit)

        try:
            validate(json_params, get_landmarks_in_map_sectors_json)
            json_params["optional_limit"] = json_params.get("optional_limit", None)
            if json_params["optional_limit"] and json_params["optional_limit"] <= 0:
                raise ValidationError("optional_limit can\'t be less or equal to zero")
            return await asyncio.shield(
                session_runner(json_params["map_sectors_names"], json_params["optional_limit"])
            )
        except ValidationError as ex:
            await logger.error(f"get_landmarks_in_map_sectors. "
                               f"Validation error on json, args: {ex.args[0]}, json_params: {json_params}")
            return []  # raise ValidationError

    @classmethod
    async def get_landmarks_refers_to_categories(cls, json_params: Dict):
        async def session_runner(map_sectors_names: List[str], optional_limit: int = None):
            async with cls._kb_driver.session(database=cls._knowledgebase_name) as session:
                return await Reader.read_landmarks_refers_to_categories(
                    session, map_sectors_names, optional_limit
                )

        try:
            validate(json_params, get_landmarks_refers_to_categories_json)
            json_params["optional_limit"] = json_params.get("optional_limit", None)
            if json_params["optional_limit"] and json_params["optional_limit"] <= 0:
                raise ValidationError("optional_limit can\'t be less or equal to zero")
            return await asyncio.shield(
                session_runner(json_params["categories_names"], json_params["optional_limit"])
            )
        except ValidationError as ex:
            await logger.error(f"get_landmarks_refers_to_categories. "
                               f"Validation error on json, args: {ex.args[0]}, json_params: {json_params}")
            return []  # raise ValidationError

    @classmethod
    async def get_landmarks_by_coordinates_and_name(cls, json_params: Dict):
        async def session_runner(
            coordinates_name_list: List[Dict[str, float | str]], optional_limit: int = None
        ):
            async with cls._kb_driver.session(database=cls._knowledgebase_name) as session:
                return await Reader.read_landmarks_by_coordinates_and_name(
                    session, coordinates_name_list, optional_limit
                )

        try:
            validate(json_params, get_landmarks_by_coordinates_and_name_json)
            json_params["optional_limit"] = json_params.get("optional_limit", None)
            if json_params["optional_limit"] and json_params["optional_limit"] <= 0:
                raise ValidationError("optional_limit can\'t be less or equal to zero")
            return await asyncio.shield(
                session_runner(json_params["coordinates_name_list"], json_params["optional_limit"])
            )
        except ValidationError as ex:
            await logger.error(f"get_landmarks_by_coordinates_and_name. "
                               f"Validation error on json, args: {ex.args[0]}, json_params: {json_params}")
            return []  # raise ValidationError

    @classmethod
    async def get_landmarks_by_name_list(cls, json_params: Dict):
        async def session_runner(landmark_names: List[str]):
            async with cls._kb_driver.session(database=cls._knowledgebase_name) as session:
                return await Reader.read_landmarks_by_name_list(session, landmark_names)

        try:
            validate(json_params, get_landmarks_by_name_list_json)
            return await asyncio.shield(
                session_runner(json_params["landmark_names"])
            )
        except ValidationError as ex:
            await logger.error(f"get_landmarks_by_name_list. "
                               f"Validation error on json, args: {ex.args[0]}, json_params: {json_params}")
            return []  # raise ValidationError

    @classmethod
    async def get_landmarks_by_name(cls, json_params: Dict):
        async def session_runner(landmark_name: str, limit: int):
            async with cls._kb_driver.session(database=cls._knowledgebase_name) as session:
                return await Reader.read_landmarks_by_name(session, landmark_name, limit)

        try:
            validate(json_params, get_landmarks_by_name_json)
            return await asyncio.shield(
                session_runner(json_params["landmark_name"], json_params["limit"])
            )
        except ValidationError as ex:
            await logger.error(f"get_landmarks_by_name. "
                               f"Validation error on json, args: {ex.args[0]}, json_params: {json_params}")
            return []  # raise ValidationError

    @classmethod
    async def get_landmarks_of_categories_in_region(cls, json_params: Dict):
        async def session_runner(region_name: str, categories_names: List[str], optional_limit: int = None):
            async with cls._kb_driver.session(database=cls._knowledgebase_name) as session:
                return await Reader.read_landmarks_of_categories_in_region(
                    session, region_name, categories_names, optional_limit
                )

        try:
            validate(json_params, get_landmarks_of_categories_in_region_json)
            json_params["optional_limit"] = json_params.get("optional_limit", None)
            if json_params["optional_limit"] and json_params["optional_limit"] <= 0:
                raise ValidationError("optional_limit can\'t be less or equal to zero")
            return await asyncio.shield(
                session_runner(
                    json_params["region_name"], json_params["categories_names"], json_params["optional_limit"]
                )
            )
        except ValidationError as ex:
            await logger.error(f"get_landmarks_of_categories_in_region. "
                               f"Validation error on json, args: {ex.args[0]}, json_params: {json_params}")
            return []  # raise ValidationError

    @classmethod
    async def get_landmarks_by_region(cls, json_params: Dict):
        async def session_runner(region_name: str, optional_limit: int = None):
            async with cls._kb_driver.session(database=cls._knowledgebase_name) as session:
                return await Reader.read_landmarks_by_region(session, region_name, optional_limit)

        try:
            validate(json_params, get_landmarks_by_region_json)
            json_params["optional_limit"] = json_params.get("optional_limit", None)
            if json_params["optional_limit"] and json_params["optional_limit"] <= 0:
                raise ValidationError("optional_limit can\'t be less or equal to zero")
            return await asyncio.shield(
                session_runner(json_params["region_name"], json_params["optional_limit"])
            )
        except ValidationError as ex:
            await logger.error(f"get_landmarks_by_region. "
                               f"Validation error on json, args: {ex.args[0]}, json_params: {json_params}")
            return []  # raise ValidationError

    @classmethod
    async def get_map_sectors_of_points(cls, json_params: Dict):
        async def session_runner(coordinates_of_points: List[Dict[str, float]], optional_limit: int = None):
            async with cls._kb_driver.session(database=cls._knowledgebase_name) as session:
                return await Reader.read_map_sectors_of_points(session, coordinates_of_points, optional_limit)

        try:

            validate(json_params, get_map_sectors_of_points)
            json_params["optional_limit"] = json_params.get("optional_limit", None)
            if json_params["optional_limit"] and json_params["optional_limit"] <= 0:
                raise ValidationError("optional_limit can\'t be less or equal to zero")
            return await asyncio.shield(
                session_runner(json_params["coordinates_of_points"], json_params["optional_limit"])
            )
        except ValidationError as ex:
            await logger.error(f"get_map_sectors_of_points. "
                               f"Validation error on json, args: {ex.args[0]}, json_params: {json_params}")
            return []  # raise ValidationError

    @classmethod
    async def get_map_sectors_structure_of_region(cls, json_params: Dict):
        async def session_runner(region_name: str):
            async with cls._kb_driver.session(database=cls._knowledgebase_name) as session:
                return await Reader.read_map_sectors_structure_of_region(session, region_name)

        try:
            validate(json_params, get_map_sectors_structure_of_region)
            return await asyncio.shield(
                session_runner(json_params["region_name"])
            )
        except ValidationError as ex:
            await logger.error(f"get_map_sectors_structure_of_region. "
                               f"Validation error on json, args: {ex.args[0]}, json_params: {json_params}")
            return []  # raise ValidationError

    @classmethod
    async def get_landmarks_of_categories_in_map_sectors(cls, json_params: Dict):
        async def session_runner(map_sectors_names: List[str], categories_names: List[str], optional_limit: int = None):
            async with cls._kb_driver.session(database=cls._knowledgebase_name) as session:
                return await Reader.read_landmarks_of_categories_in_map_sectors(
                    session, map_sectors_names, categories_names, optional_limit
                )

        try:
            validate(json_params, get_landmarks_of_categories_in_map_sectors)
            json_params["optional_limit"] = json_params.get("optional_limit", None)
            if json_params["optional_limit"] and json_params["optional_limit"] <= 0:
                raise ValidationError("optional_limit can\'t be less or equal to zero")
            return await asyncio.shield(
                session_runner(
                    json_params["map_sectors_names"],
                    json_params["categories_names"],
                    json_params["optional_limit"]
                )
            )
        except ValidationError as ex:
            await logger.error(f"get_landmarks_of_categories_in_map_sectors. "
                               f"Validation error on json, args: {ex.args[0]}, json_params: {json_params}")
            return []  # raise ValidationError

    @classmethod
    async def get_route_landmarks_by_index_id(cls, json_params: Dict):
        async def session_runner(index_id: int):
            async with cls._kb_driver.session(database=cls._knowledgebase_name) as session:
                return await Reader.read_route_landmarks_by_index_id(session, index_id)

        try:
            validate(json_params, get_route_landmarks_by_index_id)
            return await asyncio.shield(
                session_runner(json_params["index_id"])
            )
        except ValidationError as ex:
            await logger.error(f"get_route_landmarks_by_index_id. "
                               f"Validation error on json, args: {ex.args[0]}, json_params: {json_params}")
            return []  # raise ValidationError

    @classmethod
    async def get_routes_saved_by_user(cls, json_params: Dict):
        async def session_runner(user_login: str):
            async with cls._kb_driver.session(database=cls._knowledgebase_name) as session:
                return await Reader.read_routes_saved_by_user(session, user_login)

        try:
            validate(json_params, get_routes_saved_by_user)
            return await asyncio.shield(
                session_runner(json_params["user_login"])
            )
        except ValidationError as ex:
            await logger.error(f"get_routes_saved_by_user. "
                               f"Validation error on json, args: {ex.args[0]}, json_params: {json_params}")
            return []  # raise ValidationError

    @classmethod
    async def get_range_of_routes_saved_by_user(cls, json_params: Dict):
        async def session_runner(user_login: str, skip: int, limit: int):
            async with cls._kb_driver.session(database=cls._knowledgebase_name) as session:
                return await Reader.read_range_of_routes_saved_by_user(session, user_login, skip, limit)

        try:
            validate(json_params, get_range_of_routes_saved_by_user)
            if json_params["skip"] < 0:
                raise ValidationError("skip can\'t be less than zero")
            if json_params["limit"] <= 0:
                raise ValidationError("limit can\'t be less or equal to zero")
            return await asyncio.shield(
                session_runner(
                    json_params["user_login"],
                    json_params["skip"],
                    json_params["limit"]
                )
            )
        except ValidationError as ex:
            await logger.error(f"get_range_of_routes_saved_by_user. "
                               f"Validation error on json, args: {ex.args[0]}, json_params: {json_params}")
            return []  # raise ValidationError

    @classmethod
    async def get_note_by_title(cls, json_params: Dict):
        async def session_runner(note_title: str):
            async with cls._kb_driver.session(database=cls._knowledgebase_name) as session:
                return await Reader.read_note_by_title(session, note_title)

        try:
            validate(json_params, get_note_by_title)
            return await asyncio.shield(
                session_runner(json_params["note_title"])
            )
        except ValidationError as ex:
            await logger.error(f"get_note_by_title. "
                               f"Validation error on json, args: {ex.args[0]}, json_params: {json_params}")
            return []  # raise ValidationError

    @classmethod
    async def get_notes_in_range(cls, json_params: Dict):
        async def session_runner(skip: int, limit: int):
            async with cls._kb_driver.session(database=cls._knowledgebase_name) as session:
                return await Reader.read_notes_in_range(session, skip, limit)

        try:
            validate(json_params, get_notes_in_range)
            if json_params["skip"] < 0:
                raise ValidationError("skip can\'t be less than zero")
            if json_params["limit"] <= 0:
                raise ValidationError("limit can\'t be less or equal to zero")
            return await asyncio.shield(
                session_runner(
                    json_params["skip"],
                    json_params["limit"]
                )
            )
        except ValidationError as ex:
            await logger.error(f"get_notes_in_range. "
                               f"Validation error on json, args: {ex.args[0]}, json_params: {json_params}")
            return []  # raise ValidationError

    @classmethod
    async def get_notes_of_categories_in_range(cls, json_params: Dict):
        async def session_runner(note_categories_names: List[str], skip: int, limit: int):
            async with cls._kb_driver.session(database=cls._knowledgebase_name) as session:
                return await Reader.read_notes_of_categories_in_range(session, note_categories_names, skip, limit)

        try:
            validate(json_params, get_notes_of_categories_in_range)
            if json_params["skip"] < 0:
                raise ValidationError("skip can\'t be less than zero")
            if json_params["limit"] <= 0:
                raise ValidationError("limit can\'t be less or equal to zero")
            return await asyncio.shield(
                session_runner(
                    json_params["note_categories_names"],
                    json_params["skip"],
                    json_params["limit"]
                )
            )
        except ValidationError as ex:
            await logger.error(f"get_notes_in_range. "
                               f"Validation error on json, args: {ex.args[0]}, json_params: {json_params}")
            return []  # raise ValidationError

    @classmethod
    async def get_recommendations_by_coordinates(cls, json_params: Dict):
        async def session_runner(coordinates_of_points: List[Dict[str, float]], limit: int):
            async with cls._kb_driver.session(database=cls._knowledgebase_name) as session:
                return await Reader.read_recommendations_by_coordinates(
                    session, coordinates_of_points, limit
                )

        try:
            validate(json_params, get_recommendations_by_coordinates)
            if json_params["limit"] <= 0:
                raise ValidationError("limit can\'t be less or equal to zero")
            return await asyncio.shield(
                session_runner(json_params["coordinates_of_points"], json_params["limit"])
            )
        except ValidationError as ex:
            await logger.error(f"get_recommendations_by_coordinates. "
                               f"Validation error on json, args: {ex.args[0]}, json_params: {json_params}")
            return []  # raise ValidationError

    # Write queries

    @classmethod
    async def put_user(cls, json_params: Dict):
        async def session_runner(user_login: str):
            async with cls._kb_driver.session(database=cls._knowledgebase_name) as session:
                return await Creator.write_user(session, user_login)

        try:
            validate(json_params, put_user)
            return await asyncio.shield(
                session_runner(json_params["user_login"])
            )
        except ValidationError as ex:
            await logger.error(f"put_user. "
                               f"Validation error on json, args: {ex.args[0]}, json_params: {json_params}")
            return []  # raise ValidationError

    @classmethod
    async def put_note(cls, json_params: Dict):
        async def session_runner(
                guide_login: str, country_names: List[str], note_title: str, note_category_names: List[str]
        ):
            async with cls._kb_driver.session(database=cls._knowledgebase_name) as session:
                return await Creator.write_note(
                    session, guide_login, country_names, note_title, note_category_names
                )

        try:
            validate(json_params, put_note)
            return await asyncio.shield(
                session_runner(
                    json_params["guide_login"],
                    json_params["country_names"],
                    json_params["note_title"],
                    json_params["note_category_names"]
                )
            )
        except ValidationError as ex:
            await logger.error(f"put_note. "
                               f"Validation error on json, args: {ex.args[0]}, json_params: {json_params}")
            return []  # raise ValidationError

    @classmethod
    async def put_route_for_note(cls, json_params: Dict):
        async def session_runner(note_title: str, landmark_info_position_dicts: List[Dict[str, str | int | float]]):
            async with cls._kb_driver.session(database=cls._knowledgebase_name) as session:
                return await Creator.write_route_for_note(
                    session, note_title, landmark_info_position_dicts
                )

        try:
            validate(json_params, put_route_for_note)
            return await asyncio.shield(
                session_runner(
                    json_params["note_title"],
                    json_params["landmark_info_position_dicts"]
                )
            )
        except ValidationError as ex:
            await logger.error(f"put_route_for_note. "
                               f"Validation error on json, args: {ex.args[0]}, json_params: {json_params}")
            return []  # raise ValidationError

    @classmethod
    async def put_route_saved_by_user(cls, json_params: Dict):
        async def session_runner(user_login: str, landmark_info_position_dicts: List[Dict[str, str | int | float]]):
            async with cls._kb_driver.session(database=cls._knowledgebase_name) as session:
                return await Creator.write_route_saved_by_user(session, user_login, landmark_info_position_dicts)

        try:
            validate(json_params, put_route_saved_by_user)
            return await asyncio.shield(
                session_runner(
                    json_params["user_login"], json_params["landmark_info_position_dicts"]
                )
            )
        except ValidationError as ex:
            await logger.error(f"put_route_saved_by_user. "
                               f"Validation error on json, args: {ex.args[0]}, json_params: {json_params}")
            return []  # raise ValidationError

    @classmethod
    async def put_saved_relationship_for_existing_route(cls, json_params: Dict):
        async def session_runner(user_login: str, index_id: int):
            async with cls._kb_driver.session(database=cls._knowledgebase_name) as session:
                return await Creator.write_saved_relationship_for_existing_route(
                    session, user_login, index_id
                )

        try:
            validate(json_params, saved_relationship_for_existing_route)
            return await asyncio.shield(
                session_runner(json_params["user_login"], json_params["index_id"])
            )
        except ValidationError as ex:
            await logger.error(f"put_saved_relationship_for_existing_route. "
                               f"Validation error on json, args: {ex.args[0]}, json_params: {json_params}")
            return []  # raise ValidationError
