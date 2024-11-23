import enum
import json


class UserReaction(float, enum.Enum):

    LIKE = 2.0
    NEUTRAL = 1.0
    DISLIKE = 0.1


class EnumEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, enum.Enum):
            return obj.value

        return super().default(obj)


