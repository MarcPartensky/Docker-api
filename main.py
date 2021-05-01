from typing import Optional

from fastapi import FastAPI

import docker

client = docker.from_env()

app = FastAPI()


@app.get("/")
async def index():
    return "hi"


@app.get("/containers")
async def containers():
    """List all available containers."""
    return client.containers.list()


@app.get("/images")
async def images():
    """List all available images."""
    return client.images()


@app.get("/container/{id}")
async def container(id: str):
    """Return one container."""
    return client.containers.get(id)


@app.get("/container/{id}/logs")
async def container_logs(id: str):
    """Return the logs of a container."""
    container = client.containers.get(id)
    return container.logs()


@app.post("/container/{id}/restart")
async def container_restart(id: str):
    """Restart one container."""
    container = client.containers.get(id)
    return container.restart()


@app.post("/container/{id}/stop")
async def container_stop(id: str):
    """Stop one container."""
    container = client.containers.get(id)
    return container.stop()
