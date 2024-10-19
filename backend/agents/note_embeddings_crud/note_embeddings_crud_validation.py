# Author: Vodohleb04

# Read queries
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
        "limit": {"type": "number"},
        "return_embeddings": {"type": "boolean"}
    },
    "required": [
        "note_embedding", "limit"
    ],
    "additionalProperties": False,
    "max_properties": 3
}


# Write queries
"""
add_note_embedding
"""
add_note_embedding = \
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
        "note_title": {"type": "string"}
    },
    "required": [
        "note_embedding", "note_title"
    ],
    "additionalProperties": False,
    "max_properties": 2
}


# Update queries
"""
update_note_embedding
"""
update_note_embedding = \
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
        "note_title": {"type": "string"}
    },
    "required": [
        "note_embedding", "note_title"
    ],
    "additionalProperties": False,
    "max_properties": 2
}


# Delete queries
"""
delete_notes
"""
delete_notes = \
{
    "type": "object",
    "properties": {
        "note_title_list": {
            "type": "array",
            "items": {
                "type": "string"
            },
            "additionalProperties": False
        }
    },
    "required": [
        "note_title_list"
    ],
    "additionalProperties": False,
    "max_properties": 1
}