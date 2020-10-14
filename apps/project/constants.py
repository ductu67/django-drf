from enum import Enum


class StatusType(Enum):
    CANCELED = 1
    COMPLETED = 2
    INITIALIZING = 3
    INPROGRESS = 4
    NOT_STARTED = 5
    PENDING = 6

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class ProjectType(Enum):
    DOMESTIC = 1
    INTERNATIONAL = 2

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]



