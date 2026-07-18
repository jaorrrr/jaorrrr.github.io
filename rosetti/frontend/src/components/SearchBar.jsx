export default function SearchBar({ search, onSearchChange, vegetarianOnly, onVegetarianToggle }) {
  return (
    <div className="mx-auto flex max-w-5xl flex-col gap-3 px-4 py-4 sm:flex-row sm:items-center sm:justify-between">
      <div className="relative flex-1">
        <input
          type="search"
          value={search}
          onChange={(event) => onSearchChange(event.target.value)}
          placeholder="Buscar prato por nome ou descrição…"
          className="w-full rounded-full border border-black/15 bg-white px-5 py-2.5 text-sm shadow-sm outline-none transition focus:border-rosetti-red focus:ring-1 focus:ring-rosetti-red"
        />
      </div>
      <label className="flex select-none items-center gap-2 text-sm font-medium text-rosetti-black">
        <input
          type="checkbox"
          checked={vegetarianOnly}
          onChange={(event) => onVegetarianToggle(event.target.checked)}
          className="h-4 w-4 rounded border-black/30 text-rosetti-red focus:ring-rosetti-red"
        />
        Somente vegetariano 🌿
      </label>
    </div>
  );
}
