from pydantic import BaseModel


class TaskSchema(BaseModel):
    name: str
    start_at: str
    max_working_time: int
    tries: int
    dependencies: list


class WeatherDetailSchema(BaseModel):
    hour: str
    temp: int
    condition: str


class WeatherSchema(BaseModel):
    date: str
    hours: list[WeatherDetailSchema]


class ForecastSchema(BaseModel):
    forecasts: list[WeatherSchema]
