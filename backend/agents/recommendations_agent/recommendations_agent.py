# Author: Vodohleb04
import asyncio
import backend.agents.recommendations_agent.recommendations_json_validation as json_validation
from typing import Dict, List, Tuple
from enum import Enum
from jsonschema import validate, ValidationError
from aiologger.loggers.json import JsonLogger
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

    @property
    def coefficients(self) -> Dict:
        return self.__coefficients

    def __init__(self, coefficients: Dict[str, float]):
        if not self.recommendations_agent_exists():
            validate(coefficients, json_validation.recommendations_agent_coefficients_json)
            self.__coefficients = coefficients
            self._single_recommendations_agent = self
        else:
            raise RuntimeError("Unexpected behaviour, this class can have only one instance")

    @staticmethod
    def _find_params_unifiers(user_categories_preference, a_priori_recommended):
        params_unifiers = {}
        logger.debug(
            f"Recommendations agent, _find_params_unifiers, user_categories_preference: {user_categories_preference}"
        )
        logger.debug(
            f"Recommendations agent, _find_params_unifiers, a_priori_recommended: {a_priori_recommended}"
        )
        max_preference_value = max(user_categories_preference.values())
        if not max_preference_value or max_preference_value == 0:
            params_unifiers["user_categories_preference"] = 1
        else:
            params_unifiers["user_categories_preference"] = max_preference_value
        max_distance = max([recommended["distance"] for recommended in a_priori_recommended])
        if not max_distance or max_distance == 0:
            params_unifiers["distance"] = 1
        else:
            params_unifiers["distance"] = max_distance
        params_unifiers["wish_to_visit"] = 1
        max_visited_amount = max([recommended["visited_amount"] for recommended in a_priori_recommended])
        if not max_visited_amount or max_visited_amount == 0:
            params_unifiers["visited_amount"] = 1
        else:
            params_unifiers["visited_amount"] = max_visited_amount
        return params_unifiers

    @staticmethod
    def _outdated_remove_nones_from_kb_result(a_priori_recommended: List) -> List:
        """Changes list"""
        return [
            a_priori_recommended[i] for i in range(len(a_priori_recommended))
            if a_priori_recommended[i]["recommendation"]
        ]

    @staticmethod
    def _remove_nones_from_kb_result(a_priori_recommended: List) -> None:
        """Changes list"""
        i = 0
        len_bound = len(a_priori_recommended)
        while i < len_bound:
            if a_priori_recommended[i]["recommendation"] is None:
                a_priori_recommended.pop(i)
                len_bound -= 1
                continue
            else:
                j = 0
                additional_recommendations_len_bound = len(a_priori_recommended[i]["additional_recommendations"])
                while j <= additional_recommendations_len_bound:
                    if a_priori_recommended[i]["additional_recommendations"][0]["recommendation"] is None:
                        a_priori_recommended[i]["additional_recommendations"].pop(j)
                        additional_recommendations_len_bound -= 1
                        continue
                    j += 1
            i += 1

    @staticmethod
    def _are_the_same(left_landmark: Dict, right_landmark: Dict) -> bool:
        if left_landmark["name"] != right_landmark["name"]:
            return False
        if left_landmark["latitude"] != right_landmark["latitude"]:
            return False
        if left_landmark["longitude"] != right_landmark["longitude"]:
            return False
        return True

    @staticmethod
    def _remove_duplicates_from_additional_recommendations(
            a_priori_recommended: List, this_index: int, other_index: int
    ):
        i = 0
        this_additional_recommendations_len = len(a_priori_recommended[this_index]["additional_recommendations"])
        while i < this_additional_recommendations_len:
            j = 0
            other_additional_recommendations_len = len(
                a_priori_recommended[other_index]["additional_recommendations"]
            )
            while j < other_additional_recommendations_len:
                if RecommendationsAgent._are_the_same(
                        a_priori_recommended[this_index]["additional_recommendations"][i]["recommendation"],
                        a_priori_recommended[other_index]["additional_recommendations"][j]["recommendation"]
                ):
                    if (
                            a_priori_recommended[this_index]["additional_recommendations"][i]["distance"] <=
                            a_priori_recommended[other_index]["additional_recommendations"][j]["distance"]
                    ):
                        a_priori_recommended[other_index]["additional_recommendations"].pop(j)
                        other_additional_recommendations_len -= 1
                        continue
                    else:
                        a_priori_recommended[this_index]["additional_recommendations"].pop(i)
                        this_additional_recommendations_len -= 1
                        i -= 1
                        break
                j += 1
            i += 1

    @staticmethod
    def _remove_duplicates_from_kb_result(a_priori_recommended: List):
        """Changes list"""
        i = 0
        len_bound = len(a_priori_recommended)
        while i < len_bound:
            j = 0
            while j < len_bound:
                if i == j:
                    j += 1
                    continue
                if RecommendationsAgent._are_the_same(
                        a_priori_recommended[i]["recommendation"], a_priori_recommended[j]["recommendation"]
                ):
                    len_bound -= 1
                    if a_priori_recommended[i]["distance"] <= a_priori_recommended[j]["distance"]:
                        a_priori_recommended.pop(j)
                        continue
                    else:
                        a_priori_recommended.pop(i)
                        i -= 1  # To make increase == 0 (i + 1 - 1 == i)
                        break
                else:
                    RecommendationsAgent._remove_duplicates_from_additional_recommendations(a_priori_recommended, i, j)
                    j += 1
            i += 1

    @staticmethod
    def _categories_overlay(
            user_categories_preference: Dict[str, int], categories_list: List[str], preference_unifier: float
    ) -> float:
        result_criteria = 0
        i = 0
        while i < len(categories_list):
            result_criteria += user_categories_preference.get(categories_list[i], 0) / preference_unifier
            i += 1
        return result_criteria

    @staticmethod
    def _additive_super_criteria(
            user_categories_preference: Dict[str, int],
            main_categories_names: List[str],
            subcategories_names: List[str],
            distance: float,
            wish_to_visit: bool,
            visited_amount: int,
            coefficients: Dict[str, float],
            params_unifiers: Dict[str, float]
    ) -> float:
        return (
                RecommendationsAgent._categories_overlay(
                    user_categories_preference, main_categories_names, params_unifiers["user_categories_preference"]
                )
                * coefficients["main_categories_names"] / params_unifiers["user_categories_preference"] +
                RecommendationsAgent._categories_overlay(
                    user_categories_preference, subcategories_names, params_unifiers["user_categories_preference"]
                )
                * coefficients["subcategories_names"] / params_unifiers["user_categories_preference"] +
                distance
                * coefficients["distance"] / params_unifiers["distance"] +
                int(wish_to_visit)
                * coefficients["wish_to_visit"] / params_unifiers["wish_to_visit"] +
                visited_amount
                * coefficients["visited_amount"] / params_unifiers["visited_amount"]
        )

    def _find_indexes_of_recommendations(
            self,
            a_priori_recommended: List[Dict],
            params_unifiers: Dict[str, float],
            user_categories_preference: Dict[str, int],
            maximum_amount_of_recommendations: int,
    ) -> List[int]:
        a_posteriori_recommended_criteria = []
        a_posteriori_recommended_indexes = []
        for i in range(len(a_priori_recommended)):
            criteria = self._additive_super_criteria(
                user_categories_preference,
                a_priori_recommended[i]["main_categories_names"],
                a_priori_recommended[i]["subcategories_names"],
                a_priori_recommended[i]["distance"],
                a_priori_recommended[i]["wish_to_visit"],
                a_priori_recommended[i]["visited_amount"],
                self.__coefficients,
                params_unifiers
            )
            if len(a_posteriori_recommended_criteria) < maximum_amount_of_recommendations:
                a_posteriori_recommended_indexes.append(i)
                a_posteriori_recommended_criteria.append(criteria)
            else:
                min_value = min(a_posteriori_recommended_criteria)
                if criteria > min_value:
                    position_to_replace = a_posteriori_recommended_criteria.index(min_value)
                    a_posteriori_recommended_criteria[position_to_replace] = criteria
                    a_posteriori_recommended_indexes[position_to_replace] = i
        return a_posteriori_recommended_indexes

    def _find_indexes_of_additional_recommendations(
            self,
            a_priori_recommended: List[Dict],
            params_unifiers: Dict[str, float],
            user_categories_preference: Dict[str, int],
            maximum_amount_of_additional_recommendations: int,
    ) -> List[Tuple[int, int]]:
        a_posteriori_recommended_criteria = []
        a_posteriori_recommended_indexes = []
        for i in range(len(a_priori_recommended)):
            for j in range(len(a_priori_recommended[i]["additional_recommendations"])):
                criteria = self._additive_super_criteria(
                    user_categories_preference,
                    a_priori_recommended[i]["additional_recommendations"][j]["main_categories_names"],
                    a_priori_recommended[i]["additional_recommendations"][j]["subcategories_names"],
                    a_priori_recommended[i]["additional_recommendations"][j]["distance"],
                    a_priori_recommended[i]["additional_recommendations"][j]["wish_to_visit"],
                    a_priori_recommended[i]["additional_recommendations"][j]["visited_amount"],
                    self.__coefficients,
                    params_unifiers
                )
                if len(a_posteriori_recommended_criteria) < maximum_amount_of_additional_recommendations:
                    a_posteriori_recommended_indexes.append((i, j))
                    a_posteriori_recommended_criteria.append(criteria)
                else:
                    min_value = min(a_posteriori_recommended_criteria)
                    if criteria > min_value:
                        position_to_replace = a_posteriori_recommended_criteria.index(min_value)
                        a_posteriori_recommended_criteria[position_to_replace] = criteria
                        a_posteriori_recommended_indexes[position_to_replace] = (i, j)
        return a_posteriori_recommended_indexes

    @staticmethod
    def _json_params_validation(json_params):
        """This method checks values only of special params. Other values will be checked in target agent."""
        validate(json_params, json_validation.find_recommendations_for_coordinates_and_categories)
        if json_params["maximum_amount_of_recommendations"] and json_params["maximum_amount_of_recommendations"] <= 0:
            raise ValidationError("maximum_amount_of_recommendations can\'t be less or equal to zero")
        if json_params["maximum_amount_of_additional_recommendations"] and \
                json_params["maximum_amount_of_additional_recommendations"] <= 0:
            raise ValidationError("maximum_amount_of_additional_recommendations can\'t be less or equal to zero")
        if json_params["amount_of_recommendations_for_point"] and \
                json_params["amount_of_recommendations_for_point"] <= 0:
            raise ValidationError("amount_of_recommendations_for_point can\'t be less or equal to zero")
        if json_params["amount_of_additional_recommendations_for_point"] and \
                json_params["amount_of_additional_recommendations_for_point"] <= 0:
            raise ValidationError("amount_of_additional_recommendations_for_point can\'t be less or equal to zero")
        if json_params["optional_limit"] and json_params["optional_limit"] <= 0:
            raise ValidationError("optional_limit can\'t be less or equal to zero")

    @staticmethod
    async def _a_priori_recommended_by_coordinates_and_categories(json_params: Dict):
        recommendations_async_task = asyncio.create_task(
            AbstractAgentsBroker.call_agent_task(crud_recommendations_by_coordinates_and_categories_task, json_params)
        )
        a_priori_recommended_asyncio_result = await recommendations_async_task
        logger.debug(
            f"Recommendations agent, find_recommendations_for_coordinates_and_categories, "
            f"a_priori_recommended_asyncio_result: {a_priori_recommended_asyncio_result}"
        )
        a_priori_recommended = a_priori_recommended_asyncio_result.return_value
        return a_priori_recommended

    @staticmethod
    def _wrap_recommendations_result(
            recommendations: List[Dict], recommended_indexes: List[int], additional_indexes: List[Tuple[int, int]]
    ):
        result = [
            {"recommendation": None} for _ in range(len(recommendations) + len(additional_indexes))
        ]
        i = 0
        for index in recommended_indexes:
            result[i]["recommendation"] = recommendations[index]["recommendation"]
            i += 1
        for index in additional_indexes:
            result[i]["recommendation"] = recommendations[index[0]]["additional_recommendations"][index[1]]
        return result

    async def _find_recommendations_for_coordinates_and_categories(
            self,
            recommendations,
            maximum_amount_of_recommendations,
            maximum_amount_of_additional_recommendations
    ):
        user_categories_preference = {"озёра поставского района": 1}  # TODO cash request
        # TODO Cash request
        # TODO check cash on None values
        unifiers = self._find_params_unifiers(user_categories_preference, recommendations)

        recommended_indexes = self._find_indexes_of_recommendations(
            recommendations, unifiers, user_categories_preference, maximum_amount_of_recommendations
        )
        additional_indexes = self._find_indexes_of_additional_recommendations(
            recommendations, unifiers, user_categories_preference, maximum_amount_of_additional_recommendations
        )
        i = 0
        additional_bound = len(additional_indexes)
        while i < additional_bound:
            j = 0
            for recommended_index in recommended_indexes:
                if self._are_the_same(
                    recommendations[recommended_index],
                    recommendations[additional_indexes[i][0]]["additional_recommendations"][additional_indexes[i][1]]
                ):
                    recommendations[additional_indexes[i][0]]["additional_recommendations"].pop(
                        [additional_indexes[i][1]]
                    )
                    additional_indexes.pop(i)
                    i -= 1
                    break
                j += 1
            i += 1
        return self._wrap_recommendations_result(recommendations, recommended_indexes, additional_indexes)

    async def find_recommendations_for_coordinates_and_categories(self, json_params: Dict):
        try:
            self._json_params_validation(json_params)
            maximum_amount_of_recommendations = json_params["maximum_amount_of_recommendations"]
            maximum_amount_of_additional_recommendations = json_params["maximum_amount_of_additional_recommendations"]
            json_params.pop("maximum_amount_of_recommendations")
            json_params.pop("maximum_amount_of_additional_recommendations")
        except ValidationError as ex:
            await logger.error(f"find_recommendations_for_coordinates_and_categories, ValidationError({ex.args[0]})")
            return []  # raise ValidationError

        a_priori_recommended = await self._a_priori_recommended_by_coordinates_and_categories(json_params)
        #a_priori_recommended = self._outdated_remove_nones_from_kb_result(a_priori_recommended)
        self._remove_nones_from_kb_result(a_priori_recommended)
        logger.debug(
            f"Recommendations agent, find_recommendations_for_coordinates_and_categories, "
            f"a_priori_recommended after None removed: {a_priori_recommended}"
        )
        if not a_priori_recommended:
            return a_priori_recommended
        self._remove_duplicates_from_kb_result(a_priori_recommended)
        logger.debug(
            f"Recommendations agent, find_recommendations_for_coordinates_and_categories, "
            f"a_priori_recommended after duplicates removed: {a_priori_recommended}"
        )
        return self._find_recommendations_for_coordinates_and_categories(
            a_priori_recommended, maximum_amount_of_recommendations, maximum_amount_of_additional_recommendations
        )
