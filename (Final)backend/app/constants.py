from pathlib import Path

APP_TITLE = "ADHD 자가진단 API"
APP_VERSION = "1.0.0"

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
USERS_CSV = DATA_DIR / "users.csv"
RESPONSES_CSV = DATA_DIR / "responses.csv"  # summary by completed survey
RESULTS_CSV = DATA_DIR / "results.csv"      # detailed per-question answers by completed survey
DRAFTS_JSON = DATA_DIR / "draft_answers.json"

# ALLOWED_ORIGINS = [
#     "http://localhost:5173",
#     "http://127.0.0.1:5173",
# ]

ALLOWED_ORIGINS = ["*"]

CHOICES = [
    {"choice_id": 0, "text": "전혀 아니다", "score": 0},
    {"choice_id": 1, "text": "가끔 그렇다", "score": 1},
    {"choice_id": 2, "text": "자주 그렇다", "score": 3},
    {"choice_id": 3, "text": "매우 그렇다", "score": 5},
]

CHOICE_ID_TO_SCORE = {item["choice_id"]: item["score"] for item in CHOICES}
INATTENTION_IDS = {1, 2, 3, 4, 5, 6, 7, 8, 9, 20}
HYPERACTIVE_IDS = {10, 11, 12, 13, 14, 15, 16, 17, 18, 19}
ADMIN_ID = "admin"
ADMIN_PASSWORD = "1234"
