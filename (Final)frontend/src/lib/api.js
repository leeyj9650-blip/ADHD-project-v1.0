const BASE_URL = '/api';

async function request(path, options = {}) {
  const response = await fetch(`${BASE_URL}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...(options.headers || {})
    },
    ...options
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: '요청 처리에 실패했습니다.' }));
    throw new Error(error.detail || '요청 처리에 실패했습니다.');
  }

  const contentType = response.headers.get('content-type') || '';
  if (contentType.includes('application/json')) {
    return response.json();
  }
  return response;
}

export const api = {
  startUser: (payload) => request('/user/start', { method: 'POST', body: JSON.stringify(payload) }),
  resumeUser: (user_id) => request('/user/resume', { method: 'POST', body: JSON.stringify({ user_id }) }),
  getQuestions: () => request('/survey/questions'),
  saveAnswer: (payload) => request('/survey/answer', { method: 'POST', body: JSON.stringify(payload) }),
  getProgress: (userId) => request(`/survey/progress/${userId}`),
  getReview: (userId) => request(`/survey/review/${userId}`),
  updateReviewAnswer: (payload) => request('/survey/review/update', { method: 'POST', body: JSON.stringify(payload) }),
  finalizeResult: (userId) => request(`/result/finalize/${userId}`, { method: 'POST' }),
  getLatestResult: (userId) => request(`/result/latest/${userId}`),
  adminLogin: (payload) => request('/admin/login', { method: 'POST', body: JSON.stringify(payload) }),
  getAdminResults: () => request('/admin/results'),
  getAdminStats: () => request('/admin/stats')
};

export const BASE_API_URL = BASE_URL;