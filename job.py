from datetime import datetime
from multiprocessing import Process
from threading import Thread, Timer
from typing import Generator
from uuid import uuid4

from coroutine import coroutine
from logger import get_logger
from tasks import run_task
from utils import TIME_MASK


logger = get_logger()


class Job:
    """Класс задачи для планировщика."""

    def __init__(self,
                 task: str,
                 uid: str = '',
                 start_at: str = '',
                 max_working_time: int = -1,
                 tries: int = 0,
                 dependencies: list = None
        ):
        self.task = run_task(task)

        if start_at:
            self.start_at = datetime.strptime(start_at, TIME_MASK)
        else:
            self.start_at = None
        self.uid = uid if uid else uuid4().hex
        self.max_working_time = max_working_time
        self.tries = tries
        self.dependencies = dependencies or []
        self.worker = None

    @staticmethod
    def start_job(job: 'Job') -> None:
        task_name = job.task.__name__
        start_at = job.start_at
        if job.start_at and job.start_at > datetime.now():
            total_seconds = (job.start_at - datetime.now()).total_seconds()
            worker = Timer(total_seconds, job.task)
            worker.start()
            logger.info('Задача "%s" запущена в: %s.', task_name, start_at)
        else:
            if job.max_working_time >= 0:
                worker = Process(target=job.task)
                worker.start()
                worker.join(job.max_working_time)
                if worker.is_alive():
                    worker.terminate()
                    logger.info('Задача "%s" остановлена.', task_name)
            else:
                worker = Thread(target=job.task)
                worker.start()
                worker.join()
        job.worker = worker

    @staticmethod
    @coroutine
    def run() -> Generator[None, 'Job', None]:
        while job := (yield):
            try:
                Job.start_job(job)
            except GeneratorExit:
                logger.info('Метод start_job() остановлен.')
                raise
            except Exception as err:
                logger.error(err)
                while job.tries > 0:
                    job.tries -= 1
                    task_name = job.task.__name__
                    try:
                        Job.start_job(job)
                        logger.info('Задача "%s" успешно завершена.', task_name)
                    except Exception as err:
                        logger.error(err)
