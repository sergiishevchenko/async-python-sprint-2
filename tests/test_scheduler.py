import datetime

from job import JobStatus


class TestScheduler:

    def test_schedule_task(self, scheduler, job):
        scheduler.schedule_task(job)
        assert job in scheduler.tasks

    def test_schedule_inner_task(self, scheduler, job_test_inner, job_test_with_inner):
        scheduler.schedule_task(job_test_with_inner)
        assert job_test_with_inner in scheduler.tasks
        assert job_test_inner in scheduler.tasks

    def test_get_or_create_job(self, scheduler, job_test_inner, job_test_with_inner):
        scheduler.schedule_task(job_test_with_inner)
        job = scheduler.get_or_create_job(
            fn_name='task_test_0',
            task_id='12143432423145sdf235435',
            start_at=datetime.datetime(year=2023, month=1, day=1, hour=0, minute=0, second=0),
            max_working_time=20,
            tries=0,
            args=[],
            kwargs={},
            dependencies=[],
            status=JobStatus.IN_PROCESS
        )
        assert job.id == '12143432423145sdf235435'
        assert job.start_at == datetime.datetime(year=2023, month=1, day=1, hour=0, minute=0, second=0)
        assert job.max_working_time == 20
        assert job.status == JobStatus.IN_QUEUE

    def test_get_task_from_scheduler(self, scheduler, job_test_inner, job_test_with_inner):
        scheduler.schedule_task(job_test_with_inner)
        job = scheduler.get_task_from_scheduler(task_id='12143432423145sdf235435')
        assert job is None
