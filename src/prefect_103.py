import httpx
import pendulum
from prefect import flow, task, get_run_logger
import random
from prefect.blocks.system import DateTime
from prefect.tasks import task_input_hash
from prefect.artifacts import create_markdown_artifact
import os

data_time_block = DateTime.load("date-block")

@task(task_run_name="{task_run}")
def fetch_weather(task_run="feathing_weather", lat: float = 38.9, lon: float = -77.0):
    logger = get_run_logger()
    logger.info(f"{task_run} task")
    base_url = "https://api.open-meteo.com/v1/forecast/"
    temps = httpx.get(
        base_url,
        params=dict(latitude=lat, longitude=lon, hourly="temperature_2m"),
    )
    forecasted_temp = float(temps.json()["hourly"]["temperature_2m"][0])
    print(f"Forecasted temp C: {forecasted_temp} degrees")
    report(forecasted_temp)
    return forecasted_temp

@task(task_run_name="saving_data")
def save_data(content: float):
    logger = get_run_logger()
    logger.info(f"saving data task")
    with open("weather.csv", "w+") as file:
        file.write(str(content))
    return "Data saved."

@task(task_run_name="generating_random_num", cache_key_fn=task_input_hash)
def random_num_generator(data: float):
    return float(data-random.choice([20,35]))

@task
def report(data):
    markdown_rep = f"""# Weather Report
    
    ## Recent weather
    
    | Time        | Temperature |
    |:--------------|-------:|
    | Temp Forecast  | {data} |
    """
    create_markdown_artifact(
        key="weather-report",
        markdown=markdown_rep,
        description="Very scientific weather report",
    )




@flow(retries =5,flow_run_name="today-run")
def pipeline(lat=12, lon=21):
    logger = get_run_logger()
    logger.info(f"Block usage: {data_time_block}")
    data = fetch_weather( lat=lat, lon=lon)
    res = random_num_generator( data=data)
    logger.info(f"Random num: {res}\n ENV: {os.getenv('dev')}")
    # if res < 0.0:
    #     raise Exception
    return save_data(content=data)


if __name__ == "__main__":
    pipeline.serve(name="prefect_103") 