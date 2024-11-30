# Author: Vodohleb04
from abc import ABC, abstractmethod
from typing import Dict, List


class PureEmbeddingsModel(ABC):
    """
    Pure abstract class of Embeddings model. Provides methods for commands from the other agents.

    All methods work asynchronously.
    """

    @abstractmethod
    async def make_snippet_embedding(self, json_params: Dict):
        """
        Method to make snippet embedding for the given text. Don't pass the big text in it. Works asynchronously.

        :param json_params: Dict[
            "text": str,
            Optional["window_size": int],
            Optional["intersection_with_prev_window": int]
        ]

        :return: Coroutine
            List[
                Dict[
                    "embedding": List[float],
                    "snippet_text": str
                ]
            ]
        """
        raise NotImplementedError


    @abstractmethod
    async def make_recommendation_embedding(self, json_params: Dict):
        """
        Method to make embedding, used in rec system, for the given text. Full text will be processed with usage of sliding window.
        Works asynchronously.

        :param json_params: Dict[
            "text": str,
            Optional["window_size": int,]
            Optional["intersection_with_prev_window": int]
        ]

        :returns: Coroutine
            Dict[
                "embedding": List[float]
            ]
        """
        raise NotImplementedError


    @abstractmethod
    async def make_user_query_embedding(self, json_params: Dict):
        """
        Method to make embedding for user query. Full text will be processed with usage of sliding window.
        Works asynchronously.

        :param json_params: Dict[
            "text": str,
            Optional["window_size": int,]
            Optional["intersection_with_prev_window": int]
        ]

        :returns: Coroutine
            Dict[
                "embedding": List[float]
            ]
        """
        raise NotImplementedError
