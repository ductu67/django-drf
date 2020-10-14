from enum import Enum


class WorkingType(Enum):
    FULL_TIME = 1
    PART_TIME = 2


class LanguageType(Enum):
    ENGLISH = 'en'
    JAPANESE = 'jp'
    FRENCH = 'fr'

class PositionType(Enum):
    SUB_LEADER_1 = 1
    SUB_LEADER_2 = 2
    LEADER = 3
    GROUP_LEADER = 4
    MANAGER = 5
    DIRECTOR = 6