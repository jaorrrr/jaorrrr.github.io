// Implementação client-side das mesmas funções de api.js, para rodar sem
// backend (build estático, ex.: GitHub Pages). Os dados vivem no
// localStorage do navegador; não há persistência compartilhada entre
// visitantes nem segurança real de servidor — ver aviso no README.
import { categories, initialItems, categoryById } from './localData.js';

const ITEMS_STORAGE_KEY = 'rosetti_static_items';

// SHA-256("admin:rosetti123"). Troque gerando o hash do seu próprio usuário:senha
// (ex.: no console do navegador, via crypto.subtle.digest) — isso ofusca a
// senha no bundle, mas não substitui autenticação real de servidor.
const ADMIN_CREDENTIALS_HASH =
  'fa13f4095e620af41beb37710affbe5ccaf4313c515fe8c636d767513fa34796';

function loadItems() {
  const stored = localStorage.getItem(ITEMS_STORAGE_KEY);
  if (!stored) return initialItems;
  try {
    return JSON.parse(stored);
  } catch {
    return initialItems;
  }
}

function saveItems(items) {
  localStorage.setItem(ITEMS_STORAGE_KEY, JSON.stringify(items));
  return items;
}

function delay(ms = 120) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function sha256Hex(text) {
  const bytes = new TextEncoder().encode(text);
  const digest = await crypto.subtle.digest('SHA-256', bytes);
  return Array.from(new Uint8Array(digest))
    .map((b) => b.toString(16).padStart(2, '0'))
    .join('');
}

function decodeBasicAuth(authHeader) {
  const [scheme, encoded] = (authHeader || '').split(' ');
  if (scheme !== 'Basic' || !encoded) return null;
  const decoded = atob(encoded);
  const separatorIndex = decoded.indexOf(':');
  return decoded.slice(0, separatorIndex + 1) + decoded.slice(separatorIndex + 1);
}

async function assertAuthorized(authHeader) {
  const credentials = decodeBasicAuth(authHeader);
  if (!credentials) {
    const error = new Error('Autenticação necessária');
    error.status = 401;
    throw error;
  }
  const hash = await sha256Hex(credentials);
  if (hash !== ADMIN_CREDENTIALS_HASH) {
    const error = new Error('Usuário ou senha inválidos');
    error.status = 401;
    throw error;
  }
}

export function fetchCategories() {
  return delay().then(() => categories);
}

export async function fetchItems(params = {}) {
  await delay();
  const { category, search, vegetarian, featured } = params;
  let items = loadItems();

  if (category) {
    items = items.filter((item) => item.categorySlug === category);
  }
  if (search) {
    const term = search.toLowerCase();
    items = items.filter(
      (item) =>
        item.name.toLowerCase().includes(term) || item.description.toLowerCase().includes(term)
    );
  }
  if (vegetarian === 'true') {
    items = items.filter((item) => item.isVegetarian);
  }
  if (featured === 'true') {
    items = items.filter((item) => item.isFeatured);
  }
  return items;
}

export async function verifyAdminAuth(authHeader) {
  await assertAuthorized(authHeader);
  return { ok: true };
}

export async function fetchAdminItems(authHeader) {
  await assertAuthorized(authHeader);
  await delay();
  return loadItems();
}

function validatePayload(payload) {
  const errors = [];
  if (!payload.name) errors.push('Nome é obrigatório');
  if (!payload.categoryId) errors.push('Categoria é obrigatória');
  if (payload.price === undefined || Number.isNaN(Number(payload.price))) {
    errors.push('Preço inválido');
  }
  if (errors.length) {
    const error = new Error(errors.join(', '));
    error.status = 400;
    throw error;
  }
}

export async function createAdminItem(authHeader, payload) {
  await assertAuthorized(authHeader);
  validatePayload(payload);
  const items = loadItems();
  const nextId = items.reduce((max, item) => Math.max(max, item.id), 0) + 1;
  const category = categoryById(payload.categoryId);
  const newItem = {
    id: nextId,
    categoryId: Number(payload.categoryId),
    categorySlug: category?.slug,
    name: payload.name,
    description: payload.description || '',
    price: Number(payload.price),
    imageUrl: payload.imageUrl || `placeholders/${category?.slug || 'antipasti'}.svg`,
    isVegetarian: !!payload.isVegetarian,
    isSpicy: !!payload.isSpicy,
    isBestseller: !!payload.isBestseller,
    isFeatured: !!payload.isFeatured,
    isSoldOut: !!payload.isSoldOut,
  };
  items.push(newItem);
  saveItems(items);
  return newItem;
}

export async function updateAdminItem(authHeader, id, payload) {
  await assertAuthorized(authHeader);
  validatePayload(payload);
  const items = loadItems();
  const index = items.findIndex((item) => item.id === Number(id));
  if (index === -1) {
    const error = new Error('Item não encontrado');
    error.status = 404;
    throw error;
  }
  const category = categoryById(payload.categoryId);
  const updated = {
    ...items[index],
    categoryId: Number(payload.categoryId),
    categorySlug: category?.slug || items[index].categorySlug,
    name: payload.name,
    description: payload.description || '',
    price: Number(payload.price),
    imageUrl: payload.imageUrl || items[index].imageUrl,
    isVegetarian: !!payload.isVegetarian,
    isSpicy: !!payload.isSpicy,
    isBestseller: !!payload.isBestseller,
    isFeatured: !!payload.isFeatured,
    isSoldOut: !!payload.isSoldOut,
  };
  items[index] = updated;
  saveItems(items);
  return updated;
}

export async function toggleAdminItemField(authHeader, id, field) {
  await assertAuthorized(authHeader);
  const camelField = field === 'is_sold_out' ? 'isSoldOut' : 'isFeatured';
  const items = loadItems();
  const index = items.findIndex((item) => item.id === Number(id));
  if (index === -1) {
    const error = new Error('Item não encontrado');
    error.status = 404;
    throw error;
  }
  items[index] = { ...items[index], [camelField]: !items[index][camelField] };
  saveItems(items);
  return items[index];
}

export async function deleteAdminItem(authHeader, id) {
  await assertAuthorized(authHeader);
  const items = loadItems();
  const filtered = items.filter((item) => item.id !== Number(id));
  saveItems(filtered);
}
