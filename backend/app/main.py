from fastapi import FastAPI

app = FastAPI(
    title="Blacksmith Knight API",
    description="Forging Heaven — Backend API for Blacksmith Knight",
    version="0.1.0",
)


@app.get("/")
def read_root():
    return {"message": "Blacksmith Knight API online", "status": "ok"}


@app.get("/health")
def read_health():
    return {"status": "ok"}
