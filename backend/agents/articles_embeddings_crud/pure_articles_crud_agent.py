from abc import ABC, abstractmethod
from typing import Dict, List


class ArticlesCrudAgent(ABC):
    """
        Base class for CRUD agent, that provided to manage documents.

     """
    @abstractmethod
    async def get_all_documents(self):
        """
        Read query to get all existing documents.
        Works asynchronously.

        :return:
            Dict[]

            Dict structure is different to ArticlesSnippetsEmbCrudAgent and ArticlesEmbCrudAgent.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_single_document(self, doc_id: str):
        """
        Read query to get document by id.
        Works asynchronously.

        :param doc_id: string

        :return:
            Dict[]

            Dict structure is different to ArticlesSnippetsEmbCrudAgent and ArticlesEmbCrudAgent.
        """
        raise NotImplementedError

    @abstractmethod
    async def create_document(self, json_params: Dict):
        """
        Create document query.
        Works asynchronously.

        :param json_params: Dict[]

            Dict structure is different to ArticlesSnippetsEmbCrudAgent and ArticlesEmbCrudAgent.
        :return:
            Dict[
                "result": "created"
            ], if successful.
        """
        raise NotImplementedError

    @abstractmethod
    async def update_document(self,  json_params: Dict):
        """
        Update document query.
        Works asynchronously.

        :param json_params: json_params: Dict[]

            Dict structure is different to ArticlesSnippetsEmbCrudAgent and ArticlesEmbCrudAgent.
        :return:
            Dict[
                    "result": "updated"
                ], if successful.
        """
        raise NotImplementedError

    @abstractmethod
    async def delete_document(self, doc_id: str):
        """
        Delete document by id query.
        Works asynchronously.

        :param doc_id: string
        :return:
            Dict[
                    "result": "deleted"
                ], if successful.
        """
        raise NotImplementedError

    @abstractmethod
    async def close_agent(self):
        """
        Close connection after use agent.
        Always close before end of the session.
        """
        raise NotImplementedError

    @abstractmethod
    async def search_nearest_articles(self, query_vector: List[float]):
        """
        Search for nearest articles by embedding.
        Using score is (1.0 - (cosineSimilarity(query_vector, 'snippet_vector') + 1.0) / 2.0).

        :param query_vector: List[float]
        :return: List[
                    Dict[]
                    ], if error or 0 documents return List[].
            Dict structure is different to ArticlesSnippetsEmbCrudAgent and ArticlesEmbCrudAgent.
        """

        raise NotImplementedError

    @abstractmethod
    async def create_multiply_documents(self, document_list: List[Dict]):
        """
        Create multiply documents from list.

        :param document_list: List[
                    Dict[]
                    ]
            Dict structure is different to ArticlesSnippetsEmbCrudAgent and ArticlesEmbCrudAgent.
        :return:
            Dict[
                    "result": "created"
                ], if successful.
        """
        return NotImplementedError

    @abstractmethod
    def _process_result(self, json_params: Dict):
        """
        Validate elasticsearch response.

        :param json_params: Dict[]

            Dict structure is different to ArticlesSnippetsEmbCrudAgent and ArticlesEmbCrudAgent.
        :return: Dict[]

            Dict structure is different to ArticlesSnippetsEmbCrudAgent and ArticlesEmbCrudAgent.
        """
        raise NotImplementedError
