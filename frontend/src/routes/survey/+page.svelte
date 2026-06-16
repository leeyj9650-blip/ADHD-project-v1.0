<script>
  import { onMount, tick } from 'svelte';
  import { goto } from '$app/navigation';
  import ChoiceButtons from '$lib/components/ChoiceButtons.svelte';
  import ProgressBar from '$lib/components/ProgressBar.svelte';
  import HomeButton from '$lib/components/HomeButton.svelte';
  import { api } from '$lib/api';
  import { getUserId } from '$lib/storage';
  import { createRecognizer, correctSpeechText, mapSpeechToChoice, playBeep, speakText, stopSpeaking } from '$lib/voice';

  let userId = '';
  let questions = [];
  let currentIndex = 0;
  let selectedChoiceId = null;
  let answers = {};
  let statusText = '준비 중';
  let voiceState = 'idle';
  let transcript = '';
  let recognitionSupported = true;
  let recognition = null;
  let waitingTimeout = null;
  let pendingSaveTimeout = null;
  let error = '';
  let ttsRate = 0.95;
  let ttsVolume = 1;
  let showTtsPanel = true;

  // [수정됨] Enter 중복 입력 / keydown 중복 실행 방지용
  let isMovingQuestion = false;

  $: currentQuestion = questions[currentIndex];

  $: voiceStateLabel = {
    idle: '대기 중',
    reading: '질문 읽는 중',
    listening: '음성 인식 중',
    recognized: '인식 완료',
    manual: '수동 선택',
    error: '수동 선택 필요'
  }[voiceState] || '대기 중';

  // [수정됨] onMount(async () => {}) 구조 제거
  // [수정됨] 이벤트 정리 함수가 정상 동작하도록 onMount는 동기 함수로 유지
  onMount(() => {
    const keyHandler = (event) => {
      const tag = event.target?.tagName?.toLowerCase();

      if (tag === 'input' || tag === 'textarea' || tag === 'select') return;
      if (!currentQuestion) return;

      // [수정됨] 키를 길게 눌러 반복 입력되는 경우 차단
      if (event.repeat) return;

      // [수정됨] 다음 문항 이동 중에는 키보드 입력 무시
      if (isMovingQuestion) return;

      if (['1', '2', '3', '4'].includes(event.key)) {
        event.preventDefault();
        selectManual(Number(event.key) - 1);
        return; // [수정됨] 숫자키 처리 후 아래 Enter 조건으로 이어지지 않게 종료
      }

      if (event.key === 'Enter' && selectedChoiceId !== null) {
        event.preventDefault();
        nextQuestion();
        return; // [수정됨]
      }
    };

    window.addEventListener('keydown', keyHandler);

    // [수정됨] 비동기 초기화는 별도 함수로 실행
    initSurvey();

    return () => {
      window.removeEventListener('keydown', keyHandler);
      stopAllVoice('idle');
      clearTimeout(pendingSaveTimeout);
    };
  });

  // [수정됨] 기존 onMount 안에 있던 비동기 초기화 코드를 함수로 분리
  async function initSurvey() {
    userId = getUserId();

    if (!userId) {
      goto('/');
      return;
    }

    try {
      const qData = await api.getQuestions();
      const progress = await api.getProgress(userId);

      questions = qData.questions;
      answers = progress.answers || {};

      const progressIndex = Math.max((progress.current_question_id || 1) - 1, 0);
      currentIndex = Math.min(progressIndex, questions.length - 1);

      await tick();

      selectedChoiceId = answers[String(currentQuestion?.question_id)]?.choice_id ?? null;

      recognition = createRecognizer({
        onStart: () => {
          voiceState = 'listening';
          statusText = '음성 인식 중입니다. 1~4번 또는 보기 내용을 말씀해주세요.';
        },
        onResult: handleSpeechResult,
        onEnd: () => {
          clearTimeout(waitingTimeout);

          if (voiceState === 'listening') {
            voiceState = 'error';
            statusText = '음성이 인식되지 않았습니다. 다시 시도하거나 직접 선택해주세요.';
          }
        },
        onError: () => {
          voiceState = 'error';
          statusText = '수동으로 선택해주세요';
        }
      });

      recognitionSupported = !!recognition;

      await autoReadQuestion();
    } catch (e) {
      error = e.message;
    }
  }

  function stopAllVoice(nextState = 'manual') {
    stopSpeaking();
    clearTimeout(waitingTimeout);

    try {
      recognition?.abort?.();
    } catch {}

    try {
      recognition?.stop?.();
    } catch {}

    voiceState = nextState;
  }

  async function autoReadQuestion() {
    await tick();

    if (!currentQuestion) return;

    selectedChoiceId = answers[String(currentQuestion.question_id)]?.choice_id ?? null;
    statusText = '질문 읽는 중';
    voiceState = 'reading';
    transcript = '';

    stopAllVoice('reading');

    speakText(
      currentQuestion.question,
      () => {
        playBeep();
        startListening();
      },
      { rate: ttsRate, volume: ttsVolume }
    );
  }

  function startListening() {
    stopSpeaking();

    if (!recognition) {
      voiceState = 'error';
      statusText = '브라우저 음성인식을 지원하지 않습니다. 수동으로 선택해주세요';
      return;
    }

    statusText = '응답 대기 중';
    voiceState = 'listening';

    try {
      recognition.stop();
    } catch {}

    try {
      recognition.start();
    } catch {
      voiceState = 'error';
      statusText = '음성 인식을 시작할 수 없습니다. 다시 시도하거나 직접 선택해주세요.';
      return;
    }

    clearTimeout(waitingTimeout);

    waitingTimeout = setTimeout(() => {
      try {
        recognition.stop();
      } catch {}

      voiceState = 'error';
      statusText = '10초 동안 응답이 없어 수동으로 선택해주세요';
    }, 10000);
  }

  function retryListening() {
    transcript = '';
    stopAllVoice('listening');
    playBeep();
    startListening();
  }

  async function handleSpeechResult(text) {
    const corrected = correctSpeechText(text);
    transcript = corrected;

    const mapped = mapSpeechToChoice(corrected);

    if (mapped === null) {
      voiceState = 'error';
      statusText = `인식 결과: ${corrected} / 다시 말씀해주세요`;
      return;
    }

    selectedChoiceId = mapped;
    voiceState = 'recognized';
    statusText = `음성응답 인식 완료: ${corrected}`;

    await saveCurrentAnswer(mapped, 'voice', corrected);
  }

  async function saveCurrentAnswer(choiceId = selectedChoiceId, method = 'manual', voiceText = '') {
    if (choiceId === null || !currentQuestion) return;

    await api.saveAnswer({
      user_id: userId,
      question_id: currentQuestion.question_id,
      choice_id: choiceId,
      voice_text: voiceText,
      method
    });

    answers[String(currentQuestion.question_id)] = { choice_id: choiceId };
  }

  function scheduleManualSave(choiceId) {
    clearTimeout(pendingSaveTimeout);

    pendingSaveTimeout = setTimeout(async () => {
      try {
        await saveCurrentAnswer(choiceId, 'manual');
        statusText = '수동 응답이 저장되었습니다';
      } catch (e) {
        error = e.message;
      }
    }, 250);
  }

  function selectManual(choiceId) {
    stopAllVoice('manual');

    selectedChoiceId = choiceId;
    transcript = '';
    statusText = '수동 응답 선택됨. TTS/STT가 중단되었습니다.';

    scheduleManualSave(choiceId);
  }

  async function flushPendingSave() {
    if (selectedChoiceId === null) return;

    clearTimeout(pendingSaveTimeout);

    await saveCurrentAnswer(selectedChoiceId, 'manual');
  }

  async function nextQuestion() {
    if (selectedChoiceId === null) return;

    // [수정됨] Enter 한 번에 nextQuestion이 여러 번 실행되는 문제 방지
    if (isMovingQuestion) return;

    // [수정됨] 문항 이동 시작
    isMovingQuestion = true;

    try {
      stopAllVoice('idle');

      await flushPendingSave();

      if (currentIndex === questions.length - 1) {
        goto('/review');
        return;
      }

      currentIndex += 1;

      // [수정됨] 다음 문항으로 넘어갈 때 이전 선택값 초기화
      selectedChoiceId = null;

      await autoReadQuestion();
    } catch (e) {
      error = e.message;
    } finally {
      // [수정됨] 문항 이동 종료
      isMovingQuestion = false;
    }
  }
</script>

<div class="survey-shell">
  <div class="page-toolbar">
    <HomeButton confirmLeave={true} message="진행 중인 설문 화면을 벗어나 홈으로 이동하시겠습니까?" />
  </div>

  <div class="survey-card">
    <div class="survey-top">
      <div>
        <p class="eyebrow">ADHD Self Check</p>
        <h1>설문 진행</h1>
      </div>

      {#if currentQuestion}
        <div class="question-counter">Q{currentQuestion.question_id} / 20</div>
      {/if}
    </div>

    {#if error}
      <p class="error-text">{error}</p>
    {:else if currentQuestion}
      <ProgressBar current={currentQuestion.question_id} total={20} />

      <div class="survey-layout">
        <section class="question-panel">
          <div class="voice-badge state-{voiceState}">{voiceStateLabel}</div>

          <p class="question">{currentQuestion.question}</p>

          <ChoiceButtons choices={currentQuestion.choices} {selectedChoiceId} onSelect={selectManual} />

          <div class="actions main-actions">
            <button class="secondary" on:click={autoReadQuestion}>질문 다시 듣기</button>
            <button class="secondary interrupt" on:click={retryListening}>마이크로 답변</button>

            <!-- [수정됨] 이동 중에는 다음 버튼도 비활성화 -->
            <button class="primary" on:click={nextQuestion} disabled={selectedChoiceId === null || isMovingQuestion}>
              {currentIndex === questions.length - 1 ? '최종 점검으로' : '다음'}
            </button>
          </div>

          <p class="helper">단축키: 1~4번 선택, Enter 다음 문항</p>
        </section>

        <aside class="side-panel">
          <div class="info-card">
            <h3>음성 상태</h3>

            <div class="status-line">{statusText}</div>

            <div class="transcript-box">
              {transcript || '아직 인식된 텍스트가 없습니다.'}
            </div>
          </div>

          <div class="info-card">
            <button class="panel-toggle" on:click={() => showTtsPanel = !showTtsPanel}>
              TTS 설정 {showTtsPanel ? '접기' : '열기'}
            </button>

            {#if showTtsPanel}
              <label class="range-field">
                <span>읽기 속도 {ttsRate.toFixed(2)}</span>
                <input type="range" min="0.7" max="1.25" step="0.05" bind:value={ttsRate} />
              </label>

              <label class="range-field">
                <span>볼륨 {Math.round(ttsVolume * 100)}%</span>
                <input type="range" min="0" max="1" step="0.05" bind:value={ttsVolume} />
              </label>
            {/if}
          </div>

          {#if !recognitionSupported}
            <p class="helper">이 브라우저는 Web Speech API를 지원하지 않아 수동 선택 위주로 사용해야 합니다.</p>
          {/if}
        </aside>
      </div>
    {/if}
  </div>
</div>