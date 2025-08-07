import uvicorn
from fastapi import FastAPI

from app.routers import api_router
from app.utils.lifespan import lifespan

app = FastAPI(
    title="OrganizationApp",
    lifespan=lifespan,
)
app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run(app="__main__:app", host="0.0.0.0", port=8000)
