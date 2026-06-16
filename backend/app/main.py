from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.constants import ALLOWED_ORIGINS, APP_TITLE, APP_VERSION
from app.routers import admin, home, result, survey, user
from app.services.csv_service import ensure_csv_files

ensure_csv_files()

app = FastAPI(title=APP_TITLE, version=APP_VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    # allow_credentials=True,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(home.router)
app.include_router(user.router)
app.include_router(survey.router)
app.include_router(result.router)
app.include_router(admin.router)


@app.get("/")
def root():
    return {"message": "ADHD 자가진단 API 서버가 실행 중입니다."}
