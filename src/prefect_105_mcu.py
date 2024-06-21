import httpx
from prefect import flow, get_run_logger


@flow
def iron_man_fact():
    return "I.. Am... IronMan <3000"

@flow
def captain_america_fact():
    return "I can do this all day!"

@flow
def spiderman_fact():
    return "Great Power comes with great responsibilities!"

@flow(log_prints=True)
def marvel_ism():
    logger = get_run_logger()
    im = iron_man_fact()
    ca = captain_america_fact()
    sm = spiderman_fact()
    logger.info(f"Loading ...")
    print(f"Iron Man: {im}\nCaptain America: {ca}\nSpiderman: {sm}")

if __name__ == "main":
    marvel_ism.serve(name="prefect-105")