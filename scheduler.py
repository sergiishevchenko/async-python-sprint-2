from datetime import datetime
from typing import Optional

from job import Job
from logger import get_logger
from schema import TaskSchema
from utils import get_job_data, load_json, save_data_in_json

logger = get_logger()


class Scheduler:
    """Класс планировщика."""

    def __init__(self, pool_size: int = 10):
        self.job = Job.run()
        self.pool_size = pool_size
        self.queue = []

    @staticmethod
    def load_from_file() -> list[Job]:
        jobs, dependencies = [], {}
        for key, value in load_json().items():
            task = TaskSchema.parse_obj(value)
            jobs.append(Job(uid=key, task=task.name, start_at=task.start_at,
                            max_working_time=task.max_working_time, tries=task.tries, dependencies=[])
                        )
            dependencies[key] = task.dependencies
        for job in jobs:
            job.dependencies = [x for x in jobs if x.uid in dependencies[job.uid]]
        return jobs

    @staticmethod
    def save_to_file(queue: list[Job]) -> None:
        data = dict()
        for job in queue:
            job_data = get_job_data(job)
            for dependency in job.dependencies:
                if dependency in queue:
                    job_data['dependencies'].append(dependency.uid)
            data[job.uid] = job_data
        save_data_in_json(data)

    def schedule_tasks(self, jobs: list[Job]) -> None:
        self.queue = self.load_from_file()
        for job in jobs:
            self.queue.append(job)
            task_name = job.task.__name__
            if self.pool_size < len(self.queue):
                logger.error('Очередь заполнена.')
                continue
            if job.start_at and job.start_at > datetime.now():
                logger.warning('Задача "%s" добавлена в %s', task_name, job.start_at)
            else:
                logger.info('Задача "%s" добавлена в schedule_tasks', task_name)

    def append_job_to_queue(self) -> Optional[Job]:
        job = self.queue.pop(0)
        task_name = job.task.__name__
        if job.start_at and job.start_at < datetime.now():
            logger.info('Вышло время на добавление задачи "%s".', task_name)
            return None
        if job.dependencies:
            for dependency in job.dependencies:
                if (dependency in self.queue or dependency.worker and dependency.worker.is_alive()):
                    self.queue.append(job)
                    return None
        return job

    def run(self) -> None:
        counter = 0
        if self.queue:
            logger.info('Начало планировки задач.')
        while self.queue and counter < self.pool_size:
            job = self.append_job_to_queue()
            if job:
                counter += 1
                self.job.send(job)
        self.save_to_file(self.queue)
