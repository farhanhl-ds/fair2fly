from fastapi import FastAPI

app = FastAPI(title="fair2fly API")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
