from fastapi import FastAPI
from server.routes.user import router as UserRouter

app = FastAPI()

app.include_router(UserRouter, prefix="/user", tags=["user"])
