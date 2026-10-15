from enum import Enum


class RunStatus(str, Enum):
    ACTIVE = "ACTIVE"
    FAILED = "FAILED"
    COMPLETED = "COMPLETED"
    ABANDONED = "ABANDONED"


class RunStage(str, Enum):
    DRAFT = "DRAFT"
    GYM = "GYM"
    ELITE_FOUR = "ELITE_FOUR"
    CHAMPION = "CHAMPION"
    FINISHED = "FINISHED"
