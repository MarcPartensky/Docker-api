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


@app.get("/container/{id}/exec/{cmd}")
async def container_exec(id: str, cmd: str):
    """Return one container."""
    container = client.containers.get(id)
    return container.exec_run(cmd)


@app.get("/container/{id}/top")
async def container_top(id: str):
    """Show processes for all containers"""
    container = client.containers.get(id)
    return container.top()


@app.get("/container/{id}/logs/{since}")
async def container_logs(id: str, since: int = 1):
    """Return the logs of a container."""
    container = client.containers.get(id)
    return container.logs(since=since)


@app.post("/container/{id}/restart")
async def container_restart(id: str):
    """Restart a container."""
    container = client.containers.get(id)
    container.restart()
    return "restarted"


@app.post("/container/{id}/rename/{name}")
async def container_rename(id: str, name: str):
    """Rename a container."""
    container = client.containers.get(id)
    container.rename(name)
    return "renamed to " + name


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
async def container_remove(id: str):
    """Stop a container."""
    container = client.containers.get(id)
    container.remove()
    return "removed"


@app.post("/container/{id}/pause")
async def container_pause(id: str):
    """Pause a container."""
    container = client.containers.get(id)
    container.pause()
    return "paused"


@app.post("/container/{id}/unpause")
async def container_unpause(id: str):
    """Unpause a container."""
    container = client.containers.get(id)
    container.unpause()
    return "unpaused"
