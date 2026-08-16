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
