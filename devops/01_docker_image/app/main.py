from fastapi import FastAPI

app = FastAPI(title="Container Study API", version="1.0.0")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "Hello from a container"}

