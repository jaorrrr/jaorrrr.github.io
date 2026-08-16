import { useEffect, useMemo, useState } from 'react';
import Header from '../components/Header.jsx';
import CategoryNav from '../components/CategoryNav.jsx';
import SearchBar from '../components/SearchBar.jsx';
import MenuItemCard from '../components/MenuItemCard.jsx';
import { fetchCategories, fetchItems } from '../dataClient.js';

export default function Menu() {
  const [categories, setCategories] = useState([]);
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [search, setSearch] = useState('');
  const [vegetarianOnly, setVegetarianOnly] = useState(false);
  const [activeSlug, setActiveSlug] = useState('');

  useEffect(() => {
    Promise.all([fetchCategories(), fetchItems()])
      .then(([categoriesData, itemsData]) => {
        setCategories(categoriesData);
        setItems(itemsData);
        setActiveSlug(categoriesData[0]?.slug || '');
      })
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  const filteredItems = useMemo(() => {
    const term = search.trim().toLowerCase();
    return items.filter((item) => {
      const matchesTerm =
        !term ||
        item.name.toLowerCase().includes(term) ||
        item.description.toLowerCase().includes(term);
      const matchesVegetarian = !vegetarianOnly || item.isVegetarian;
      return matchesTerm && matchesVegetarian;
    });
  }, [items, search, vegetarianOnly]);

  const itemsByCategory = useMemo(() => {
    const map = new Map();
    for (const category of categories) {
      map.set(
        category.slug,
        filteredItems.filter((item) => item.categorySlug === category.slug)
      );
    }
    return map;
  }, [categories, filteredItems]);

  function handleSelectCategory(slug) {
    setActiveSlug(slug);
    const section = document.getElementById(`categoria-${slug}`);
    if (section) {
      section.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  }

  const isFiltering = search.trim() !== '' || vegetarianOnly;

  return (
    <div className="min-h-screen bg-marble">
      <Header />
      {categories.length > 0 && (
        <CategoryNav categories={categories} activeSlug={activeSlug} onSelect={handleSelectCategory} />
      )}
      <SearchBar
        search={search}
        onSearchChange={setSearch}
        vegetarianOnly={vegetarianOnly}
        onVegetarianToggle={setVegetarianOnly}
      />

      <main className="mx-auto max-w-5xl px-4 pb-16">
        {loading && <p className="py-12 text-center text-rosetti-black/60">Carregando cardápio…</p>}
        {error && (
          <p className="py-12 text-center text-rosetti-red">
            Não foi possível carregar o cardápio: {error}
          </p>
        )}

        {!loading && !error && isFiltering && filteredItems.length === 0 && (
          <p className="py-12 text-center text-rosetti-black/60">
            Nenhum prato encontrado para essa busca.
          </p>
        )}

        {!loading &&
          !error &&
          categories.map((category) => {
            const categoryItems = itemsByCategory.get(category.slug) || [];
            if (isFiltering && categoryItems.length === 0) return null;

            return (
              <section key={category.slug} id={`categoria-${category.slug}`} className="scroll-mt-16 py-8">
                <div className="mb-4 flex items-baseline gap-3">
                  <h2 className="font-serif text-2xl font-semibold text-rosetti-black">
                    {category.name}
                  </h2>
                  <span className="text-sm uppercase tracking-wide text-rosetti-black/50">
                    {category.name_pt}
                  </span>
                </div>
                <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
                  {categoryItems.map((item) => (
                    <MenuItemCard key={item.id} item={item} />
                  ))}
                </div>
              </section>
            );
          })}
      </main>

      <footer className="border-t border-black/10 bg-rosetti-black py-6 text-center text-sm text-white/60">
        <p>Rosetti · Ristorante Italiano · Grazie mille e buon appetito!</p>
      </footer>
    </div>
  );
}
