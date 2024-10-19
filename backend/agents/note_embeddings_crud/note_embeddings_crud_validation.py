"""
get_nearest_notes
"""
get_nearest_notes = \
{
    "type": "object",
    "properties": {
        "note_embedding": {
            "type": "array",
            "items": {
                "type": "number"
            },
            "additionalProperties": False
        },
        "limit": "number",
        "return_embeddings": "bool"
    },
    "required": [
        "note_embedding", "limit"
    ],
    "additionalProperties": False,
    "max_properties": 3
}