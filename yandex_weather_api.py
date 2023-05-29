import json
from http import HTTPStatus

from logger import get_logger
from urllib.error import HTTPError
from urllib.request import urlopen
from utils import ERR_MESSAGE_TEMPLATE, get_url_by_city_name


logger = get_logger('root')


class YandexWeatherAPI:
    """
    Base class for requests
    """

    def __do_req(url: str) -> str:
        """Base request method"""
        try:
            with urlopen(url) as response:
                resp_body = response.read().decode("utf-8")
                data = json.loads(resp_body)
            if response.status != HTTPStatus.OK:
                raise HTTPError(
                    "Error during execute request. {}: {}".format(
                        resp_body.status, resp_body.reason
                    )
                )
            return data
        except Exception as error:
            logger.error(error)
            raise Exception(ERR_MESSAGE_TEMPLATE.format(error=error))

    @staticmethod
    def get_forecasting(city: str):
        url = get_url_by_city_name(city)
        return YandexWeatherAPI.__do_req(url)