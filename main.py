#!/usr/bin/env python

import docker

from typing import Optional

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware

client = docker.from_env()

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


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Custom title",
        version="2.5.0",
        description="This is a very custom OpenAPI schema",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


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
    containers = []
    for raw_container in client.containers.list():
        print(raw_container.__dict__)
        health = None
        if "Health" in raw_container.attrs["State"]:
            health = raw_container.attrs["State"]["Health"]["Status"]
        exposed_ports = None
        if "ExposedPorts" in raw_container.attrs["Config"]:
            heatlh = raw_container.attrs["Config"]["ExposedPorts"]
            exposed_ports=list(raw_container.attrs["Config"]["ExposedPorts"].keys()),
        container = dict(
            id=raw_container.id,
            name=raw_container.name,
            image=raw_container.image.tags,
            status=raw_container.status,
            started_at=raw_container.attrs["State"]["StartedAt"],
            finished_at=raw_container.attrs["State"]["FinishedAt"],
            health=health,
            exposed_ports=exposed_ports,
            ports=raw_container.attrs["NetworkSettings"]["Ports"],
            networks=list(raw_container.attrs["NetworkSettings"]["Networks"].keys())
        )
        containers.append(container)
    print(containers)
    # return [c.attrs for c in client.containers.list()]
    return containers


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


if __name__ == "__main__":
    import os, uvicorn

    uvicorn.run(
        "app",
        host=os.environ.get("HOST") or "localhost",
        port=os.environ.get("PORT") or "8000",
        log_level=os.environ.get("LOG_LEVEL") or "info",
    )
