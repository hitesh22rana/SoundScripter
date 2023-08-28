# Purpose: Custom responses for FastAPI
# Path: backend\app\utils\responses.py

import typing

import orjson
from fastapi import Response


class OK(Response):
    media_type = "application/json"

    def __init__(self, content: typing.Any = None) -> None:
        super().__init__(content, 200)

    def render(self, content) -> bytes:
        assert orjson is not None, "orjson must be installed"
        return orjson.dumps(content)


class Created(Response):
    media_type = "application/json"

    def __init__(self, content: typing.Any = None) -> None:
        super().__init__(content, 201)

    def render(self, content) -> bytes:
        assert orjson is not None, "orjson must be installed"
        return orjson.dumps(content)


class Accepted(Response):
    media_type = "application/json"

    def __init__(self, content: typing.Any = None) -> None:
        super().__init__(content, 202)

    def render(self, content) -> bytes:
        assert orjson is not None, "orjson must be installed"
        return orjson.dumps(content)
