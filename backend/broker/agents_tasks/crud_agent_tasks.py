# Author: Vodohleb04
"""Tasks to work with crud agent. Use broker to run tasks"""
from typing import Dict
from backend.broker.broker_initializer import BROKER
from backend.agents.crud_agent.crud_initializer import CRUD_AGENT



# Read tasks

@BROKER.task
async def categories_of_region_task(json_params: Dict):
    """
    Task to get the categories of the region. Do NOT call this task directly. Give it as the first argument (agent_task)
    of AgentsBroker.call_agent_task instead.
    Works asynchronously.

    Params for target function of agent Dict in form {
            "region_name": str,
            "optional_limit": int | None
        }, params for target function of agent
    :return: Coroutine
        List[
            {
                "category": {"name": str} | None,
                "located_at": {"name": str} | None
            }
        ]
    """
    return await CRUD_AGENT.get_categories_of_region(json_params)


@BROKER.task
async def landmarks_in_map_sectors_task(json_params: Dict):
    """
    Task to get landmarks, located in passed map sectors. Finds map sectors by their names.
    Do NOT call this task directly. Give it as the first argument (agent_task) of AgentsBroker.call_agent_task instead.
    Works asynchronously.

    Params for target function of agent Dict in form {
            "map_sectors_names": List[str],
            "optional_limit": int | None
        }, params for target function of agent
    :return: Coroutine
        List [
            {
                "landmark": Dict | None,
                "sector": Dict | None,
                "categories_names": List[str] | [] (empty list)
            }
        ], where categories_names are categories of landmark
    """
    return await CRUD_AGENT.get_landmarks_in_map_sectors(json_params)


@BROKER.task
async def landmarks_refers_to_categories_task(json_params: Dict):
    """
    Task to get landmarks, that refers to given categories. Finds categories by their names.
    Do NOT call this task directly. Give it as the first argument (agent_task) of AgentsBroker.call_agent_task instead.
    Works asynchronously.

    Params for target function of agent Dict in form {
            "categories_names": List[str],
            "optional_limit": int | None
        }
    :return: Coroutine
        List [
            {
                "landmark": Dict | None,
                "category": Dict | None
            }
        ]
    """
    return await CRUD_AGENT.get_landmarks_refers_to_categories(json_params)


@BROKER.task
async def landmarks_by_coordinates_and_name_task(json_params: Dict):
    """
    Task to get landmarks with the given coordinates and name.
    Do NOT call this task directly. Give it as the first argument (agent_task) of AgentsBroker.call_agent_task instead.
    Works asynchronously.

    Params for target function of agent Dict in form {
            "coordinates_name_list": List [
                Dict [
                    "latitude": float,
                    "longitude": float,
                    "name": str
                ]
            ],
            "optional_limit": int | None
        }
    :return: Coroutine
        List [
            Dict[
                "landmark": Dict | None,
                "categories_names": List[str] | [] (empty list),
                "in_regions": List["str"] | []
            ]
        ],  where categories_names are categories of landmark, in_regions - names of regions, where landmark is located
    """
    return await CRUD_AGENT.get_landmarks_by_coordinates_and_name(json_params)


@BROKER.task
async def landmarks_by_name_list_task(json_params: Dict):
    """
    Task to get landmarks with given names.
    Do NOT call this task directly. Give it as the first argument (agent_task) of AgentsBroker.call_agent_task instead.
    Works asynchronously.

    Params for target function of agent Dict in form {
            "landmark_names": List[str]
        }
    :return: Coroutine
        List [
            Dict[
                "landmark": Dict | None,
                "categories_names": List[str] | [] (empty list),
                "in_regions": List["str"] | []
            ]
        ],  where categories_names are categories of landmark, in_regions - names of regions, where landmark is located
    """
    return await CRUD_AGENT.get_landmarks_by_name_list(json_params)


@BROKER.task
async def landmarks_by_name_task(json_params: Dict):
    """
    Task to get landmarks with the names that starts with the given name.
    Do NOT call this task directly. Give it as the first argument (agent_task) of AgentsBroker.call_agent_task instead.
    Works asynchronously.

    Params for target function of agent Dict in form {
            "landmark_name": str,
            "limit": int
        }
    :return: Coroutine
        List [
            Dict[
                "landmark": Dict | None,
                "categories_names": List[str] | [] (empty list),
                "in_regions": List["str"] | []
            ]
        ],  where categories_names are categories of landmark, in_regions - names of regions, where landmark is located
    """
    return await CRUD_AGENT.get_landmarks_by_name(json_params)


@BROKER.task
async def landmarks_of_categories_in_region_task(json_params: Dict):
    """
    Task to get landmarks, located in given region, that refer to given categories.
    Finds region by its name. Finds categories by their names.
    Do NOT call this task directly. Give it as the first argument (agent_task) of AgentsBroker.call_agent_task instead.
    Works asynchronously.

    Params for target function of agent Dict in form {
            "region_name": str,
            "categories_names": List[str],
            "optional_limit": int | None
        }
    :return: Coroutine
        List [
            Dict[
                "landmark": Dict | None,
                "located_at": Dict | None,
                "category": Dict | None
            ]
        ], where "located_at" is the region, where landmark is located
    """
    return await CRUD_AGENT.get_landmarks_of_categories_in_region(json_params)


@BROKER.task
async def landmarks_by_region_task(json_params: Dict):
    """
    Task to get landmarks, located in region. Finds region by its name.
    Do NOT call this task directly. Give it as the first argument (agent_task) of AgentsBroker.call_agent_task instead.
    Works asynchronously.

    Params for target function of agent Dict in form {
            "region_name": str,
            "optional_limit": int | None
        }
    :return: Coroutine
        List[
            Dict[
                "landmark": Dict | None,
                "located_at": Dict | None,
                "categories_names": List[str] | [] (empty list)
            ]
        ],  where "located_at" is the region, where landmark is located, categories_names are categories of landmark
    """
    return await CRUD_AGENT.get_landmarks_by_region(json_params)


@BROKER.task
async def map_sectors_of_points_task(json_params: Dict):
    """
    Task to get map sectors where given points are located.
    Do NOT call this task directly. Give it as the first argument (agent_task) of AgentsBroker.call_agent_task instead.
    Works asynchronously.

    Params for target function of agent Dict in form {
        "coordinates_of_points": List[
            Dict [
                "longitude": float,
                "latitude": float
            ]
        ],
        "optional_limit": int | None
    }
    :return: Coroutine
        List[
            Dict[
                "of_point": Dict ["longitude": float, "latitude": float]
                "map_sector": Dict | None,
            ]
        ]
    """
    return await CRUD_AGENT.get_map_sectors_of_points(json_params)


@BROKER.task
async def map_sectors_structure_of_region_task(json_params: Dict):
    """
    Task to get map sectors structure of the given region.
    Do NOT call this task directly. Give it as the first argument (agent_task) of AgentsBroker.call_agent_task instead.
    Works asynchronously.

    Params for target function of agent Dict in form {
        "region_name": str
    }
    :return: Coroutine
        List[
            Dict[
                "map_sector_name": str | None,
                "tl_latitude": float | None,
                "tl_longitude": float | None,
                "br_latitude": float | None,
                "br_longitude: float | None"
                "neighbour_map_sector_names": List[str] | (empty list)
            ]
        ]
    """
    return await CRUD_AGENT.get_map_sectors_structure_of_region(json_params)


@BROKER.task
async def landmarks_of_categories_in_map_sectors_task(json_params: Dict):
    """
    Task to get landmarks that refer to the given categories and are located in the given map sectors.
    Finds map sectors by names. Finds categories by names.

    Do NOT call this task directly. Give it as the first argument (agent_task) of AgentsBroker.call_agent_task instead.

    Works asynchronously.


    Params for target function of agent Dict in form {
        "map_sectors_names": List[str],
        "categories_names": List[str],
        "optional_limit": int | None
    }
    :return: Coroutine
        List[
            Dict[
                "landmark": Dict | None,
                "map_sector": Dict | None,
                "category": Dict | None
            ]
        ]
    """
    return await CRUD_AGENT.get_landmarks_of_categories_in_map_sectors(json_params)


@BROKER.task
async def route_landmarks_by_index_id_task(json_params: Dict):
    """
    Task to get list landmarks of the route with the given index_id (unique id of route). Landmarks are returned in the
        order that corresponds to the order of appearance of landmarks in the route.

    Do NOT call this task directly. Give it as the first argument (agent_task) of AgentsBroker.call_agent_task instead.
    Works asynchronously.

    :param json_params: Params for target function of agent Dict in form {
        "index_id": int
    }
    :return: Coroutine
        List[
            Dict[
                "landmark": Dict | None,
            ]
        ]
    """
    return await CRUD_AGENT.get_route_landmarks_by_index_id(json_params)


@BROKER.task
async def routes_saved_by_user_task(json_params: Dict):
    """
    Task to get routes with its landmarks (returns landmarks in the order that corresponds to the order of appearance
        of landmarks in the route).

    Do NOT call this task directly. Give it as the first argument (agent_task) of AgentsBroker.call_agent_task instead.
    Works asynchronously.

    :param json_params: Dict in form {
        "user_login": str
    }
    :return: Coroutine
        List[
            Dict[
                "route": Dict | None,
                "route_landmarks": List[Dict | None] | None
            ]
        ]
    """
    return await CRUD_AGENT.get_routes_saved_by_user(json_params)


@BROKER.task
async def range_of_routes_saved_by_user_task(json_params: Dict):
    """
    Task to get range of routes with its landmarks (returns landmarks in the order that corresponds to the order of
        appearance of landmarks in the route). Range looks like (skip, skip + limit]. skip=0 return result from the very
        beginning.

    Do NOT call this task directly. Give it as the first argument (agent_task) of AgentsBroker.call_agent_task instead.
    Works asynchronously.

    :param json_params: Dict in form {
        "user_login": str,
        "skip": int,
        "limit": limit
    }
    :return: Coroutine
        List[
            Dict[
                "route": Dict | None,
                "route_landmarks": List[Dict | None] | None
            ]
        ]
    """
    return await CRUD_AGENT.get_range_of_routes_saved_by_user(json_params)


@BROKER.task
async def note_by_title_task(json_params: Dict):
    """
    Task to get note with its routes (returns routes with theirs landmarks in the order that corresponds to the
        order of appearance of landmarks in the route) by title of the note.

    Do NOT call this task directly. Give it as the first argument (agent_task) of AgentsBroker.call_agent_task instead.
    Works asynchronously.

    :param json_params: Dict in form {
        "note_title": str
    }
    :return: Coroutine
        List[
            Dict[
                "note": Dict | None,
                "route": Dict | None,
                "route_landmarks": List[Dict | None] | None,
                "note_category_names": List[str | None] | None
            ]
        ]
    """
    return await CRUD_AGENT.get_note_by_title(json_params)


@BROKER.task
async def notes_in_range_task(json_params: Dict):
    """
    Task to get range of notes of all categories with their routes (with landmarks in the order that corresponds to the
    order of appearance of landmarks in the route). Range looks like (skip, skip + limit].

    Do NOT call this task directly. Give it as the first argument (agent_task) of AgentsBroker.call_agent_task instead.
    Works asynchronously.

    :param json_params: Dict in form {
        "skip": int,
        "limit": limit
    }
    :return: Coroutine
        List[
            Dict[
                "note": Dict | None,
                "route": Dict | None,
                "route_landmarks": List[Dict | None] | None,
                "note_category_names": List[str | None] | None
            ]
        ]
    """
    return await CRUD_AGENT.get_notes_in_range(json_params)


@BROKER.task
async def notes_of_categories_in_range(json_params: Dict):
    """
    Task to get range of notes of the given categories with their routes (with landmarks in the order that corresponds
    to the order of appearance of landmarks in the route). Range looks like (skip, skip + limit].

    Do NOT call this task directly. Give it as the first argument (agent_task) of AgentsBroker.call_agent_task instead.
    Works asynchronously.

    :param json_params: Dict in form {
        "note_categories_names": List[str]
        "skip": int,
        "limit": limit
    }
    :return: Coroutine
        List[
            Dict[
                "note": Dict | None,
                "route": Dict | None,
                "route_landmarks": List[Dict | None] | None,
                "note_category_names": List[str | None] | None
            ]
        ]
    """
    return await CRUD_AGENT.get_notes_of_categories_in_range(json_params)


@BROKER.task
async def crud_recommendations_by_coordinates_task(json_params: Dict):
    """
    Task to get recommended landmarks by given coordinates. Returns recommended landmarks.

    Do NOT call this task directly. Give it as the first argument (agent_task) of AgentsBroker.call_agent_task instead.

    Works asynchronously.

    :param json_params: Params for target function of agent Dict in form {
        "coordinates_of_points": List [
            Dict [
                "latitude": float,
                "longitude": float
            ]
        ],
        "limit": int | None
    }
    :return: Coroutine
    List[
        Dict[
            "recommendation": Dict | None,
        ]
    ]
    """
    return await CRUD_AGENT.get_recommendations_by_coordinates(json_params)


# Write tasks
@BROKER.task
async def post_user_task(json_params: Dict):
    """
    Task to put user to kb. Returns True if everything fine, else returns False.

    Do NOT call this task directly. Give it as the first argument (agent_task) of AgentsBroker.call_agent_task instead.
    Works asynchronously.

    :param json_params: Dict in form {"user_login": str}
    :return: Coroutine Dict["result": bool] -
    """
    return await CRUD_AGENT.put_user(json_params)


@BROKER.task
async def post_note_task(json_params: Dict):
    """
    Task to put note created by guide to kb. Returns True if everything fine, returns False otherwise.

    Do NOT call this task directly. Give it as the first argument (agent_task) of AgentsBroker.call_agent_task instead.
    Works asynchronously.

    :param json_params: Dict in form {
        "guide_login": str,
        "country_names": List[str],
        "note_title": str,
        "note_category_names": List[str]
    }
    :return: Coroutine Dict["result": bool] -
    """
    return await CRUD_AGENT.put_note(json_params)


@BROKER.task
async def post_route_for_note_task(json_params: Dict):
    """
    Task to put route for the corresponding note to kb. Returns True if everything fine, returns False otherwise.

    Do NOT call this task directly. Give it as the first argument (agent_task) of AgentsBroker.call_agent_task instead.
    Works asynchronously.

    :param json_params: Dict in form {
        "note_title": str,
        "landmark_info_position_dicts": List[
            Dict [
                "name": str,
                "position": int,
                "latitude": float,
                "longitude": float
            ]
        ], where name is name of landmark and position is position in route of corresponding landmark (starts from 0)
    }

    :return: Coroutine Dict["result": bool] -
    """
    return await CRUD_AGENT.put_route_for_note(json_params)


@BROKER.task
async def post_route_saved_by_user_task(json_params: Dict):
    """
    Task to put route saved by user to kb. Returns True if everything fine, returns False otherwise.

    Do NOT call this task directly. Give it as the first argument (agent_task) of AgentsBroker.call_agent_task instead.
    Works asynchronously.

    :param json_params: Dict in form {
        "user_login": str,
        "landmark_info_position_dicts": List[
            Dict [
                "name": str,
                "position": int,
                "latitude": float,
                "longitude": float
            ]
        ], where name is name of landmark and position is position in route of corresponding landmark (starts from 0)
    }
    :return: Coroutine Dict["result": bool] -
    """
    return await CRUD_AGENT.put_route_saved_by_user(json_params)


@BROKER.task
async def post_saved_relationship_for_existing_route(json_params: Dict):
    """
    Task to mark route with the given index_id as saved by user. Returns True if everything fine,
        returns False otherwise.

    Do NOT call this task directly. Give it as the first argument (agent_task) of AgentsBroker.call_agent_task instead.
    Works asynchronously.

    :param json_params: Dict in form {
        "user_login": str,
        "index_id": int
    }
    :return: Coroutine Dict["result": bool] -
    """
    return await CRUD_AGENT.put_saved_relationship_for_existing_route(json_params)
