import os

from yandex_weather_api import YandexWeatherAPI


def task_test_0():
    return get_weather_for_city(CITY_NAME="MOSCOW")


def task_test_1():
    return get_weather_for_city(CITY_NAME="PARIS")


def task_test_2():
    return get_weather_for_city(CITY_NAME="LONDON")


def task_test_3():
    return get_weather_for_city(CITY_NAME="BERLIN")


def task_test_4():
    return get_weather_for_city(CITY_NAME="BEIJING")


def task_test_inner_0():
    return get_weather_for_city(CITY_NAME="BEIJING")


def task_test_inner_1():
    return get_weather_for_city(CITY_NAME="KAZAN")


def task_test_inner_2():
    return get_weather_for_city(CITY_NAME="SPETERSBURG")


def task_test_inner_3():
    return get_weather_for_city(CITY_NAME="VOLGOGRAD")


def get_weather_for_city(CITY_NAME):
    if not os.path.exists(CITY_NAME):
        os.makedirs(CITY_NAME)
    else:
        os.rmdir(CITY_NAME)

    yandexAPI = YandexWeatherAPI()

    response = yandexAPI.get_forecasting(CITY_NAME)
    with open(f"{CITY_NAME}.txt", "w") as file:
        file.write(str(response.get("info")))
    return response.get("info")


test_tasks = {
    'task_test_0': task_test_0,
    'task_test_1': task_test_1,
    'task_test_2': task_test_2,
    'task_test_3': task_test_3,
    'task_test_4': task_test_4,

    'task_test_inner_0': task_test_inner_0,
    'task_test_inner_1': task_test_inner_1,
    'task_test_inner_2': task_test_inner_2,
    'task_test_inner_3': task_test_inner_3,
}
