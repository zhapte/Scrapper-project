const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'
const TOKEN_STORAGE_KEY = 'scraper_access_token'

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  })

  const data = await response.json().catch(() => null)

  if (!response.ok) {
    throw new Error(data?.detail || 'Request failed')
  }

  return data
}

export function getStoredToken() {
  return localStorage.getItem(TOKEN_STORAGE_KEY)
}

export function setStoredToken(token) {
  localStorage.setItem(TOKEN_STORAGE_KEY, token)
}

export function clearStoredToken() {
  localStorage.removeItem(TOKEN_STORAGE_KEY)
}

export async function registerUser(userData) {
  return request('/auth/register', {
    method: 'POST',
    body: JSON.stringify(userData),
  })
}

export async function loginUser(credentials) {
  return request('/auth/login', {
    method: 'POST',
    body: JSON.stringify(credentials),
  })
}

export async function requestPasswordReset(passwordResetRequest) {
  return request('/auth/forgot-password', {
    method: 'POST',
    body: JSON.stringify(passwordResetRequest),
  })
}

export async function resetPassword(passwordResetData) {
  return request('/auth/reset-password', {
    method: 'POST',
    body: JSON.stringify(passwordResetData),
  })
}

export async function getCurrentUser(token) {
  return request('/auth/me', {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })
}
