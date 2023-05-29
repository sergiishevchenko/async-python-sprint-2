import datetime

from enums import JobStatus
from logger import get_logger


logger = get_logger('root')


class Job:
    """Класс задачи для планировщика."""

    def __init__(self, id, fn, args=None, kwargs=None, start_at=datetime.datetime.now(), max_working_time=None, tries=0, dependencies=[], status=JobStatus(0)):
        self.id = id
        self.fn = fn
        self.fn_name = fn.__name__
        self.start_at = start_at
        self.max_working_time = max_working_time
        self.tries = tries
        self.dependencies = dependencies
        self.time_delta = datetime.timedelta(minutes=10)
        self.result = None
        self.status = status
        self.args = args if args is not None else []
        self.kwargs = kwargs if kwargs is not None else {}
        self.is_start_datetime()

    def run(self):
        try:
            return self.fn(*self.args, **self.kwargs)
        except Exception as error:
            logger.error('Ошибка - {}'.format(error))
            return None

    def pause(self):
        pass

    def stop(self):
        pass

    def is_task_completed(self):
        for task in self.dependencies:
            if task.status == JobStatus.IS_COMPLETED:
                continue
            else:
                return False
        return True

    def is_start_datetime(self):
        for task in self.dependencies:
            if task.start_at > self.start_at:
                self.start_at = task.start_at + datetime.timedelta(minutes=1)
