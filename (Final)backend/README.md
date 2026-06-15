# backend

## 실행

```bash
cd backend
python -m venv .venv
.venv\\Scripts\\activate # windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

기본 주소: `http://127.0.0.1:8000`

관리자 기본 계정:
- id: `admin`
- password: `1234`
