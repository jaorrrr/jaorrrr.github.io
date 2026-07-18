const badgeStyles = {
  vegetarian: 'bg-rosetti-green/10 text-rosetti-green border-rosetti-green/30',
  spicy: 'bg-rosetti-red/10 text-rosetti-red border-rosetti-red/30',
  bestseller: 'bg-amber-100 text-amber-800 border-amber-300',
  featured: 'bg-rosetti-black text-white border-rosetti-black',
};

function formatPrice(price) {
  return price.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
}

export default function MenuItemCard({ item }) {
  const badges = [];
  if (item.isFeatured) badges.push({ key: 'featured', label: '★ Destaque do dia' });
  if (item.isBestseller) badges.push({ key: 'bestseller', label: 'Mais pedido' });
  if (item.isVegetarian) badges.push({ key: 'vegetarian', label: 'Vegetariano' });
  if (item.isSpicy) badges.push({ key: 'spicy', label: 'Picante 🌶' });

  return (
    <article
      className={`flex gap-4 rounded-xl border border-black/10 bg-white p-3 shadow-sm transition hover:shadow-md sm:p-4 ${
        item.isSoldOut ? 'opacity-60' : ''
      }`}
    >
      <img
        src={item.imageUrl}
        alt={item.name}
        loading="lazy"
        className="h-24 w-24 flex-shrink-0 rounded-lg object-cover sm:h-28 sm:w-28"
      />
      <div className="flex flex-1 flex-col">
        <div className="flex items-start justify-between gap-2">
          <h3 className="font-serif text-lg font-semibold italic text-rosetti-black">
            {item.name}
          </h3>
          <span className="whitespace-nowrap font-serif text-lg font-semibold text-rosetti-red">
            {formatPrice(item.price)}
          </span>
        </div>
        <p className="mt-1 text-sm text-rosetti-black/70">{item.description}</p>
        <div className="mt-auto flex flex-wrap gap-1.5 pt-2">
          {item.isSoldOut && (
            <span className="rounded-full border border-black/20 bg-black/5 px-2 py-0.5 text-xs font-semibold text-rosetti-black/70">
              Esgotado
            </span>
          )}
          {badges.map((badge) => (
            <span
              key={badge.key}
              className={`rounded-full border px-2 py-0.5 text-xs font-semibold ${badgeStyles[badge.key]}`}
            >
              {badge.label}
            </span>
          ))}
        </div>
      </div>
    </article>
  );
}
