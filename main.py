from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import create_db_and_tables
from routes.task_routes import router as task_router
from routes.auth_routes import router as auth_router
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

BASE_DIR = Path(__file__).resolve().parent
FRONT_DIR = BASE_DIR / "front"

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(
    title="Todo API",
    description="API para gerenciamento de tarefas com autenticação JWT.",
    version="2.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(task_router)


@app.get("/", include_in_schema=False)
def serve_index():
    return FileResponse(FRONT_DIR / "index.html")


app.mount("/", StaticFiles(directory=FRONT_DIR, html=True), name="front")