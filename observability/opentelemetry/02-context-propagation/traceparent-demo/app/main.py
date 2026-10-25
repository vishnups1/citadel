import logging

from fastapi import FastAPI, Request

app = FastAPI()
log = logging.getLogger("uvicorn.error")


@app.get("/")
def hello(request: Request):
    traceparent = request.headers.get("traceparent")
    log.info("[app]   received traceparent=%s", traceparent)
    return {
        "message": "Hello, World!",
        "traceparent_received": traceparent,
        "tracestate_received": request.headers.get("tracestate"),
    }
