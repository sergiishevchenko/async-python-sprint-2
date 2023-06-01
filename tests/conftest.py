import datetime
import random
import uuid

import pytest as pytest
from job import Job
from scheduler import Scheduler
from tasks import test_tasks


def get_time_for_tests():
    return datetime.datetime.now() + datetime.timedelta(seconds=(random.randrange(30) + 2))


def fn():
    pass
@pytest.fixture()
def job_test_inner():
    return Job(
        id='12143432423145sdf235435',
        fn=fn,
        start_at=datetime.datetime(year=2022, month=1, day=1, hour=0, minute=20, second=0),
        max_working_time=20,
        args=[],
        kwargs={},
        tries=0,
        dependencies=[],
    )


@pytest.fixture()
def job_test_with_inner(job_test_inner):
    return Job(
        id='121434324231454ddsf235435',
        fn=fn,
        start_at=datetime.datetime(year=2022, month=1, day=1, hour=0, minute=0, second=0),
        max_working_time=20,
        args=[],
        kwargs={},
        tries=0,
        dependencies=[job_test_inner],
    )


@pytest.fixture()
def job():
    return Job(
        id='1214343242314542354sdfds5',
        fn=fn,
        start_at=datetime.datetime(year=2022, month=1, day=1, hour=0, minute=0, second=0),
        max_working_time=20,
        args=[],
        kwargs={},
        tries=0,
        dependencies=[],
    )


@pytest.fixture()
def scheduler():
    return Scheduler()


def create_tasks_for_tests(scheduler):
    for i in range(20):
        job_0 = Job(
            id=uuid.uuid4(),
            fn=test_tasks[f'task_test_{i % 10}'],
            start_at=get_time_for_tests(),
            max_working_time=20,
            tries=0,
            args=[],
            kwargs={},
            dependencies=[],
        )
        scheduler.schedule_task(task=job_0)

    for i in range(5):
        job_test_inner_0 = Job(
            id=uuid.uuid4(),
            fn=test_tasks['task_test_inner_0'], kwargs={},
        )
        job_test_inner_1 = Job(
            id=uuid.uuid4(),
            fn=test_tasks['task_test_inner_1'], kwargs={},
        )
        job_test_inner_2 = Job(
            id=uuid.uuid4(),
            fn=test_tasks['task_test_inner_2'], kwargs={},
        )
        job_test_inner_3 = Job(
            id=uuid.uuid4(),
            fn=test_tasks['task_test_inner_3'], kwargs={},
        )
        job = Job(
            id=uuid.uuid4(),
            fn=test_tasks[f'task_test_{i % 4}'],
            start_at=get_time_for_tests(),
            max_working_time=20,
            tries=0,
            args=[],
            kwargs={},
            dependencies=[job_test_inner_0, job_test_inner_1, job_test_inner_2, job_test_inner_3],
        )
        scheduler.schedule_task(task=job)
