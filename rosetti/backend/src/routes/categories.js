import { Router } from 'express';
import db from '../db.js';

const router = Router();

router.get('/', (req, res) => {
  const categories = db
    .prepare('SELECT id, slug, name, name_pt, sort_order FROM categories ORDER BY sort_order ASC')
    .all();
  res.json(categories);
});

export default router;
