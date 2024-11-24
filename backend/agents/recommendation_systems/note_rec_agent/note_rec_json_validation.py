from backend.agents.recommendation_systems.note_rec_sys_user_reaction import UserReaction

"""
make_recommendations
"""
make_recommendations = \
 {
        "type": "object",
        "properties": {
            "state": {
                "type": "array",
                "items": {
                    "type": "number"
                }
            },
            "maximum_amount_of_recommendations": {"type": "number"}
        },
        "required": [
            "state",
            "maximum_amount_of_recommendations"
        ],
        "additionalProperties": False
 }


"""
interaction_with_note_started
"""
interaction_with_note_started = \
{
    "type": "object",
    "properties": {
        "state": {
            "type": "array",
            "items": {
                "type": "number"
            }
        },
        "note_title": "string"
    },
    "required": [
        "state",
        "note_title"
    ],
    "additionalProperties": False
}


"""
interaction_with_note_finished
"""
interaction_with_note_finished = \
{
    "type": "object",
    "properties": {
        "interactions": {
            "type": "array",
            "items": {
                "row_uuid": "string",
                "row_index": "number",
                "user_reaction": {
                    "enum": [UserReaction.LIKE, UserReaction.NEUTRAL, UserReaction.DISLIKE]
                },
                "relative_interaction_time": "number"
            },
            "required": [
                "row_uuid",
                "row_index",
                "user_reaction",
                "relative_interaction_time"
            ],
            "additionalProperties": False
        }
    },
    "required": [
        "interactions"
    ],
    "additionalProperties": False
}


"""
count_new_state
"""
count_new_state = \
{
    "type": "object",
    "properties": {
        "new_notes": {
            "type": "array",
            "items": {
                "title": "string"
            },
            "required": [
                "title"
            ],
            "additionalProperties": False
        },
        "state": {
            "type": "array",
            "items": {
                "type": "number"
            }
        }
    },
    "required": [
        "new_notes",
        "state"
    ],
    "additionalProperties": False
}

