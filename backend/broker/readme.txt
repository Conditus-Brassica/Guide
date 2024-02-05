Если функционал агента готов, добавляем экземпляр агента в конструктор класса AgentsBroker (лучше всего передавать
интерфейс или абстрактный класс). Создаем экземпляр агента в broker_initializer.py РЯДОМ с CRUD агентом (в else части)

При создании функции агента, которая может быть вызвана другим агентом, для нее создается task. Все task-и, относящиеся
к одному и тому же агенту размещаются в своем файле

Путь к task-ам: backend/broker/agents_tasks/example_agent_tasks.py

task - асинхронная функция с декоратором @BROKER.task, где BROKER - глобальная переменная импортируемая с модулем broker
(она находится в файле broker_initializer, но не обязательно испортировать ее напрямую оттуда).


@BROKER.task
async def example_task(json_params: Dict):
"""
Docstring

:param json_params: Dict in form {
    "param": param_type
}, params for target function of agent
:return: Coroutine ...
"""
    return await BROKER.example_agent.target_method(json_params)


В task-е вызывается метод конкретного агента, а не абстрактного. При вызове передаются параметры метода агента. Сам
task другими агентами не вызывается. Вызов осуществляется через асинхронный метод

    AbstractAgentsBroker.get_broker().call_agent_task(target_task, json_params: Dict)

Импортируйте в своего агента именно АБСТРАКТНЫЙ класс брокера. Иначе возможно возникновение круговой зависимости.

Метод вызывается через await, либо, что вероятнее всего (зависит от контекста), оборачивается asyncio.create_task.

Для вызова task-а необходимо передать его в качестве параметра в метод AgentBroker.call_agent_tasks(agent_task, json_params)

Для запуска Broker-а необходимо в терминале из директории course запустить скрипт

    taskiq worker backend.broker.broker_initializer:BROKER \
        backend.broker.agents_tasks.crud_agent_tasks \
        backend.broker.agents_tasks.recommendations_agent_tasks \
        backend.broker.agents_tasks.landmarks_by_sectors_agent_tasks \
        backend.broker.agents_tasks.route_builder_task \
        backend.broker.agents_tasks.route_generating_tasks \
        --no-configure-logging


В конкретных агентах не используйте BROKER из broker_initializer,
этот объект доступен через метод класса AgentsBroker.get_broker(). Это тот же самый экземпляр класса (класс синглетон).

Пример создания task-ов в файле backend/broker/agents_tasks/crud_agent_tasks.py
Пример вызова этих же task-ов в файле backend/agents/crud_agent/crud_test.py
