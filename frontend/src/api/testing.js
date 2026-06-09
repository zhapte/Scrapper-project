import { getStoredToken } from './auth.js'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

async function authorizedRequest(path, options = {}) {
  const token = getStoredToken()

  if (!token) {
    throw new Error('No login token found. Please log in again.')
  }

  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
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

export function seedProducts() {
  return authorizedRequest('/seed-products', {
    method: 'POST',
  })
}

export function getProducts() {
  return authorizedRequest('/products')
}

export function getMe() {
  return authorizedRequest('/auth/me')
}
