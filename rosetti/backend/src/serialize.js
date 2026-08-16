export function serializeItem(row) {
  return {
    id: row.id,
    categoryId: row.category_id,
    categorySlug: row.category_slug,
    name: row.name,
    description: row.description,
    price: row.price,
    imageUrl: row.image_url,
    isVegetarian: !!row.is_vegetarian,
    isSpicy: !!row.is_spicy,
    isBestseller: !!row.is_bestseller,
    isFeatured: !!row.is_featured,
    isSoldOut: !!row.is_sold_out,
  };
}
