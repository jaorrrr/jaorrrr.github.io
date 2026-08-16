import { useEffect, useState } from 'react';

const emptyForm = {
  categoryId: '',
  name: '',
  description: '',
  price: '',
  imageUrl: '',
  isVegetarian: false,
  isSpicy: false,
  isBestseller: false,
  isFeatured: false,
  isSoldOut: false,
};

export default function ItemForm({ categories, initialItem, onSubmit, onCancel }) {
  const [form, setForm] = useState(emptyForm);

  useEffect(() => {
    if (initialItem) {
      setForm({
        categoryId: initialItem.categoryId,
        name: initialItem.name,
        description: initialItem.description,
        price: initialItem.price,
        imageUrl: initialItem.imageUrl || '',
        isVegetarian: initialItem.isVegetarian,
        isSpicy: initialItem.isSpicy,
        isBestseller: initialItem.isBestseller,
        isFeatured: initialItem.isFeatured,
        isSoldOut: initialItem.isSoldOut,
      });
    } else {
      setForm({ ...emptyForm, categoryId: categories[0]?.id || '' });
    }
  }, [initialItem, categories]);

  function updateField(field, value) {
    setForm((prev) => ({ ...prev, [field]: value }));
  }

  function handleSubmit(event) {
    event.preventDefault();
    onSubmit({ ...form, categoryId: Number(form.categoryId), price: Number(form.price) });
  }

  const checkboxes = [
    { field: 'isVegetarian', label: 'Vegetariano' },
    { field: 'isSpicy', label: 'Picante' },
    { field: 'isBestseller', label: 'Mais pedido' },
    { field: 'isFeatured', label: 'Destaque do dia' },
    { field: 'isSoldOut', label: 'Esgotado' },
  ];

  return (
    <form
      onSubmit={handleSubmit}
      className="space-y-4 rounded-xl border border-black/10 bg-white p-5 shadow-sm"
    >
      <h3 className="font-serif text-lg font-semibold">
        {initialItem ? 'Editar prato' : 'Novo prato'}
      </h3>

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
        <label className="text-sm font-medium">
          Nome (italiano)
          <input
            required
            value={form.name}
            onChange={(e) => updateField('name', e.target.value)}
            className="mt-1 w-full rounded-md border border-black/20 px-3 py-2 text-sm outline-none focus:border-rosetti-red focus:ring-1 focus:ring-rosetti-red"
          />
        </label>

        <label className="text-sm font-medium">
          Categoria
          <select
            required
            value={form.categoryId}
            onChange={(e) => updateField('categoryId', e.target.value)}
            className="mt-1 w-full rounded-md border border-black/20 px-3 py-2 text-sm outline-none focus:border-rosetti-red focus:ring-1 focus:ring-rosetti-red"
          >
            {categories.map((category) => (
              <option key={category.id} value={category.id}>
                {category.name}
              </option>
            ))}
          </select>
        </label>

        <label className="text-sm font-medium sm:col-span-2">
          Descrição (português)
          <textarea
            value={form.description}
            onChange={(e) => updateField('description', e.target.value)}
            rows={2}
            className="mt-1 w-full rounded-md border border-black/20 px-3 py-2 text-sm outline-none focus:border-rosetti-red focus:ring-1 focus:ring-rosetti-red"
          />
        </label>

        <label className="text-sm font-medium">
          Preço (R$)
          <input
            required
            type="number"
            step="0.01"
            min="0"
            value={form.price}
            onChange={(e) => updateField('price', e.target.value)}
            className="mt-1 w-full rounded-md border border-black/20 px-3 py-2 text-sm outline-none focus:border-rosetti-red focus:ring-1 focus:ring-rosetti-red"
          />
        </label>

        <label className="text-sm font-medium">
          URL da imagem
          <input
            value={form.imageUrl}
            onChange={(e) => updateField('imageUrl', e.target.value)}
            placeholder="https://…"
            className="mt-1 w-full rounded-md border border-black/20 px-3 py-2 text-sm outline-none focus:border-rosetti-red focus:ring-1 focus:ring-rosetti-red"
          />
        </label>
      </div>

      <div className="flex flex-wrap gap-4 pt-1">
        {checkboxes.map(({ field, label }) => (
          <label key={field} className="flex select-none items-center gap-2 text-sm">
            <input
              type="checkbox"
              checked={form[field]}
              onChange={(e) => updateField(field, e.target.checked)}
              className="h-4 w-4 rounded border-black/30 text-rosetti-red focus:ring-rosetti-red"
            />
            {label}
          </label>
        ))}
      </div>

      <div className="flex justify-end gap-3 pt-2">
        <button
          type="button"
          onClick={onCancel}
          className="rounded-full border border-black/20 px-5 py-2 text-sm font-semibold text-rosetti-black/70 hover:border-black/40"
        >
          Cancelar
        </button>
        <button
          type="submit"
          className="rounded-full bg-rosetti-red px-5 py-2 text-sm font-semibold text-white hover:bg-rosetti-redDark"
        >
          Salvar
        </button>
      </div>
    </form>
  );
}
