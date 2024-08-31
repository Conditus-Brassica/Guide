# Read validation
"""
get_categories_of_region
"""
get_categories_of_region_json = \
    {
        "type": "object",
        "properties": {
            "region_name": {"type": "string"},
            "optional_limit": {"type": ["number", "null"]}
        },
        "required": ["region_name"],
        "maxProperties": 2,
        "additionalProperties": False
    }

"""
get_landmarks_in_map_sectors
"""
get_landmarks_in_map_sectors_json = \
    {
        "type": "object",
        "properties": {
            "map_sectors_names":
                {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "additionalProperties": False
                },
            "optional_limit": {"type": ["number", "null"]},
            "additionalProperties": False
        },
        "required": ["map_sectors_names"],
        "maxProperties": 2,
        "additionalProperties": False
    }

"""
get_landmarks_refers_to_categories
"""
get_landmarks_refers_to_categories_json = \
    {
        "type": "object",
        "properties": {
            "categories_names":
                {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "additionalProperties": False
                },
            "optional_limit": {"type": ["number", "null"]},
            "additionalProperties": False
        },
        "required": ["categories_names"],
        "maxProperties": 2,
        "additionalProperties": False
    }

"""
get_landmarks_by_coordinates
"""
get_landmarks_by_coordinates_json = \
    {
        "type": "object",
        "properties": {
            "coordinates": {
                "type": "array",
                "items":
                    {
                        "type": "object",
                        "properties": {
                            "latitude": {"type": "number"},
                            "longitude": {"type": "number"}
                        },
                        "required": ["latitude", "longitude"],
                        "maxProperties": 2,
                        "additionalProperties": False
                    },
                "additionalProperties": False
            },
            "optional_limit": {"type": ["number", "null"]}
        },
        "required": ["coordinates"],
        "maxProperties": 2,
        "additionalProperties": False
    }

"""
get_landmarks_by_name_list
"""
get_landmarks_by_name_list_json = \
    {
        "type": "object",
        "properties": {
            "landmark_names":
                {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                    "additionalProperties": False
                },
            "additionalProperties": False
        },
        "required": ["landmark_names"],
        "maxProperties": 1,
        "additionalProperties": False
    }

"""
get_landmarks_by_name
"""
get_landmarks_by_name_json = \
    {
        "type": "object",
        "properties": {
            "landmark_name": {"type": "string"},
            "limit": {"type": "number"},
            "additionalProperties": False
        },
        "required": ["landmark_name", "limit"],
        "maxProperties": 2,
        "additionalProperties": False
    }

"""
get_landmarks_of_categories_in_region
"""
get_landmarks_of_categories_in_region_json = \
    {
        "type": "object",
        "properties": {
            "region_name":
                {
                    "type": "string"
                },
            "categories_names":
                {
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                },
            "optional_limit": {"type": ["number", "null"]}
        },
        "required": ["categories_names", "region_name"],
        "maxProperties": 3,
        "additionalProperties": False
    }

"""
get_landmarks_by_region
"""
# Он такой же как и у get_categories_of_region_json
get_landmarks_by_region_json = \
    {
        "type": "object",
        "properties": {
            "region_name": {"type": "string"},
            "optional_limit": {"type": ["number", "null"]}
        },
        "required": ["region_name"],
        "maxProperties": 2,
        "additionalProperties": False
    }


"""
get_map_sectors_of_points
"""
get_map_sectors_of_points = \
    {
        "type": "object",
        "properties": {
            "coordinates_of_points": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "longitude": {"type": "number"},
                        "latitude": {"type": "number"}
                    },
                    "required": ["longitude", "latitude"],
                    "additionalProperties": False,
                    "maxProperties": 2
                }

            },
            "optional_limit": {"type": ["null", "number"]}
        },
        "required": ["coordinates_of_points"],
        "maxProperties": 2,
        "additionalProperties": False
    }

"""
get_map_sectors_structure_of_region
"""
get_map_sectors_structure_of_region = \
    {
        "type": "object",
        "properties": {
            "region_name": {"type": "string"}
        },
        "required": ["region_name"],
        "maxProperties": 1,
        "additionalProperties": False
    }

"""
get_landmarks_of_categories_in_map_sectors
"""
get_landmarks_of_categories_in_map_sectors = \
    {
        "type": "object",
        "properties": {
            "map_sectors_names": {
                "type": "array",
                "items": {"type": "string"}

            },
            "categories_names": {
                "type": "array",
                "items": {"type": "string"}

            },
            "optional_limit": {"type": ["null", "number"]}
        },
        "required": ["map_sectors_names", "categories_names"],
        "maxProperties": 3,
        "additionalProperties": False
    }

"""
get_route_landmarks_by_index_id
"""
get_route_landmarks_by_index_id = \
    {
        "type": "object",
        "properties": {
            "index_id": {"type": "number"}
        },
        "required": ["index_id"],
        "maxProperties": 1,
        "additionalProperties": False
    }

"""
get_routes_saved_by_user
"""
get_routes_saved_by_user = \
    {
        "type": "object",
        "properties": {
            "user_login": {"type": "string"}
        },
        "required": ["user_login"],
        "maxProperties": 1,
        "additionalProperties": False
    }

"""
get_range_of_routes_saved_by_user
"""
get_range_of_routes_saved_by_user = \
    {
        "type": "object",
        "properties": {
            "user_login": {"type": "string"},
            "skip": {"type": "number"},
            "limit": {"type": "number"}
        },
        "required": ["user_login", "skip", "limit"],
        "maxProperties": 3,
        "additionalProperties": False
    }

"""
get_note_by_title
"""
get_note_by_title = \
    {
        "type": "object",
        "properties": {
            "note_title": {"type": "string"}
        },
        "required": ["note_title"],
        "maxProperties": 1,
        "additionalProperties": False
    }

"""
get_notes_in_range
"""
get_notes_in_range = \
    {
        "type": "object",
        "properties": {
            "skip": {"type": "number"},
            "limit": {"type": "number"}
        },
        "required": ["skip", "limit"],
        "maxProperties": 2,
        "additionalProperties": False
    }

"""
get_notes_of_categories_in_range
"""
get_notes_of_categories_in_range = \
    {
        "type": "object",
        "properties": {
            "note_categories_names": {
                "type": "array",
                "items": {
                    "type": "string"
                }
            },
            "skip": {"type": "number"},
            "limit": {"type": "number"}
        },
        "required": ["note_categories_names", "skip", "limit"],
        "maxProperties": 3,
        "additionalProperties": False
    }

"""
get_recommendations_by_coordinates
"""
get_recommendations_by_coordinates = \
    {
        "type": "object",
        "properties": {
            "coordinates_of_points": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "latitude": {"type": "number"},
                        "longitude": {"type": "number"}
                    },
                    "required": ["latitude", "longitude"],
                    "maxProperties": 2,
                    "additionalProperties": False
                }

            },
            "limit": {"type": "number"}
        },
        "required": [
            "coordinates_of_points",
            "limit"
        ],
        "maxProperties": 2,
        "additionalProperties": False
    }

# Write validation
"""
put_user
"""
put_user = \
    {
        "type": "object",
        "properties": {
            "user_login": {"type": "string"}
        },
        "required": ["user_login"],
        "maxProperties": 1,
        "additionalProperties": False
    }

"""
put_note
"""
put_note = \
    {
        "type": "object",
        "properties": {
            "guide_login": {"type": "string"},
            "country_names": {
                "type": "array",
                "items": {"type": "string"}
            },
            "note_title": {"type": "string"},
            "note_category_names": {
                "type": "array",
                "items": {"type": "string"}
            }
        },
        "required": ["guide_login", "country_names", "note_title", "note_category_names"],
        "maxProperties": 4,
        "additionalProperties": False
    }

"""
put_route_for_note
"""
put_route_for_note = \
    {
        "type": "object",
        "properties": {
            "note_title": {"type": "string"},
            "landmark_info_position_dicts": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "position": {"type": "number"},
                        "longitude": {"type": "number"},
                        "latitude": {"type": "number"}
                    },
                    "required": ["name", "position", "longitude", "latitude"],
                    "additionalProperties": False,
                    "maxProperties": 4
                }
            },
        },
        "required": ["note_title", "landmark_info_position_dicts"],
        "maxProperties": 2,
        "additionalProperties": False
    }

"""
put_route_saved_by_user
"""
put_route_saved_by_user = \
    {
        "type": "object",
        "properties": {
            "user_login": {"type": "string"},
            "landmark_info_position_dicts": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "position": {"type": "number"},
                        "longitude": {"type": "number"},
                        "latitude": {"type": "number"}
                    },
                    "required": ["name", "position", "longitude", "latitude"],
                    "additionalProperties": False,
                    "maxProperties": 4
                }
            },
        },
        "required": ["user_login", "landmark_info_position_dicts"],
        "maxProperties": 2,
        "additionalProperties": False
    }

"""
saved_relationship_for_existing_route
"""
saved_relationship_for_existing_route = \
    {
        "type": "object",
        "properties": {
            "user_login": {"type": "string"},
            "index_id": {"type": "number"},
        },
        "required": ["user_login", "index_id"],
        "maxProperties": 2,
        "additionalProperties": False
    }
