#Author: Vodohleb04
"""Pure agents broker"""
from abc import ABC, abstractmethod
from typing import Dict

import taskiq
from taskiq_redis import ListQueueBroker


class AbstractAgentsBroker(ListQueueBroker, ABC):
    """
    Pure custom broker class to work with agents.
    Child classes are singletons.
    This class is used to solve cycle dependencies.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    @abstractmethod
    def get_broker(cls):
        """
        Method to take broker object. Returns None in case when broker is not exists.
        :return: None | AgentsBroker
        """
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def broker_exists(cls) -> bool:
        """Method to check if broker object already exists"""
        raise NotImplementedError

    @staticmethod
    async def call_agent_task(agent_task, json_params: Dict):
        """
        Wrapper to call task using broker. Call tasks only using this function.
        Works asynchronously.

        :param agent_task: task to call (check broker/agents_tasks/... for available tasks). Takes only function name
        without arguments
        :param json_params: Dict with arguments to run the agent\'s function.
        :return: agent_task.wait_result(). Use return_value property to get result of agent_task
        """
        agent_task = await agent_task.kiq(json_params)

        return await agent_task.wait_result()

