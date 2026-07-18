import { Router } from 'express';
import db from '../db.js';
import { serializeItem as serialize } from '../serialize.js';

const router = Router();

router.get('/', (req, res) => {
  const { category, search, vegetarian, featured } = req.query;

  let query = `
    SELECT items.*, categories.slug AS category_slug
    FROM items
    JOIN categories ON categories.id = items.category_id
    WHERE 1 = 1
  `;
  const params = [];

  if (category) {
    query += ' AND categories.slug = ?';
    params.push(category);
  }

  if (search) {
    query += ' AND (items.name LIKE ? OR items.description LIKE ?)';
    params.push(`%${search}%`, `%${search}%`);
  }

  if (vegetarian === 'true') {
    query += ' AND items.is_vegetarian = 1';
  }

  if (featured === 'true') {
    query += ' AND items.is_featured = 1';
  }

  query += ' ORDER BY categories.sort_order ASC, items.sort_order ASC';

  const rows = db.prepare(query).all(...params);
  res.json(rows.map(serialize));
});

router.get('/:id', (req, res) => {
  const row = db
    .prepare(
      `SELECT items.*, categories.slug AS category_slug
       FROM items
       JOIN categories ON categories.id = items.category_id
       WHERE items.id = ?`
    )
    .get(req.params.id);

  if (!row) {
    return res.status(404).json({ error: 'Item não encontrado' });
  }

  res.json(serialize(row));
});

export default router;
