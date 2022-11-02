#!/usr/bin/env python

import docker

from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

client = docker.DockerClient()

app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=[""],
    allow_headers=[""],
)


@app.get("/")
async def index():
    return "docker-api"


@app.get("/live")
async def healthcheck():
    return "Ok"


@app.get("/images")
async def images():
    """List all available images."""
    return [i.attrs for i in client.images.list()]


@app.get("/ps")
async def ps_all():
    """List all containers."""
    return [c.attrs for c in client.containers.list()]


@app.get("/ps/ids")
async def ps_ids():
    """List all containers ids."""
    return [c.id for c in client.containers.list()]


@app.get("/ps/{id}")
async def ps_one(id: str):
    """Return one container."""
    return client.containers.get(id).attrs


@app.post("/exec/{id}/{cmd}")
async def exec(id: str, cmd: str):
    """Return one container."""
    container = client.containers.get(id)
    return container.exec_run(cmd)


@app.get("/top/{id}")
async def top(id: str):
    """Show processes for all containers"""
    container = client.containers.get(id)
    return container.top()


@app.get("/logs/{id}/{since}")
async def logs(id: str, since: int = 1):
    """Return the logs of a container."""
    container = client.containers.get(id)
    return container.logs(since=since)


@app.post("/restart/{id}")
async def restart(id: str):
    """Restart a container."""
    container = client.containers.get(id)
    container.restart()
    return "restarted"


@app.post("/rename/{id}/{name}")
async def rename(id: str, name: str):
    """Rename a container."""
    container = client.containers.get(id)
    container.rename(name)
    return "renamed to " + name


@app.post("/kill/{id}")
async def kill(id: str):
    """Kill a container."""
    container = client.containers.get(id)
    container.kill()
    return "killed"


@app.post("/stop/{id}")
async def stop(id: str):
    """Stop a container."""
    container = client.containers.get(id)
    container.stop()
    return "stopped"


@app.post("/remove/{id}")
async def remove(id: str):
    """Stop a container."""
    container = client.containers.get(id)
    container.remove()
    return "removed"


@app.post("/pause/{id}")
async def pause(id: str):
    """Pause a container."""
    container = client.containers.get(id)
    container.pause()
    return "paused"


@app.post("/unpause/{id}")
async def unpause(id: str):
    """Unpause a container."""
    container = client.containers.get(id)
    container.unpause()
    return "unpaused"
