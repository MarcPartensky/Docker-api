#!/usr/bin/env python

import docker

from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel


client = docker.DockerClient()

app = FastAPI()


@app.get("/")
async def index():
    return "docker-api"


@app.get("/containers")
async def containers():
    """List all containers."""
    return [c.attrs for c in client.containers.list()]


@app.get("/containers/ids")
async def containers_ids():
    """List all containers ids."""
    return [c.id for c in client.containers.list()]


@app.get("/images")
async def images():
    """List all available images."""
    return [i.attrs for i in client.images.list()]


@app.get("/container/{id}")
async def container(id: str):
    """Return one container."""
    return client.containers.get(id).attrs


@app.get("/container/{id}/logs")
async def container_logs(id: str):
    """Return the logs of a container."""
    container = client.containers.get(id)
    return container.logs()


@app.post("/container/{id}/restart")
async def container_restart(id: str):
    """Restart a container."""
    container = client.containers.get(id)
    container.restart()
    return "restarted"


@app.post("/container/{id}/kill")
async def container_kill(id: str):
    """Kill a container."""
    container = client.containers.get(id)
    container.kill()
    return "killed"


@app.post("/container/{id}/stop")
async def container_stop(id: str):
    """Stop a container."""
    container = client.containers.get(id)
    container.stop()
    return "stopped"


@app.post("/container/{id}/remove")
async def container_stop(id: str):
    """Stop a container."""
    container = client.containers.get(id)
    container.remove()
    return "removed"
