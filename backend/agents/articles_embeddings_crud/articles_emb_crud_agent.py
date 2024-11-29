from typing import Dict, List
import elasticsearch_settings
from elasticsearch import AsyncElasticsearch, NotFoundError, ConflictError
from elasticsearch.helpers import async_bulk
from pure_articles_crud_agent import ArticlesCrudAgent
import logging

logger = logging.getLogger("async_logger_aec")
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)

logger.addHandler(handler)


class ArticlesEmbCrudAgent(ArticlesCrudAgent):
    """
        Class to work with article's snippets database.
        Provides read, write, update and delete queries for article's snippets.
        All methods work asynchronously.

        Get settings from elasticsearch_settings:
            elasticsearch_settings.HOST - elasticsearch endpoint, use to create AsyncElasticsearch client
            elasticsearch_settings.ARTICLES_EMB_IND - current index, where all the work happens
    """

    _instance = None 

    def __new__(cls, *args, **kwargs):
        """
        Realization Singleton.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls) 
        return cls._instance

    def __init__(self):
        """
        Initialization ArticlesEmbCrudAgent.
        """
        if not hasattr(self, "__initialized"): 
            self.__client = AsyncElasticsearch(hosts=elasticsearch_settings.HOST)
            self.__initialized = True 

    def _process_result(self, json_params: Dict):
        """
        Validate elasticsearch response.

        :param json_params:
            Dict structure is different to every response, but has important identical keys.
        :return:
            Dict[
                "id" : string,
                "article_name": string,
                "article_vector": List[float]
            ]

        """
        return {
            "id": json_params["_id"],
            "article_name": json_params["_source"]["article_name"],
            "article_vector": json_params["_source"]["article_vector"]
        }

    async def get_all_documents(self):
        """
        Get all existing documents.

        :return:
            List[
                Dict[
                "id" : string,
                "article_name": string,
                "article_vector": List[float]
                ]
            ], if error or 0 documents return List[]

        """
        try:
            resp = await self.__client.search(index=elasticsearch_settings.ARTICLES_EMB_IND, body={
                "query": {
                    "match_all": {}
                },
                "size": 1000
            }
                                              )
        except Exception as e:
            logger.error(str(e))
            return []

        else:
            if resp["hits"]["hits"]:
                return [
                    self._process_result(doc)
                    for doc in resp.body["hits"]["hits"]
                ]
            else:
                return []

    async def get_single_document(self, doc_id: str):
        """
        Get document by id.

        :param doc_id: string
        :return: Dict[
                "id" : string,
                "article_name": string,,
                "article_vector": List[float]
                ], if error return {}
        """
        try:
            resp = await self.__client.get(index=elasticsearch_settings.ARTICLES_EMB_IND, id=doc_id)

        except NotFoundError:
            logger.warning(f"Document with id {doc_id} not found")
            return {}

        except Exception as e:
            logger.error(str(e))
            return {}

        else:
            return self._process_result(resp.body)

    async def search_nearest_articles(self, query_vector: List[float]):
        """
        Search for nearest articles by embedding, return best 10 articles.
        Using score is (1.0 - cosineSimilarity(params.query_vector, 'article_vector')).

        :param query_vector: List[float]
        :return: List[
                Dict[
                "id" : string,
                "article_name": string,
                "article_vector": List[float]
                ]
            ], if error or 0 documents return List[]
        """
        try:
            resp = await self.__client.search(index=elasticsearch_settings.ARTICLES_EMB_IND, body={
                "query": {
                    "script_score": {
                        "query": {
                            "match_all": {}
                        },
                        "script": {
                            "source": """
                              (1.0 - cosineSimilarity(params.query_vector, 'article_vector'))
                            """,
                            "params": {
                                "query_vector": query_vector
                            }
                        }
                    }
                }
            })

        except Exception as e:
            logger.error(str(e))
            return []

        else:
            if resp.body["hits"]["hits"]:
                return [
                        self._process_result(doc)
                        for doc in resp.body["hits"]["hits"]
                    ]
            else:
                return []

    async def create_document(self, json_params: Dict):
        """
        Create document.

        :param json_params: Dict[
                "id" : string,
                "article_name": string,
                "article_vector": List[float],
            ]
        :return: Dict[
                "result": string
            ], result = "created" if okay
        """
        try:
            resp = await self.__client.create(index=elasticsearch_settings.ARTICLES_EMB_IND, body=json_params,
                                              id=json_params["id"])

        except ConflictError:
            logger.error(f"Document with {json_params['id']} already exist.")
            return {"result": "error"}
        except Exception as e:
            logger.error(str(e))
            return {"result": "error"}
        else:
            return {"result": resp.body["result"]}

    async def update_document(self, json_params: Dict):
        """
        Updated document.

        :param json_params: Dict[
                "id" : string,
                "article_name": string,
                "article_vector": List[float],
            ]
        :return: Dict[
                    "result": string
                ], result = "updated" if okay
        """
        try:
            resp = await self.__client.update(index=elasticsearch_settings.ARTICLES_EMB_IND,
                                              id=json_params['id'],
                                              body={
                                                  "doc": {
                                                      "article_name": json_params["article_name"],
                                                      "article_vector": json_params["article_vector"]
                                                  }
                                              })

        except NotFoundError:
            logger.warning(f"Document with id {json_params['id']} not found")
            return {"result": "error"}

        except Exception as e:
            logger.error(str(e))
            return {"result": "error"}

        else:
            return {"result": resp.body["result"]}

    async def delete_document(self, doc_id: str):
        """
        Delete document by id.

        :param doc_id: string
        :return: Dict[
                    "result": string
                ], result = "deleted" if okay
        """
        try:
            resp = await self.__client.delete(index=elasticsearch_settings.ARTICLES_EMB_IND, id=doc_id)

        except Exception as e:
            logger.error(str(e))
            return {"result": "error"}

        else:
            return {"result": resp.body["result"]}

    async def create_multiply_documents(self, document_list: List[Dict]):
        """
        Create multiply documents from list.

        :param document_list:  List[
                Dict[
                    "id" : string,
                    "article_name": string,
                    "article_vector": List[float],
                ]
            ]
        :return:
            Dict[
                    "result": string
                ], result = "created" if okay
        """
        actions = [
            {
                "_op_type": "create",
                "_index": elasticsearch_settings.ARTICLES_EMB_IND,
                "_id": doc["id"],
                "_source": {k: v for k, v in doc.items() if k != "id"}
            }
            for doc in document_list
        ]
        try:
            (success, details) = await async_bulk(self.__client, actions)

        except Exception as e:
            logger.error(str(e))
            return {"result": "error"}

        if not success:
            return {"result": "error"}

        else:
            return {"result": "created"}

    async def close_agent(self):
        """
        Close connection after use agent.
        Always close before end of the session.
        """
        await self.__client.close()
