#! /usr/bin/env python3
from pathlib import Path

from starlink import Starlink

import asyncio
from uvicorn import Config, Server
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import HTMLResponse, FileResponse
from fastapi_versioning import VersionedFastAPI, version
from loguru import logger
from typing import Any
from mavlink2rest import Mavlink2Rest


SERVICE_NAME = "Starlink Position"

app = FastAPI(
    title="StarLink Position",
    description="Provide MAVLink position from starlink",
)

logger.info(f"Starting {SERVICE_NAME}!")


@app.get("/position", status_code=status.HTTP_200_OK)
@version(1, 0)
async def position() -> Any:
    position = Starlink.position()
    logger.info(f"position: {position}")
    return position


async def periodic() -> None:
    while True:
        await asyncio.sleep(1)
        mavlink = Mavlink2Rest()
        try:
            position = Starlink.position()
            mavlink.send_gps_input_simple(
                position["latitude"],
                position["longitude"],
                position["altitude"],
                gps_id=1,
            )
        except Exception as error:
            print(f"Failed to get position: {error}")
            await asyncio.sleep(10)


app = VersionedFastAPI(
    app, version="1.0.0", prefix_format="/v{major}.{minor}", enable_latest=True
)

app.mount("/", StaticFiles(directory="static", html=True), name="static")


@app.get("/", response_class=FileResponse)
async def root() -> Any:
    return "index.html"


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    config = Config(app=app, loop=loop, host="0.0.0.0", port=80, log_config=None)
    server = Server(config)

    loop.create_task(periodic())
    loop.run_until_complete(server.serve())
