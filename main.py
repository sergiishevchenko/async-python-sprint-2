from job import Job
from scheduler import Scheduler
from utils import DELAY_TIME


if __name__ == '__main__':
    scheduler = Scheduler(pool_size=8)

    create_folder = Job('create_folder', start_at=DELAY_TIME)
    delete_folder = Job('delete_folder', dependencies=[create_folder])

    create_file = Job('create_file')
    write_down_to_file = Job('write_down_to_file')
    read_from_file = Job('read_from_file', tries=3, dependencies=[create_file])
    delete_file = Job('delete_file', dependencies=[create_file, write_down_to_file, read_from_file])

    get_forecasts = Job('get_forecasts')

    # ставим задачи в очередь с помощью метода schedule_tasks
    scheduler.schedule_tasks([
        create_folder,
        delete_folder,

        create_file,
        write_down_to_file,
        read_from_file,
        delete_file,

        get_forecasts
    ])

    scheduler.run()
