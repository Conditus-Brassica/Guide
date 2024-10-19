"""
get_landmarks_embeddings
"""
get_landmarks_embeddings = \
{
    "type": "object",
    "properties": {
        "landmarks": {
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
    },
    "required": [
        "landmarks"
    ],
    "additionalProperties": False
}