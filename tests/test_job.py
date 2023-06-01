import datetime


class TestJob:

    def test_set_next_time(self, job):
        job.set_next_time()
        assert job.start_at==datetime.datetime(year=2022, month=1, day=1, hour=0, minute=10, second=0)

    def test_is_task_completed_true(self, job):
        assert job.is_task_completed() is True

    def test_is_task_completed_false(self, job_test_with_inner):
        assert job_test_with_inner.is_task_completed() is False

    def test_is_start_datetime(self, job):
        job.is_start_datetime()
        assert job.start_at==datetime.datetime(year=2022, month=1, day=1, hour=0, minute=0, second=0)
