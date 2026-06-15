import { browser } from '$app/environment';

const MISRECOGNITION_DICTIONARY = [
  ['저녀', '전혀'], ['전여', '전혀'], ['전혀아니야', '전혀아니다'],
  ['가금', '가끔'], ['가끔그레', '가끔그렇다'], ['가끔그래', '가끔그렇다'],
  ['차주', '자주'], ['좌주', '자주'], ['자주그래', '자주그렇다'],
  ['우그러', '매우'], ['메우', '매우'], ['매우그래', '매우그렇다'],
  ['일 본', '1번'], ['이번', '2번'], ['삼 본', '3번'], ['사 본', '4번']
];

function applyMisrecognitionDictionary(text = '') {
  let corrected = text;
  for (const [wrong, right] of MISRECOGNITION_DICTIONARY) {
    corrected = corrected.replaceAll(wrong, right);
  }
  return corrected;
}

function normalize(text = '') {
  return applyMisrecognitionDictionary(text)
    .toLowerCase()
    .replace(/\s+/g, '')
    .replace(/[.,!?]/g, '')
    .replace(/입니다|이에요|예요|이요|요|할게요|해주세요|해줘|선택|응답/g, '');
}

function hasAny(text, candidates = []) {
  return candidates.some((candidate) => text.includes(candidate));
}

export function correctSpeechText(text = '') {
  return applyMisrecognitionDictionary(text);
}

export function mapSpeechToChoice(text) {
  const t = normalize(text);
  if (!t) return null;

  const ambiguousPatterns = [/전혀그렇/, /아니다그렇/, /가끔아니/, /자주아니/, /매우아니/];
  if (ambiguousPatterns.some((pattern) => pattern.test(t))) return null;

  const matchTable = [
    { candidates: ['전혀아니다', '아니다', '1번', '하나', '일번'], choiceId: 0 },
    { candidates: ['가끔그렇다', '가끔', '2번', '둘', '이번'], choiceId: 1 },
    { candidates: ['자주그렇다', '자주', '3번', '셋', '삼번'], choiceId: 2 },
    { candidates: ['매우그렇다', '매우', '4번', '넷', '사번'], choiceId: 3 }
  ];

  const matched = matchTable.filter((item) => hasAny(t, item.candidates));
  return matched.length === 1 ? matched[0].choiceId : null;
}

export function speakText(text, onEnd, options = {}) {
  if (!browser || !('speechSynthesis' in window)) {
    onEnd?.();
    return;
  }

  window.speechSynthesis.cancel();
  const utterance = new SpeechSynthesisUtterance(text);
  utterance.lang = 'ko-KR';
  utterance.rate = Number(options.rate ?? 0.95);
  utterance.volume = Number(options.volume ?? 1);
  utterance.onend = () => onEnd?.();
  window.speechSynthesis.speak(utterance);
}

export function stopSpeaking() {
  if (browser && 'speechSynthesis' in window) {
    window.speechSynthesis.cancel();
  }
}

export function playBeep() {
  if (!browser) return;
  const AudioContextClass = window.AudioContext || window.webkitAudioContext;
  if (!AudioContextClass) return;
  const context = new AudioContextClass();
  const oscillator = context.createOscillator();
  const gainNode = context.createGain();
  oscillator.connect(gainNode);
  gainNode.connect(context.destination);
  oscillator.frequency.value = 880;
  oscillator.type = 'sine';
  gainNode.gain.value = 0.1;
  oscillator.start();
  oscillator.stop(context.currentTime + 0.2);
}

export function createRecognizer({ onResult, onEnd, onError, onStart }) {
  if (!browser) return null;
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SpeechRecognition) return null;
  const recognition = new SpeechRecognition();
  recognition.lang = 'ko-KR';
  recognition.continuous = false;
  recognition.interimResults = false;

  recognition.onstart = () => onStart?.();
  recognition.onresult = (event) => {
    const transcript = event.results?.[0]?.[0]?.transcript || '';
    onResult?.(transcript);
  };
  recognition.onend = () => onEnd?.();
  recognition.onerror = (event) => onError?.(event.error);

  return recognition;
}
