from fastapi import FastAPI, Depends
from app.api.api_v1.routers.users import users_router
from starlette.requests import Request
import uvicorn


from app.api.api_v1.routers.auth import auth_router


from app.core import config
from app.db.session import SessionLocal
from app.core.auth import get_current_active_user
from app import tasks
from fastapi.middleware.cors import CORSMiddleware


from app.db.session import Base, engine


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=config.PROJECT_NAME, docs_url="/api/docs", openapi_url="/api"
)


origins = [
    "*",
]


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    request.state.db = SessionLocal()
    response = await call_next(request)
    request.state.db.close()
    return response



app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/api/v1")
async def root():
    return {"message": "Hello World"}


@app.get("/api/v1/task")
async def example_task():
    celery_app.send_task("app.tasks.example_task", args=["Hello World"])

    return {"message": "success"}


#Routers
app.include_router(
    users_router,
    prefix="/api/v1",
    tags=["users"],
    dependencies=[Depends(get_current_active_user)],
)   
