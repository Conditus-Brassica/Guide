"""
recommendations_agent_coefficients_json
"""

"""
find_recommendations_for_coordinates_and_categories
"""
find_recommendations_for_coordinates_and_categories = \
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
            "categories_names": {
                "type": "array",
                "items": {"type": "string"}
            },
            "user_login": {"type": "string"},
            "amount_of_recommendations_for_point": {"type": "number"},
            "maximum_amount_of_recommendations": {"type": "number"},
            "optional_limit": {"type": ["number", "null"]}
        },
        "required": [
            "coordinates_of_points",
            "categories_names",
            "user_login",
            "amount_of_recommendations_for_point",
            "maximum_amount_of_recommendations"
        ],
        "additionalProperties": False
 }
