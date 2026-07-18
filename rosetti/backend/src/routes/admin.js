import { Router } from 'express';
import db from '../db.js';
import { requireAdminAuth } from '../middleware/auth.js';
import { serializeItem } from '../serialize.js';

const router = Router();

router.use(requireAdminAuth);

router.get('/verify', (req, res) => {
  res.json({ ok: true });
});

router.get('/items', (req, res) => {
  const rows = db
    .prepare(
      `SELECT items.*, categories.slug AS category_slug
       FROM items
       JOIN categories ON categories.id = items.category_id
       ORDER BY categories.sort_order ASC, items.sort_order ASC`
    )
    .all();
  res.json(rows.map(serializeItem));
});

function validateItemPayload(body) {
  const errors = [];
  if (!body.name || typeof body.name !== 'string') errors.push('Nome é obrigatório');
  if (!body.categoryId) errors.push('Categoria é obrigatória');
  if (body.price === undefined || Number.isNaN(Number(body.price))) errors.push('Preço inválido');
  return errors;
}

router.post('/items', (req, res) => {
  const errors = validateItemPayload(req.body);
  if (errors.length) {
    return res.status(400).json({ error: errors.join(', ') });
  }

  const category = db.prepare('SELECT id FROM categories WHERE id = ?').get(req.body.categoryId);
  if (!category) {
    return res.status(400).json({ error: 'Categoria não encontrada' });
  }

  const maxSortOrder =
    db
      .prepare('SELECT MAX(sort_order) AS m FROM items WHERE category_id = ?')
      .get(req.body.categoryId).m || 0;

  const info = db
    .prepare(
      `INSERT INTO items (
        category_id, name, description, price, image_url,
        is_vegetarian, is_spicy, is_bestseller, is_featured, is_sold_out, sort_order
      ) VALUES (@categoryId, @name, @description, @price, @imageUrl,
        @isVegetarian, @isSpicy, @isBestseller, @isFeatured, @isSoldOut, @sortOrder)`
    )
    .run({
      categoryId: req.body.categoryId,
      name: req.body.name,
      description: req.body.description || '',
      price: Number(req.body.price),
      imageUrl: req.body.imageUrl || null,
      isVegetarian: req.body.isVegetarian ? 1 : 0,
      isSpicy: req.body.isSpicy ? 1 : 0,
      isBestseller: req.body.isBestseller ? 1 : 0,
      isFeatured: req.body.isFeatured ? 1 : 0,
      isSoldOut: req.body.isSoldOut ? 1 : 0,
      sortOrder: maxSortOrder + 1,
    });

  const row = db
    .prepare(
      `SELECT items.*, categories.slug AS category_slug
       FROM items JOIN categories ON categories.id = items.category_id
       WHERE items.id = ?`
    )
    .get(info.lastInsertRowid);

  res.status(201).json(serializeItem(row));
});

router.put('/items/:id', (req, res) => {
  const existing = db.prepare('SELECT * FROM items WHERE id = ?').get(req.params.id);
  if (!existing) {
    return res.status(404).json({ error: 'Item não encontrado' });
  }

  const errors = validateItemPayload(req.body);
  if (errors.length) {
    return res.status(400).json({ error: errors.join(', ') });
  }

  const category = db.prepare('SELECT id FROM categories WHERE id = ?').get(req.body.categoryId);
  if (!category) {
    return res.status(400).json({ error: 'Categoria não encontrada' });
  }

  db.prepare(
    `UPDATE items SET
      category_id = @categoryId,
      name = @name,
      description = @description,
      price = @price,
      image_url = @imageUrl,
      is_vegetarian = @isVegetarian,
      is_spicy = @isSpicy,
      is_bestseller = @isBestseller,
      is_featured = @isFeatured,
      is_sold_out = @isSoldOut,
      updated_at = datetime('now')
     WHERE id = @id`
  ).run({
    id: req.params.id,
    categoryId: req.body.categoryId,
    name: req.body.name,
    description: req.body.description || '',
    price: Number(req.body.price),
    imageUrl: req.body.imageUrl || null,
    isVegetarian: req.body.isVegetarian ? 1 : 0,
    isSpicy: req.body.isSpicy ? 1 : 0,
    isBestseller: req.body.isBestseller ? 1 : 0,
    isFeatured: req.body.isFeatured ? 1 : 0,
    isSoldOut: req.body.isSoldOut ? 1 : 0,
  });

  const row = db
    .prepare(
      `SELECT items.*, categories.slug AS category_slug
       FROM items JOIN categories ON categories.id = items.category_id
       WHERE items.id = ?`
    )
    .get(req.params.id);

  res.json(serializeItem(row));
});

router.patch('/items/:id/toggle', (req, res) => {
  const { field } = req.body;
  const allowedFields = ['is_sold_out', 'is_featured'];

  if (!allowedFields.includes(field)) {
    return res.status(400).json({ error: 'Campo inválido para alternar' });
  }

  const existing = db.prepare('SELECT * FROM items WHERE id = ?').get(req.params.id);
  if (!existing) {
    return res.status(404).json({ error: 'Item não encontrado' });
  }

  const newValue = existing[field] ? 0 : 1;
  db.prepare(`UPDATE items SET ${field} = ?, updated_at = datetime('now') WHERE id = ?`).run(
    newValue,
    req.params.id
  );

  const row = db
    .prepare(
      `SELECT items.*, categories.slug AS category_slug
       FROM items JOIN categories ON categories.id = items.category_id
       WHERE items.id = ?`
    )
    .get(req.params.id);

  res.json(serializeItem(row));
});

router.delete('/items/:id', (req, res) => {
  const existing = db.prepare('SELECT id FROM items WHERE id = ?').get(req.params.id);
  if (!existing) {
    return res.status(404).json({ error: 'Item não encontrado' });
  }

  db.prepare('DELETE FROM items WHERE id = ?').run(req.params.id);
  res.status(204).end();
});

export default router;
