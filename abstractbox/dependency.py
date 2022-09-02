from docker import DockerClient
from docker.errors import DockerException
from fastapi.exceptions import HTTPException
from loguru import logger


async def docker_client() -> DockerClient:

    try:
        client = DockerClient.from_env()
    except DockerException as exc:
        logger.trace(f"Something went wrong while initialising the Docker client: {exc}")
        raise HTTPException(status_code=500, detail="Something went wrong while initialising the Docker client.")
    else:
        yield client
