"""
recommendations_agent_coefficients_json
"""
recommendations_agent_coefficients_json = \
  {
      "type": "object",
      "properties": {
          "main_categories_names": {"type": "number"},
          "subcategories_names": {"type": "number"},
          "distance": {"type": "number"},
          "wish_to_visit": {"type": "number"},
          "visited_amount": {"type": "number"}
      },
      "required": [
          "main_categories_names",
          "subcategories_names",
          "distance",
          "wish_to_visit",
          "visited_amount"
      ],
      "additionalProperties": False
  }

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
            "amount_of_additional_recommendations_for_point": {"type": "number"},
            "maximum_amount_of_recommendations": {"type": "number"},
            "maximum_amount_of_additional_recommendations": {"type": "number"},
            "optional_limit": {"type": ["number", "null"]},
        },
        "required": [
            "coordinates_of_points",
            "categories_names",
            "user_login",
            "amount_of_recommendations_for_point",
            "amount_of_additional_recommendations_for_point",
            "maximum_amount_of_recommendations",
            "maximum_amount_of_additional_recommendations"
        ],
        "additionalProperties": False
 }
