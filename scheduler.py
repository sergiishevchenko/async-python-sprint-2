import datetime
import json
import time
from typing import Optional, List

from coroutine import coroutine
from job import Job, JobStatus
from schema import TaskSchema
from logger import get_logger
from tasks import test_tasks


logger = get_logger('root')


class Scheduler:
    """Класс планировщика."""

    def __init__(self, pool_size: int = 10) -> None:
        self.pool_size: int = pool_size
        self.tasks: list[Job] = []
        self.is_active_scheduler = False

    def schedule_task(self, task: Job) -> None:
        if self.get_task_from_scheduler(task.id):
            logger.warning('Задача уже поставлена.')

        if task.dependencies:
            for dependency in task.dependencies:
                if dependency not in self.tasks:
                    self.schedule_task(dependency)

        self.tasks.append(task)
        logger.info('Задача добавлена в Scheduler.')

    def get_or_create_job(self, task_id, fn_name, args, kwargs, start_at, max_working_time, tries, status, dependencies) -> List[Job]:
        job = self.get_tasks_with_status(task_id)
        if job:
            return job
        return Job(id=task_id, fn=test_tasks.get(fn_name), args=args, kwargs=kwargs, start_at=start_at,
                   max_working_time=max_working_time, tries=tries,
                   status=JobStatus.IN_QUEUE if status == JobStatus.IN_PROCESS else status,
                   dependencies=dependencies)

    def get_task(self, target) -> None:
        while self.is_active_scheduler:
            self.tasks.sort()
            if self.tasks[0].status == JobStatus.IN_QUEUE:
                if self.tasks[0].is_task_completed() is False:
                    self.tasks[0].set_next_time()

                if len(self.get_tasks_with_status(JobStatus.IN_PROCESS)) < self.pool_size:
                    self.tasks[0].status = JobStatus.IN_PROCESS
                    target.send(self.tasks[0])
                else:
                    logger.info('Размер пула больше, чем 10!')

    def get_tasks_with_status(self, status) -> list[Job]:
        return [task for task in self.tasks if task.status == status]

    @coroutine
    def execute_task(self):
        while task := (yield):
            try:
                task.result = task.run()
                task.status = JobStatus.IS_COMPLETED
            except Exception as error:
                logger.error('Ошибка - {}'.format(error))
                if task.tries > 0:
                    task.set_next_time()
                    task.tries -= 1
                    task.status = JobStatus.IN_QUEUE
                else:
                    task.status = JobStatus.IS_ERROR

    def run(self) -> None:
        logger.info('Scheduler стартанул.')
        self.is_active_scheduler = True
        executed_task = self.execute_task()
        self.get_task(executed_task)

    def restart(self) -> None:
        try:
            with open('result.json') as file:
                tasks = json.load(file)
        except Exception as error:
            logger.exception("Ошибка - {}".format(error))

        for task in tasks:
            try:
                task = TaskSchema.parse_raw(task)
            except TypeError as error:
                logger.error("Ошибка - {}".format(error))
                continue

            dependencies = []

            for dependence in task.dependencies:
                dependencies.append(
                    self.get_or_create_job(id_job=dependence.id, fn_name=dependence.fn_name,
                                           args=dependence.args, kwargs=dependence.kwargs, start_at=dependence.start_at,
                                           max_working_time=dependence.max_working_time,
                                           tries=dependence.tries,
                                           status=dependence.status,
                                           dependencies=dependence.dependencies))
            task_job = self.get_or_create_job(
                job_id=task.id,
                fn_name=task.fn_name,
                start_at=task.start_at,
                max_working_time=task.max_working_time,
                tries=task.tries,
                status=task.status,
                args=task.args,
                kwargs=task.kwargs,
                dependencies=dependencies
            )
            self.schedule_task(task=task_job)

        logger.info('Scheduler перезапустился!')
        self.run()

    def get_task_from_scheduler(self, task_id) -> Optional[Job]:
        try:
            job = next(task for task in self.tasks if task.id == task_id)
        except StopIteration:
            job = None
        return job

    def stop(self) -> None:
        self.is_active_scheduler = False
        tasks = []
        for task in self.tasks:
            task_dict = task.__dict__
            task_dict['dependencies'] = [task.__dict__ for task in task_dict['dependencies']]
            tasks.append(TaskSchema.parse_obj(task.__dict__).json())
        with open('result.json', 'w') as file:
            json.dump(tasks, file)
        logger.info('Scheduler остановился!')
