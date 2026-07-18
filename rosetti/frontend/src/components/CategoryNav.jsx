export default function CategoryNav({ categories, activeSlug, onSelect }) {
  return (
    <nav className="sticky top-0 z-20 border-b border-black/10 bg-rosetti-white/95 backdrop-blur">
      <div className="mx-auto flex max-w-5xl gap-2 overflow-x-auto px-4 py-3 sm:justify-center">
        {categories.map((category) => {
          const isActive = category.slug === activeSlug;
          return (
            <button
              key={category.slug}
              type="button"
              onClick={() => onSelect(category.slug)}
              className={`whitespace-nowrap rounded-full border px-4 py-1.5 font-serif text-sm font-semibold tracking-wide transition-colors ${
                isActive
                  ? 'border-rosetti-red bg-rosetti-red text-white'
                  : 'border-black/15 bg-transparent text-rosetti-black hover:border-rosetti-red hover:text-rosetti-red'
              }`}
            >
              {category.name}
            </button>
          );
        })}
      </div>
    </nav>
  );
}
