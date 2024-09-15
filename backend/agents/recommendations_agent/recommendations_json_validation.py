"""
find_recommendations_for_coordinates
"""
find_recommendations_for_coordinates = \
 {
        "type": "object",
        "properties": {
            "coordinates_of_points": {
                "type": "array",
                "items": {
                    "latitude": "number",
                    "longitude": "number"
                },
                "required": [
                    "latitude",
                    "longitude"
                ],
                "additionalProperties": False
            },
            "watch_state": {
                "type": "array",
                "items": {
                    "type": "number"
                }
            },
            "visit_state": {
                "type": "array",
                "items": {
                    "type": "number"
                }
            },
            "maximum_amount_of_recommendations": {"type": "number"}
        },
        "required": [
            "coordinates_of_points",
            "watch_state",
            "visit_state",
            "maximum_amount_of_recommendations"
        ],
        "additionalProperties": False
 }


"""
post_result_of_recommendations
"""
post_result_of_recommendations = \
{
    "type": "object",
    "properties": {
        "primary_recommendations": {
            "type": "array",
            "items": {
                "name": "string",
                "latitude": "number",
                "longitude": "number",
                "row_index": "number",
                "row_uuid": "string"  # uuid 
            },
            "required": [
                "name",
                "latitude",
                "longitude",
                "row_index",
                "row_uuid"
            ],
            "additionalProperties": False
        },
        "result_recommendations": {
            "type": "array",
            "items": {
                "name": "string",
                "latitude": "number",
                "longitude": "number"
            },
            "required": [
                "name",
                "latitude",
                "longitude"
            ],
            "additionalProperties": True
        },
        "new_watch_state": {
                "type": "array",
                "items": {
                    "type": "number"
                }
            },
        "new_visit_state": {
            "type": "array",
            "items": {
                "type": "number"
            }
        },
        "user_reward": {"type": "number"}
    },
    "required": [
        "primary_recommendations",
        "result_recommendations",
        "user_reward",
        "new_watch_state",
        "new_visit_state"
    ],
    "additionalProperties": False
}
