
from scheduler import Scheduler
from tests.conftest import create_tasks_for_tests


def restart_scheduler(scheduler) -> None:
    scheduler.restart()


def stop_scheduler(scheduler) -> None:
    create_tasks_for_tests(scheduler)

    scheduler.stop()


def main():
    scheduler = Scheduler()
    stop_scheduler(scheduler)

    scheduler = Scheduler()
    restart_scheduler(scheduler)


if __name__ == "__main__":
    main()
