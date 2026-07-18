import { useEffect, useState } from 'react';
import TricoloreLine from '../components/TricoloreLine.jsx';
import ItemForm from '../components/ItemForm.jsx';
import {
  buildBasicAuthHeader,
  clearStoredAuth,
  createAdminItem,
  deleteAdminItem,
  fetchAdminItems,
  fetchCategories,
  getStoredAuth,
  setStoredAuth,
  toggleAdminItemField,
  updateAdminItem,
  verifyAdminAuth,
} from '../api.js';

function formatPrice(price) {
  return price.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
}

function LoginForm({ onAuthenticated }) {
  const [username, setUsername] = useState('admin');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  async function handleSubmit(event) {
    event.preventDefault();
    setLoading(true);
    setError(null);
    const authHeader = buildBasicAuthHeader(username, password);
    try {
      await verifyAdminAuth(authHeader);
      setStoredAuth(authHeader);
      onAuthenticated(authHeader);
    } catch (err) {
      setError('Usuário ou senha inválidos.');
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-marble px-4">
      <div className="w-full max-w-sm">
        <div className="mb-6 text-center">
          <p className="text-xs uppercase tracking-[0.35em] text-rosetti-red">Rosetti</p>
          <h1 className="mt-1 font-serif text-3xl font-semibold text-rosetti-black">
            Painel administrativo
          </h1>
        </div>
        <TricoloreLine className="mb-6" />
        <form
          onSubmit={handleSubmit}
          className="space-y-4 rounded-xl border border-black/10 bg-white p-6 shadow-sm"
        >
          <label className="block text-sm font-medium">
            Usuário
            <input
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="mt-1 w-full rounded-md border border-black/20 px-3 py-2 text-sm outline-none focus:border-rosetti-red focus:ring-1 focus:ring-rosetti-red"
            />
          </label>
          <label className="block text-sm font-medium">
            Senha
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="mt-1 w-full rounded-md border border-black/20 px-3 py-2 text-sm outline-none focus:border-rosetti-red focus:ring-1 focus:ring-rosetti-red"
            />
          </label>
          {error && <p className="text-sm text-rosetti-red">{error}</p>}
          <button
            type="submit"
            disabled={loading}
            className="w-full rounded-full bg-rosetti-red px-5 py-2.5 text-sm font-semibold text-white hover:bg-rosetti-redDark disabled:opacity-60"
          >
            {loading ? 'Entrando…' : 'Entrar'}
          </button>
        </form>
      </div>
    </div>
  );
}

function AdminDashboard({ authHeader, onLogout }) {
  const [categories, setCategories] = useState([]);
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [editingItem, setEditingItem] = useState(null);
  const [showForm, setShowForm] = useState(false);

  function loadData() {
    setLoading(true);
    Promise.all([fetchCategories(), fetchAdminItems(authHeader)])
      .then(([categoriesData, itemsData]) => {
        setCategories(categoriesData);
        setItems(itemsData);
        setError(null);
      })
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }

  useEffect(() => {
    loadData();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  async function handleSubmitForm(payload) {
    try {
      if (editingItem) {
        await updateAdminItem(authHeader, editingItem.id, payload);
      } else {
        await createAdminItem(authHeader, payload);
      }
      setShowForm(false);
      setEditingItem(null);
      loadData();
    } catch (err) {
      alert(`Erro ao salvar: ${err.message}`);
    }
  }

  async function handleToggle(item, field) {
    try {
      await toggleAdminItemField(authHeader, item.id, field);
      loadData();
    } catch (err) {
      alert(`Erro ao atualizar: ${err.message}`);
    }
  }

  async function handleDelete(item) {
    if (!confirm(`Remover "${item.name}" do cardápio?`)) return;
    try {
      await deleteAdminItem(authHeader, item.id);
      loadData();
    } catch (err) {
      alert(`Erro ao remover: ${err.message}`);
    }
  }

  return (
    <div className="min-h-screen bg-marble">
      <header className="bg-rosetti-black text-white">
        <TricoloreLine />
        <div className="mx-auto flex max-w-5xl items-center justify-between px-4 py-5">
          <div>
            <p className="text-xs uppercase tracking-[0.35em] text-rosetti-red">Rosetti</p>
            <h1 className="font-serif text-2xl font-semibold">Painel administrativo</h1>
          </div>
          <button
            type="button"
            onClick={onLogout}
            className="rounded-full border border-white/30 px-4 py-1.5 text-sm hover:border-white/60"
          >
            Sair
          </button>
        </div>
      </header>

      <main className="mx-auto max-w-5xl px-4 py-8">
        <div className="mb-6 flex items-center justify-between">
          <h2 className="font-serif text-xl font-semibold">Pratos do cardápio</h2>
          <button
            type="button"
            onClick={() => {
              setEditingItem(null);
              setShowForm(true);
            }}
            className="rounded-full bg-rosetti-red px-5 py-2 text-sm font-semibold text-white hover:bg-rosetti-redDark"
          >
            + Novo prato
          </button>
        </div>

        {showForm && (
          <div className="mb-8">
            <ItemForm
              categories={categories}
              initialItem={editingItem}
              onSubmit={handleSubmitForm}
              onCancel={() => {
                setShowForm(false);
                setEditingItem(null);
              }}
            />
          </div>
        )}

        {loading && <p className="text-rosetti-black/60">Carregando…</p>}
        {error && <p className="text-rosetti-red">{error}</p>}

        {!loading && !error && (
          <div className="overflow-x-auto rounded-xl border border-black/10 bg-white shadow-sm">
            <table className="w-full min-w-[720px] text-left text-sm">
              <thead className="bg-black/5 text-xs uppercase tracking-wide text-rosetti-black/60">
                <tr>
                  <th className="px-4 py-3">Prato</th>
                  <th className="px-4 py-3">Categoria</th>
                  <th className="px-4 py-3">Preço</th>
                  <th className="px-4 py-3">Status</th>
                  <th className="px-4 py-3 text-right">Ações</th>
                </tr>
              </thead>
              <tbody>
                {items.map((item) => (
                  <tr key={item.id} className="border-t border-black/10">
                    <td className="px-4 py-3 font-serif italic">{item.name}</td>
                    <td className="px-4 py-3 capitalize">{item.categorySlug}</td>
                    <td className="px-4 py-3">{formatPrice(item.price)}</td>
                    <td className="px-4 py-3">
                      <div className="flex flex-wrap gap-1.5">
                        {item.isFeatured && (
                          <span className="rounded-full bg-rosetti-black px-2 py-0.5 text-xs text-white">
                            Destaque
                          </span>
                        )}
                        {item.isSoldOut && (
                          <span className="rounded-full bg-black/10 px-2 py-0.5 text-xs">
                            Esgotado
                          </span>
                        )}
                      </div>
                    </td>
                    <td className="px-4 py-3">
                      <div className="flex justify-end gap-2 whitespace-nowrap">
                        <button
                          type="button"
                          onClick={() => handleToggle(item, 'is_featured')}
                          className="rounded-full border border-black/15 px-3 py-1 text-xs hover:border-rosetti-red hover:text-rosetti-red"
                        >
                          {item.isFeatured ? 'Remover destaque' : 'Destacar'}
                        </button>
                        <button
                          type="button"
                          onClick={() => handleToggle(item, 'is_sold_out')}
                          className="rounded-full border border-black/15 px-3 py-1 text-xs hover:border-rosetti-red hover:text-rosetti-red"
                        >
                          {item.isSoldOut ? 'Reabrir' : 'Esgotar'}
                        </button>
                        <button
                          type="button"
                          onClick={() => {
                            setEditingItem(item);
                            setShowForm(true);
                            window.scrollTo({ top: 0, behavior: 'smooth' });
                          }}
                          className="rounded-full border border-black/15 px-3 py-1 text-xs hover:border-rosetti-red hover:text-rosetti-red"
                        >
                          Editar
                        </button>
                        <button
                          type="button"
                          onClick={() => handleDelete(item)}
                          className="rounded-full border border-rosetti-red/40 px-3 py-1 text-xs text-rosetti-red hover:bg-rosetti-red hover:text-white"
                        >
                          Remover
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </main>
    </div>
  );
}

export default function Admin() {
  const [authHeader, setAuthHeader] = useState(null);
  const [checking, setChecking] = useState(true);

  useEffect(() => {
    const stored = getStoredAuth();
    if (!stored) {
      setChecking(false);
      return;
    }
    verifyAdminAuth(stored)
      .then(() => setAuthHeader(stored))
      .catch(() => clearStoredAuth())
      .finally(() => setChecking(false));
  }, []);

  function handleLogout() {
    clearStoredAuth();
    setAuthHeader(null);
  }

  if (checking) {
    return <div className="flex min-h-screen items-center justify-center bg-marble">Carregando…</div>;
  }

  if (!authHeader) {
    return <LoginForm onAuthenticated={setAuthHeader} />;
  }

  return <AdminDashboard authHeader={authHeader} onLogout={handleLogout} />;
}
