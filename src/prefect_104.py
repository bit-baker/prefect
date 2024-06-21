from prefect import flow

import httpx
from prefect import flow

if __name__ == "__main__":
    flow.from_source(
        source="https://github.com/bit-baker/prefect.git",
        entrypoint="src/prefect_103.py:pipeline",
    ).deploy(
        name="my-first-managed-deployment",
        work_pool_name="pool-1",
    )