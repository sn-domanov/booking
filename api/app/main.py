from fastapi import FastAPI

app = FastAPI()


@app.get("/live")
async def liveness():
    return {"status": "alive"}