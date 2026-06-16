import { browser } from '$app/environment';

const KEY = 'adhd_user_id';

export function saveUserId(userId) {
  if (browser) localStorage.setItem(KEY, userId);
}

export function getUserId() {
  if (!browser) return null;
  return localStorage.getItem(KEY);
}

export function clearUserId() {
  if (browser) localStorage.removeItem(KEY);
}
