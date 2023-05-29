import datetime

from pydantic import BaseModel
from typing import Optional
from uuid import UUID

from job import JobStatus


class TaskDetailSchema(BaseModel):
    id: UUID
    fn_name: str
    args: list
    kwargs: dict
    start_at: datetime.datetime
    max_working_time: Optional[int]
    tries: int
    status: JobStatus
    dependencies: list


class TaskSchema(TaskDetailSchema):
    dependencies: list[TaskDetailSchema]
