from enum import Enum


class JobStatus(Enum):
    IN_QUEUE = 0
    IN_PROCESS = 1
    IS_COMPLETED = 2
    IS_ERROR = 3