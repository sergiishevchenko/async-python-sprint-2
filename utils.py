import json

from datetime import datetime, timedelta


CITIES = {
    "MOSCOW": "https://code.s3.yandex.net/async-module/moscow-response.json",
    "PARIS": "https://code.s3.yandex.net/async-module/paris-response.json",
    "LONDON": "https://code.s3.yandex.net/async-module/london-response.json",
    "BERLIN": "https://code.s3.yandex.net/async-module/berlin-response.json",
    "BEIJING": "https://code.s3.yandex.net/async-module/beijing-response.json",
    "KAZAN": "https://code.s3.yandex.net/async-module/kazan-response.json",
    "SPETERSBURG": "https://code.s3.yandex.net/async-module/spetersburg-response.json",
    "VOLGOGRAD": "https://code.s3.yandex.net/async-module/volgograd-response.json",
    "NOVOSIBIRSK": "https://code.s3.yandex.net/async-module/novosibirsk-response.json",
    "KALININGRAD": "https://code.s3.yandex.net/async-module/kaliningrad-response.json",
    "ABUDHABI": "https://code.s3.yandex.net/async-module/abudhabi-response.json",
    "WARSZAWA": "https://code.s3.yandex.net/async-module/warszawa-response.json",
    "BUCHAREST": "https://code.s3.yandex.net/async-module/bucharest-response.json",
    "ROMA": "https://code.s3.yandex.net/async-module/roma-response.json",
    "CAIRO": "https://code.s3.yandex.net/async-module/cairo-response.json",

    "GIZA": "https://code.s3.yandex.net/async-module/giza-response.json",
    "MADRID": "https://code.s3.yandex.net/async-module/madrid-response.json",
    "TORONTO": "https://code.s3.yandex.net/async-module/toronto-response.json"
}

MIN_MAJOR_PYTHON_VER = 3
MIN_MINOR_PYTHON_VER = 9
ERR_MESSAGE_TEMPLATE = "Unexpected error: {error}"

RANDOM_FILE_NAME = 'results.txt'
RANDOM_FOLDER_NAME = 'new folder'
JOBS_FILE_NAME = 'file_with_jobs.json'

TIME_MASK = '%d.%m.%Y %H:%M:%S'

NEXT_TIME = datetime.now() + timedelta(seconds=5)
DELAY_TIME = NEXT_TIME.strftime(TIME_MASK)

DEFAULT_DURATION = 0.1


def check_python_version():
    import sys

    if (
        sys.version_info.major < MIN_MAJOR_PYTHON_VER
        or sys.version_info.minor < MIN_MINOR_PYTHON_VER
    ):
        raise Exception(
            "Please use python version >= {}.{}".format(
                MIN_MAJOR_PYTHON_VER, MIN_MINOR_PYTHON_VER
            )
        )


def get_url_by_city_name(city_name):
    try:
        return CITIES[city_name]
    except KeyError:
        raise Exception("Please check that city {} exists".format(city_name))


def get_job_data(job):
    start_at = job.start_at or ''
    if isinstance(start_at, datetime):
        start_at = start_at.strftime(TIME_MASK)
    return {'name': job.task.__name__, 'start_at': start_at, 'max_working_time': job.max_working_time, 'tries': job.tries, 'dependencies': []}


def load_json() -> dict:
    try:
        with open(JOBS_FILE_NAME, 'r', encoding='UTF-8') as file:
            try:
                return json.load(file)
            except ValueError:
                return {}
    except EnvironmentError:
        return {}


def save_data_in_json(job: dict) -> None:
    with open(JOBS_FILE_NAME, 'w', encoding='UTF-8') as file:
        json.dump(job, file)
