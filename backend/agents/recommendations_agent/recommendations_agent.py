# Author: Vodohleb04
import asyncio
import torch
import backend.agents.recommendations_agent.recommendations_json_validation as json_validation
from typing import Dict, List
from jsonschema import validate, ValidationError
from aiologger.loggers.json import JsonLogger
from torch import nn
from backend.agents.recommendations_agent.pure_recommendations_agent import PureRecommendationsAgent
from backend.broker.abstract_agents_broker import AbstractAgentsBroker
from backend.broker.agents_tasks.crud_agent_tasks import crud_recommendations_by_coordinates_and_categories_task

logger = JsonLogger.with_default_handlers(
    level="DEBUG",
    serializer_kwargs={'ensure_ascii': False},
)


class RecommendationsAgent(PureRecommendationsAgent):
    _single_recommendations_agent = None

    @classmethod
    def get_recommendations_agent(cls):
        """
        Method to take recommendations agent object. Returns None in case when recommendations agent is not exists.
        :return: None | PureRecommendationsAgent
        """
        return cls._single_recommendations_agent

    @classmethod
    def recommendations_agent_exists(cls) -> bool:
        """Method to check if recommendations agent object already exists"""
        if cls._single_recommendations_agent:
            return True
        else:
            return False

    def __init__(self):
        if not self.recommendations_agent_exists():

            self._single_recommendations_agent = self
        else:
            raise RuntimeError("Unexpected behaviour, this class can have only one instance")

    @staticmethod
    def _outdated_remove_nones_from_kb_result(kb_pre_recommendations: List) -> List:
        """Changes list"""
        return [
            kb_pre_recommendations[i] for i in range(len(kb_pre_recommendations))
            if kb_pre_recommendations[i]["recommendation"]
        ]

    @staticmethod
    def _remove_nones_from_kb_result(kb_pre_recommendations: List) -> None:
        """Changes list"""
        i = 0
        len_bound = len(kb_pre_recommendations)
        while i < len_bound:
            if kb_pre_recommendations[i]["recommendation"] is None:
                kb_pre_recommendations.pop(i)
                len_bound -= 1
                continue
            i += 1

    @staticmethod
    def _landmarks_are_equal(left_landmark: Dict, right_landmark: Dict) -> bool:
        if left_landmark["name"] != right_landmark["name"]:
            return False
        if left_landmark["latitude"] != right_landmark["latitude"]:
            return False
        if left_landmark["longitude"] != right_landmark["longitude"]:
            return False
        return True

    @staticmethod
    def _remove_duplicates_from_kb_result(kb_pre_recommendations: List):
        """Changes list"""
        i = 0
        len_bound = len(kb_pre_recommendations)
        while i < len_bound:
            j = 0
            while j < len_bound:
                if i == j:
                    j += 1
                    continue
                if RecommendationsAgent._landmarks_are_equal(
                        kb_pre_recommendations[i]["recommendation"], kb_pre_recommendations[j]["recommendation"]
                ):
                    len_bound -= 1
                    if kb_pre_recommendations[i]["distance"] <= kb_pre_recommendations[j]["distance"]:
                        kb_pre_recommendations.pop(j)
                        continue
                    else:
                        kb_pre_recommendations.pop(i)
                        i -= 1  # To make increase == 0 (i + 1 - 1 == i)
                        break
                j += 1
            i += 1

    @staticmethod
    def _json_params_validation(json_params):
        """This method checks values only of special params. Other values will be checked in target agent."""
        validate(json_params, json_validation.find_recommendations_for_coordinates_and_categories)
        if json_params["maximum_amount_of_recommendations"] and json_params["maximum_amount_of_recommendations"] <= 0:
            raise ValidationError("maximum_amount_of_recommendations can\'t be less or equal to zero")
        if json_params["amount_of_recommendations_for_point"] and \
                json_params["amount_of_recommendations_for_point"] <= 0:
            raise ValidationError("amount_of_recommendations_for_point can\'t be less or equal to zero")
        if json_params["optional_limit"] and json_params["optional_limit"] <= 0:
            raise ValidationError("optional_limit can\'t be less or equal to zero")

    @staticmethod
    async def _kb_pre_recommendation_by_coordinates_and_categories(json_params: Dict):
        recommendations_async_task = asyncio.create_task(
            AbstractAgentsBroker.call_agent_task(crud_recommendations_by_coordinates_and_categories_task, json_params)
        )
        kb_pre_recommendation_asyncio_result = await recommendations_async_task
        logger.debug(
            f"Recommendations agent, find_recommendations_for_coordinates_and_categories, "
            f"kb_pre_recommendation_asyncio_result: {kb_pre_recommendation_asyncio_result}"
        )
        kb_pre_recommendations = kb_pre_recommendation_asyncio_result.return_value
        return kb_pre_recommendations

    async def _find_recommendations_for_coordinates_and_categories(
            self, recommendations, maximum_amount_of_recommendations
    ):
        # TODO Cash request
        # TODO check cash on None values
        pass


    async def find_recommendations_for_coordinates_and_categories(self, json_params: Dict):
        try:
            self._json_params_validation(json_params)
            maximum_amount_of_recommendations = json_params["maximum_amount_of_recommendations"]
            json_params.pop("maximum_amount_of_recommendations")
        except ValidationError as ex:
            await logger.error(f"find_recommendations_for_coordinates_and_categories, ValidationError({ex.args[0]})")
            return []  # raise ValidationError

        kb_pre_recommendations = await self._kb_pre_recommendation_by_coordinates_and_categories(json_params)
        self._remove_nones_from_kb_result(kb_pre_recommendations)
        logger.debug(
            f"Recommendations agent, find_recommendations_for_coordinates_and_categories, "
            f"kb_pre_recommendations after None removed: {kb_pre_recommendations}"
        )
        if not kb_pre_recommendations:
            return kb_pre_recommendations
        self._remove_duplicates_from_kb_result(kb_pre_recommendations)
        logger.debug(
            f"Recommendations agent, find_recommendations_for_coordinates_and_categories, "
            f"kb_pre_recommendations after duplicates removed: {kb_pre_recommendations}"
        )
        return await self._find_recommendations_for_coordinates_and_categories(
            kb_pre_recommendations, maximum_amount_of_recommendations
        )
