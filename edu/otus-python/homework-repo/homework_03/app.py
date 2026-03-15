"""Minimal FastAPI application used in tests.

The application exposes a single endpoint ``/ping/`` that returns a JSON
response ``{"message": "pong"}``.  The tests build a Docker image from this
module and run it, therefore the module also contains an explicit entrypoint
so it can be executed directly with ``python app.py``.
"""

from fastapi import FastAPI
import uvicorn


app = FastAPI()


@app.get("/ping/")
async def ping() -> dict[str, str]:
    """Return a simple JSON response used by the tests."""

    return {"message": "pong"}


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000)
