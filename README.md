# 음성 인터랙션 기반 ADHD 자가진단 지원 시스템 (ADHD 자가진단 ♥)

> **"기존의 지루하고 피로도 높은 텍스트 설문을 넘어, 음성으로 소통하는 메디컬 AI 보조 시스템 프로토타입"**

> 본 프로젝트는 브라우저 기반 음성 안내(TTS)와 음성 응답 인식(STT)을 적용하여 사용자의 참여도와 접근성을 극대화한 ADHD 자가진단 보조 도구입니다.

---

## 📅 프로젝트 개요
- **개발 기간**: 2026.04 (약 3주)
- **개발 인원**: 3인 (팀 프로젝트)
- **과정명**: 융합 메디컬 AI with 스마트 웰니스

---

## 🛠️ 기술 스택 및 아키텍처

### 1. Technology Stack
- **Backend**: Python, FastAPI, Uvicorn, Pydantic
- **Frontend**: SvelteKit, Vite, JavaScript
- **Voice Interaction**: Web Speech API (`speechSynthesis` [TTS], `SpeechRecognition` [STT])
- **Data Management**: CSV (유저 및 응답 저장), JSON (임시 데이터)

### 2. System Architecture
본 시스템은 확장성과 유지보수성을 고려하여 3계층 구조(3-Tier Architecture)로 설계되었습니다.

`SvelteKit (화면 단)` → `FastAPI Routers` → `Services` → `Data (CSV/JSON)`

---

## 🎯 핵심 기능 및 프로세스

1. **사용자 세션 관리**: 안내문 동의 후 고유 유저 ID 발급 및 기존 설문 상태 이어하기 기능 제공
2. **스마트 음성 안내 (TTS)**: 한국어 질문 자동 낭독 및 속도/볼륨 조절 기능
3. **음성 인식 응답 (STT)**: 사용자의 음성 답변을 텍스트로 변환 후 보기 번호/문구로 매핑
4. **예외 처리 및 Fallback**: 브라우저 미지원 또는 **10초 무응답 시 즉시 수동 선택(버튼) 유도 및 TTS/STT 중단**
5. **데이터 시각화 및 관리**: 최종 점수 계산(부주의 점수, 과잉행동/충동성 점수), 관리자 페이지 내 성별/연령/지역별 통계 그래프 및 CSV 다운로드 기능

---

## 👤 나의 기여 및 담당 역할 (My Role)

### 1. 예외 처리 및 Fallback 로직 설계 (핵심 기여)
- 음성 인식(STT) 환경에서 발생할 수 있는 '무응답 예외 상황'을 방지하기 위해 **10초 타이머 기반의 Fallback 메커니즘을 구현**했습니다.
- 10초간 응답이 없을 경우, 시스템이 완전히 멈추는 대신 **사용자에게 시각적 팝업을 통해 수동 선택을 유도**하고, 진행 중이던 TTS와 STT를 안전하게 중단(Clear)시켜 자원 낭비와 버그를 막았습니다.

### 2. 프론트엔드-백엔드 데이터 흐름 연동 및 예외 처리
- 사용자가 입력한 데이터와 설문 상태가 끊기지 않고 원활하게 흐를 수 있도록 프론트엔드 화면과 백엔드 REST API 사이의 유기적인 인터랙션을 연동하고 테스트했습니다.
- 기획안에 명시된 데이터 구조(users, responses, draft_answers)가 비즈니스 로직에 맞게 정확히 적재되는지 검증했습니다.

---

## ⚙️ 실행 방법 (Getting Started)

### Backend
```
cd backend
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend
```
cd frontend
npm install
npm run dev
```

### 기본 접속 주소: http://127.0.0.1:5173

---

## 💡 프로젝트를 통해 얻은 점 (Retrospective)
- **협업의 가치**: 백엔드(FastAPI)와 프론트엔드(SvelteKit)가 데이터를 주고받는 과정에서 명세서(API)와 역할 분담의 중요성을 깊이 깨달았습니다.
- **사용자 경험(UX) 고려**: 웹 스피치 기술을 단순 구현하는 것에 그치지 않고, '무응답 10초 예외 처리'와 같은 사용자 흐름(Flow) 중심의 Fallback 기능을 고민하며 진정한 의미의 '보조 시스템'을 구축하는 경험을 쌓았습니다.
