import 'dotenv/config';
import express from 'express';
import cors from 'cors';
import categoriesRouter from './routes/categories.js';
import itemsRouter from './routes/items.js';
import adminRouter from './routes/admin.js';

const app = express();
const PORT = process.env.PORT || 4000;

app.use(cors());
app.use(express.json());

app.get('/api/health', (req, res) => {
  res.json({ status: 'ok', service: 'rosetti-backend' });
});

app.use('/api/categories', categoriesRouter);
app.use('/api/items', itemsRouter);
app.use('/api/admin', adminRouter);

app.use((req, res) => {
  res.status(404).json({ error: 'Rota não encontrada' });
});

app.listen(PORT, () => {
  console.log(`Rosetti backend rodando em http://localhost:${PORT}`);
});
