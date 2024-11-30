"""
make_snippet_embedding
"""
make_snippet_embedding = \
 {
        "type": "object",
        "properties": {
            "text": {"type": "string"},
            "window_size": {"type": "number"},
            "intersection_with_prev_window": {"type": "number"}
        },
        "required": [
            "text"
        ],
        "additionalProperties": False
 }


"""
make_recommendation_embedding
"""
make_recommendation_embedding = \
 {
        "type": "object",
        "properties": {
            "text": {"type": "string"},
            "window_size": {"type": "number"},
            "intersection_with_prev_window": {"type": "number"}
        },
        "required": [
            "text"
        ],
        "additionalProperties": False
 }

