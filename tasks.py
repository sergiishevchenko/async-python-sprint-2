from pathlib import Path
from typing import Callable

from logger import get_logger
from schema import ForecastSchema
from utils import RANDOM_FOLDER_NAME, RANDOM_FILE_NAME
from yandex_weather_api import YandexWeatherAPI

logger = get_logger()


def create_folder() -> None:
    for i in range(5):
        path = Path(f'{RANDOM_FOLDER_NAME} {i + 1}')
        if not path.is_dir():
            path.mkdir()
            logger.info('Папка создана - %s.', path)
    logger.info('Папка создана')


def delete_folder() -> None:
    for i in range(5):
        path = Path(f'{RANDOM_FOLDER_NAME} {i + 1}')
        if path.is_dir():
            path.rmdir()
            logger.info('Удаляем папку ... %s.', path)
    logger.info('Папка удалена!')


def create_file() -> None:
    with open(RANDOM_FILE_NAME, 'w', encoding='UTF-8') as file:
        message = 'Файл {} успешно создан.'.format(RANDOM_FILE_NAME)
        file.write(f'{message}\n')
    logger.info(msg=message)


def write_down_to_file() -> None:
    with open(RANDOM_FILE_NAME, 'a', encoding='UTF-8') as file:
        file.writelines(['Lorem {i + 1}\n' for i in range(10)])
    logger.info('Запись в файл окончена.')


def read_from_file() -> None:
    try:
        with open(RANDOM_FILE_NAME, 'r', encoding='UTF-8') as file:
            for line in file.readlines():
                logger.info(line.strip())
        logger.info('Чтение файла {} окончено.'.format(RANDOM_FILE_NAME))
    except EnvironmentError as err:
        logger.error(err)


def delete_file() -> None:
    path = Path(RANDOM_FILE_NAME)
    if path.is_file():
        path.unlink()
        logger.info('Удаляем файл ... %s.', path)
    logger.info('Файл удалён!')


def get_forecasts() -> None:
    try:
        forecasts = ForecastSchema.parse_obj(YandexWeatherAPI().get_forecasting())
        logger.info('Данные извлечены.')
    except Exception as err:
        logger.error(err)
    logger.info('Прогноз погоды извлечён.')


def run_task(task: str) -> Callable:
    return tasks[task]


tasks = {
    'create_folder': create_folder,
    'delete_folder': delete_folder,

    'create_file': create_file,
    'write_to_file': write_down_to_file,
    'read_from_file': read_from_file,
    'delete_file': delete_file,

    'get_forecasts': get_forecasts
}
