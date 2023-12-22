# Purpose: Custom responses for FastAPI
# Path: backend\app\utils\responses.py

import typing

import orjson
from fastapi import Response


class OK(Response):
    media_type = "application/json"

    def __init__(
        self,
        content: typing.Any = None,
        headers: typing.Optional[typing.Mapping[str, str]] = None,
    ) -> None:
        super().__init__(content=content, status_code=200, headers=headers)

    def render(self, content) -> bytes:
        assert orjson is not None, "orjson must be installed"
        return orjson.dumps(content)


class Created(Response):
    media_type = "application/json"

    def __init__(
        self,
        content: typing.Any = None,
        headers: typing.Optional[typing.Mapping[str, str]] = None,
    ) -> None:
        super().__init__(content=content, status_code=201, headers=headers)

    def render(self, content) -> bytes:
        assert orjson is not None, "orjson must be installed"
        return orjson.dumps(content)


class Accepted(Response):
    media_type = "application/json"

    def __init__(
        self,
        content: typing.Any = None,
        headers: typing.Optional[typing.Mapping[str, str]] = None,
    ) -> None:
        super().__init__(content=content, status_code=202, headers=headers)

    def render(self, content) -> bytes:
        assert orjson is not None, "orjson must be installed"
        return orjson.dumps(content)
