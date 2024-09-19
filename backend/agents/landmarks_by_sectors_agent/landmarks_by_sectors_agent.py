import asyncio
import json
import redis

from aiologger.loggers.json import JsonLogger
from jsonschema import validate
from jsonschema.exceptions import ValidationError

from backend.agents.landmarks_by_sectors_agent.pure_landmarks_by_sectors_agent import PURELandmarksBySectorsAgent
from backend.broker.abstract_agents_broker import AbstractAgentsBroker
from backend.broker.agents_tasks.crud_agent_tasks import landmarks_of_categories_in_map_sectors_task, \
    landmarks_in_map_sectors_task, map_sectors_structure_of_region_task
from backend.agents.landmarks_by_sectors_agent.squares_params_json_validation import *

logger = JsonLogger.with_default_handlers(
    level="DEBUG",
    serializer_kwargs={'ensure_ascii': False},
)


class LandmarksBySectorsAgent(PURELandmarksBySectorsAgent):
    _cache = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)
    _result = {}
    _sectors = {}
    _cache_expiry = 3600

    LAT_DIFFERENCE = 0.312
    LONG_DIFFERENCE = 0.611
    CACHE_SECTORS_MAX_SIZE = 60
    CACHE_CATEGORIES_MAX_SIZE = 10
    MAP_SECTORS_NAMES = "map_sectors_names"
    CATEGORIES_NAMES = "categories_names"

    _single_landmarks_agent = None

    def __init__(self):
        super().__init__()

    @classmethod
    def get_landmarks_by_sectors_agent(cls):
        """
        Method to take crud agent object. Returns None in case when crud is not exists.
        :return: None | pure_landmarks_by_sectors_agent
        """
        return cls._single_landmarks_agent

    @classmethod
    def landmarks_by_sectors_agent_exists(cls) -> bool:
        """Method to check if crud object already exists"""
        if cls._single_landmarks_agent:
            return True
        else:
            return False

    @classmethod
    def create(cls):
        cls._single_landmarks_agent = LandmarksBySectorsAgent()
        return cls._single_landmarks_agent

    @classmethod
    async def get_sectors(cls):
        _region_sectors_async_task = asyncio.create_task(
            AbstractAgentsBroker.call_agent_task(
                map_sectors_structure_of_region_task,
                {"region_name": "Беларусь"}
            )
        )
        result_task = await _region_sectors_async_task
        cls._sectors = result_task.return_value

    @classmethod
    async def get_landmarks_in_sector(cls, json_params: dict):
        if not cls._sectors:
            await cls.get_sectors()

        # Check if format of dictionary is right using validator
        await cls._coords_of_square_validation(json_params)
        squares_in_sector = await cls.get_necessary_sectors(json_params)

        # Comparing with cache, then updating cache
        squares_in_sector[cls.MAP_SECTORS_NAMES] = [
            i for i in squares_in_sector[cls.MAP_SECTORS_NAMES] if i not in cls._cache.get(cls.MAP_SECTORS_NAMES)
        ]
        cls._set_cache(squares_in_sector)
        if len(squares_in_sector[cls.MAP_SECTORS_NAMES]) != 0:
            landmarks_sectors_async_task = asyncio.create_task(
                AbstractAgentsBroker.call_agent_task(
                    landmarks_in_map_sectors_task,
                    squares_in_sector
                )
            )
            result_task = await landmarks_sectors_async_task
            cls._result = result_task.return_value
        return cls._result

    @classmethod
    async def get_landmarks_by_categories_in_sector(cls, jsom_params: dict):
        if not cls._sectors:
            await cls.get_sectors()
        await cls._coords_of_square_with_categories_validation(jsom_params)
        squares_in_sector = await cls.get_necessary_sectors(jsom_params)
        squares_in_sector[cls.CATEGORIES_NAMES] = jsom_params[cls.CATEGORIES_NAMES]
        squares_in_sector[cls.MAP_SECTORS_NAMES] = [
            i for i in squares_in_sector[cls.MAP_SECTORS_NAMES] if i not in cls._cache.get(cls.MAP_SECTORS_NAMES)
        ]
        squares_in_sector[cls.CATEGORIES_NAMES] = [
            i for i in squares_in_sector[cls.CATEGORIES_NAMES] if i not in cls._cache.get(cls.CATEGORIES_NAMES)
        ]
        cls._set_cache(squares_in_sector)
        if len(squares_in_sector[cls.MAP_SECTORS_NAMES]) != 0:
            landmarks_sectors_categories_async_task = asyncio.create_task(
                AbstractAgentsBroker.call_agent_task(
                    landmarks_of_categories_in_map_sectors_task, squares_in_sector
                )
            )
            result_task = await landmarks_sectors_categories_async_task
            cls._result = result_task.return_value
        return cls._result

    @classmethod
    def _set_cache(cls, squares_in_sector: dict):
        """
        cls._cache is set from redis that prevents repeating of elements
        """
        cls._cache.ltrim(cls.MAP_SECTORS_NAMES, -cls.CACHE_SECTORS_MAX_SIZE, -1)
        cls._cache.ltrim(cls.CATEGORIES_NAMES, -cls.CACHE_CATEGORIES_MAX_SIZE, -1)
        for sector_name in squares_in_sector[cls.MAP_SECTORS_NAMES]:
            cls._cache.sadd(cls.MAP_SECTORS_NAMES, sector_name)
        if cls.CATEGORIES_NAMES in squares_in_sector.keys():
            for category in squares_in_sector[cls.CATEGORIES_NAMES]:
                cls._cache.sadd(cls.CATEGORIES_NAMES, category)
        
        cls._cache.expire(cls.MAP_SECTORS_NAMES, cls._cache_expiry)
        cls._cache.expire(cls.CATEGORIES_NAMES, cls._cache_expiry)
        

    @classmethod
    async def get_necessary_sectors(cls, coords_of_sector: dict):
        squares_in_sector = {cls.MAP_SECTORS_NAMES: []}
        for element in cls._sectors:
            if (coords_of_sector["TL"]["longitude"] - cls.LONG_DIFFERENCE <= element["TL"]["longitude"] <
                element["BR"]["longitude"] <=
                coords_of_sector["BR"]["longitude"] + cls.LONG_DIFFERENCE) and (
                    coords_of_sector["BR"]["latitude"] - cls.LAT_DIFFERENCE <= element["BR"]["latitude"] <
                    element["TL"]["latitude"] <=
                    coords_of_sector["TL"]["latitude"] + cls.LAT_DIFFERENCE):
                squares_in_sector[cls.MAP_SECTORS_NAMES].append(element["name"])
        return squares_in_sector

    @staticmethod
    async def _coords_of_square_validation(jsom_params: dict):
        try:
            validate(jsom_params, get_coords_of_map_sectors_json)
        except ValidationError as e:
            await logger.info(
                f"Validation error on json, args: {e.args[0]}, json_params: {get_coords_of_map_sectors_json}")
            raise ValidationError("Validation error")

    @staticmethod
    async def _coords_of_square_with_categories_validation(json_params: dict):
        try:
            validate(json_params, get_categories_of_landmarks_json)
        except ValidationError as e:
            await logger.info(
                f"Validation error on json, args: {e.args[0]}, json_params: {json_params}")
            raise ValidationError("Validation error")

    @classmethod
    def get_landmarks_by_sectors_agent(cls):
        """
        Method to take landmarks by sectors agent object. Returns None in case when landmarks by sectors agent is not exists.
        :return: None | PURELandmarksBySectorsAgent
        """
        return cls._single_landmarks_agent

    @classmethod
    def landmarks_by_sectors_agent_exists(cls) -> bool:
        """Method to check if landmarks by sectors agent object already exists"""
        if cls._single_landmarks_agent:
            return True
        else:
            return False
