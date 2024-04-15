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
from backend.agents.crud_agent.pure_crud_classes.pure_crud_agent import PureCRUDAgent
from backend.agents.crud_agent.pure_crud_classes.pure_reader import PureReader
from backend.agents.crud_agent.crud_json_validation import *


logger = JsonLogger.with_default_handlers(
    level="DEBUG",
    serializer_kwargs={'ensure_ascii': False},
)


class CRUDAgent(PureCRUDAgent):
    _single_crud = None
    _reader = None
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
    def _class_init(cls, reader: PureReader, async_kb_driver: AsyncDriver, knowledgebase_name: str):
        """
        :param reader: reader for agent
        :param async_kb_driver: async driver of knowledge base
        :param knowledgebase_name: name of knowledgebase to query
        """
        cls._reader = reader
        cls._kb_driver = async_kb_driver
        cls._knowledgebase_name = knowledgebase_name

    def __init__(self, reader: PureReader, async_kb_driver: AsyncDriver, knowledgebase_name: str):
        """
        :param reader: reader for agent
        :param async_kb_driver: async driver of knowledge base
        :param knowledgebase_name: name of knowledgebase to query
        """
        if not self._single_crud:
            self._class_init(reader, async_kb_driver, knowledgebase_name)
            self._single_crud = self
        else:
            raise RuntimeError("Unexpected behaviour, this class can have only one instance")

    @classmethod
    async def get_categories_of_region(cls, json_params: Dict):
        async def session_runner(region_name: str, optional_limit: int = None):
            async with cls._kb_driver.session(database=cls._knowledgebase_name) as session:
                return await cls._reader.read_categories_of_region(session, region_name, optional_limit)

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
                return await cls._reader.read_landmarks_in_map_sectors(session, map_sectors_names, optional_limit)

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
                return await cls._reader.read_landmarks_refers_to_categories(
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
    async def get_landmarks_by_coordinates(cls, json_params: Dict):
        async def session_runner(coordinates: List[Dict[str, float]], optional_limit: int = None):
            async with cls._kb_driver.session(database=cls._knowledgebase_name) as session:
                return await cls._reader.read_landmarks_by_coordinates(session, coordinates, optional_limit)

        try:
            validate(json_params, get_landmarks_by_coordinates_json)
            json_params["optional_limit"] = json_params.get("optional_limit", None)
            if json_params["optional_limit"] and json_params["optional_limit"] <= 0:
                raise ValidationError("optional_limit can\'t be less or equal to zero")
            return await asyncio.shield(
                session_runner(json_params["coordinates"], json_params["optional_limit"])
            )
        except ValidationError as ex:
            await logger.error(f"get_landmarks_by_coordinates. "
                               f"Validation error on json, args: {ex.args[0]}, json_params: {json_params}")
            return []  # raise ValidationError

    @classmethod
    async def get_landmarks_by_names(cls, json_params: Dict):
        async def session_runner(landmark_names: List[str], optional_limit: int = None):
            async with cls._kb_driver.session(database=cls._knowledgebase_name) as session:
                return await cls._reader.read_landmarks_by_names(session, landmark_names, optional_limit)

        try:
            validate(json_params, get_landmarks_by_names_json)
            json_params["optional_limit"] = json_params.get("optional_limit", None)
            if json_params["optional_limit"] and json_params["optional_limit"] <= 0:
                raise ValidationError("optional_limit can\'t be less or equal to zero")
            return await asyncio.shield(
                session_runner(json_params["landmark_names"], json_params["optional_limit"])
            )
        except ValidationError as ex:
            await logger.error(f"get_landmarks_by_names. "
                               f"Validation error on json, args: {ex.args[0]}, json_params: {json_params}")
            return []  # raise ValidationError

    @classmethod
    async def get_landmarks_of_categories_in_region(cls, json_params: Dict):
        async def session_runner(region_name: str, categories_names: List[str], optional_limit: int = None):
            async with cls._kb_driver.session(database=cls._knowledgebase_name) as session:
                return await cls._reader.read_landmarks_of_categories_in_region(
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
                return await cls._reader.read_landmarks_by_region(session, region_name, optional_limit)

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
    async def get_recommendations_for_landmark_by_region(cls, json_params: Dict):
        async def session_runner(
                user_login: str,
                current_latitude: float,
                current_longitude: float,
                current_name: str,
                amount_of_recommendations: int
        ):
            async with cls._kb_driver.session(database=cls._knowledgebase_name) as session:
                return await cls._reader.read_recommendations_for_landmark_by_region(
                    session, user_login, current_latitude, current_longitude, current_name, amount_of_recommendations
                )

        try:
            validate(json_params, get_recommendations_for_landmark_by_region_json)
            return await asyncio.shield(
                session_runner(
                    json_params["user_login"], json_params["current_latitude"], json_params["current_longitude"],
                    json_params["current_name"], json_params["amount_of_recommendations"]
                )
            )
        except ValidationError as ex:
            await logger.error(f"get_recommendations_for_landmark_by_region. "
                               f"Validation error on json, args: {ex.args[0]}, json_params: {json_params}")
            return []  # raise ValidationError

    @classmethod
    async def get_map_sectors_of_points(cls, json_params: Dict):
        async def session_runner(coordinates_of_points: List[Dict[str, float]], optional_limit: int = None):
            async with cls._kb_driver.session(database=cls._knowledgebase_name) as session:
                return await cls._reader.read_map_sectors_of_points(session, coordinates_of_points, optional_limit)

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
    async def get_landmarks_of_categories_in_map_sectors(cls, json_params: Dict):
        async def session_runner(map_sectors_names: List[str], categories_names: List[str], optional_limit: int = None):
            async with cls._kb_driver.session(database=cls._knowledgebase_name) as session:
                return await cls._reader.read_landmarks_of_categories_in_map_sectors(
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
    async def get_recommendations_by_coordinates_and_categories(cls, json_params: Dict):
        async def session_runner(
                coordinates_of_points: List[Dict[str, float]],
                categories_names: List[str],
                user_login: str,
                amount_of_recommendations_for_point: int,
                optional_limit: int | None
        ):
            async with cls._kb_driver.session(database=cls._knowledgebase_name) as session:
                return await cls._reader.read_recommendations_by_coordinates_and_categories(
                    session, coordinates_of_points, categories_names, user_login, amount_of_recommendations_for_point,
                    optional_limit
                )

        try:
            validate(json_params, get_recommendations_by_coordinates_and_categories)
            json_params["optional_limit"] = json_params.get("optional_limit", None)
            if json_params["optional_limit"] and json_params["optional_limit"] <= 0:
                raise ValidationError("optional_limit can\'t be less or equal to zero")
            return await asyncio.shield(
                session_runner(
                    json_params["coordinates_of_points"], json_params["categories_names"], json_params["user_login"],
                    json_params["amount_of_recommendations_for_point"], json_params["optional_limit"]
                )
            )
        except ValidationError as ex:
            await logger.error(f"get_recommendations_by_coordinates_and_categories. "
                               f"Validation error on json, args: {ex.args[0]}, json_params: {json_params}")
            return []  # raise ValidationError
