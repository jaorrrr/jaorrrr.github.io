// Ponto único de importação para as páginas: escolhe entre a API real
// (rosetti/backend, usada em `npm run dev`) e a versão estática em
// localStorage (usada no build `--mode static`, ex.: GitHub Pages).
import * as apiClient from './api.js';
import * as localApiClient from './localApi.js';

const isStatic = import.meta.env.VITE_DATA_MODE === 'static';
const client = isStatic ? localApiClient : apiClient;

export const fetchCategories = client.fetchCategories;
export const fetchItems = client.fetchItems;
export const verifyAdminAuth = client.verifyAdminAuth;
export const fetchAdminItems = client.fetchAdminItems;
export const createAdminItem = client.createAdminItem;
export const updateAdminItem = client.updateAdminItem;
export const toggleAdminItemField = client.toggleAdminItemField;
export const deleteAdminItem = client.deleteAdminItem;

export { getStoredAuth, setStoredAuth, clearStoredAuth, buildBasicAuthHeader } from './authStorage.js';
