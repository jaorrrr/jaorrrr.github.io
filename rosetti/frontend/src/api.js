const API_BASE = '/api';
const AUTH_STORAGE_KEY = 'rosetti_admin_auth';

export function getStoredAuth() {
  return sessionStorage.getItem(AUTH_STORAGE_KEY);
}

export function setStoredAuth(basicAuthHeader) {
  sessionStorage.setItem(AUTH_STORAGE_KEY, basicAuthHeader);
}

export function clearStoredAuth() {
  sessionStorage.removeItem(AUTH_STORAGE_KEY);
}

export function buildBasicAuthHeader(username, password) {
  return `Basic ${btoa(`${username}:${password}`)}`;
}

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
  });

  if (!response.ok) {
    let message = `Erro ${response.status}`;
    try {
      const data = await response.json();
      if (data.error) message = data.error;
    } catch {
      // resposta sem corpo JSON
    }
    const error = new Error(message);
    error.status = response.status;
    throw error;
  }

  if (response.status === 204) return null;
  return response.json();
}

export function fetchCategories() {
  return request('/categories');
}

export function fetchItems(params = {}) {
  const query = new URLSearchParams(
    Object.entries(params).filter(([, value]) => value !== undefined && value !== '')
  ).toString();
  return request(`/items${query ? `?${query}` : ''}`);
}

export function verifyAdminAuth(authHeader) {
  return request('/admin/verify', { headers: { Authorization: authHeader } });
}

export function fetchAdminItems(authHeader) {
  return request('/admin/items', { headers: { Authorization: authHeader } });
}

export function createAdminItem(authHeader, payload) {
  return request('/admin/items', {
    method: 'POST',
    headers: { Authorization: authHeader },
    body: JSON.stringify(payload),
  });
}

export function updateAdminItem(authHeader, id, payload) {
  return request(`/admin/items/${id}`, {
    method: 'PUT',
    headers: { Authorization: authHeader },
    body: JSON.stringify(payload),
  });
}

export function toggleAdminItemField(authHeader, id, field) {
  return request(`/admin/items/${id}/toggle`, {
    method: 'PATCH',
    headers: { Authorization: authHeader },
    body: JSON.stringify({ field }),
  });
}

export function deleteAdminItem(authHeader, id) {
  return request(`/admin/items/${id}`, {
    method: 'DELETE',
    headers: { Authorization: authHeader },
  });
}
