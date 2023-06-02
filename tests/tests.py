import pathlib
import unittest

from job import Job
from scheduler import Scheduler
from utils import JOBS_FILE_NAME, load_json


class SchedulerTest(unittest.TestCase):
    """Класс для тестирования класса Scheduler."""

    scheduler = Scheduler()
    path = pathlib.Path(JOBS_FILE_NAME).resolve()
    amount_jobs = 3

    @staticmethod
    def assertFileNotExist(path):
        if not path.is_file():
            raise AssertionError('Файл не существует: {str()}'.format(path))

    def test_amount_jobs_for_schedule(self):
        jobs = [
            Job('create_file'),
            Job('write_down_to_file'),
            Job('read_from_file'),
            Job('delete_file'),
            Job('get_forecasts')
        ]
        len_jobs = len(jobs)
        self.scheduler.schedule_tasks(jobs)
        self.assertEqual(len(self.scheduler.queue), len_jobs, 'Количество запланированных задач не равно {}:'.format(len_jobs))

    def test_amount_jobs_in_file(self):
        amount_jobs_in_file = (len(self.scheduler.queue) - self.amount_jobs)
        self.scheduler.save_to_file(self.scheduler.queue[self.amount_jobs:])
        self.assertFileNotExist(self.path)
        self.assertEqual(len(load_json()), amount_jobs_in_file, 'Количество сохраненных задач не равно {}:'.format(amount_jobs_in_file))

    def test_load_jobs(self):
        amount_jobs_in_file = (len(self.scheduler.queue) - self.amount_jobs)
        jobs_from_file = self.scheduler.load_from_file()
        self.assertEqual(len(jobs_from_file), amount_jobs_in_file, 'Количество загруженных задач не равно {}:'.format(amount_jobs_in_file))

    def test_run_jobs(self):
        self.scheduler.schedule_tasks([])
        self.scheduler.run()
        self.assertTrue(len(self.scheduler.queue) == 0, 'Очередь задач не пуста:')
        self.assertTrue(len(load_json()) == 0, 'Файл с задачами не пуст:')


if __name__ == '__main__':
    unittest.main()
