import db from './db.js';

const categories = [
  { slug: 'antipasti', name: 'Antipasti', name_pt: 'Entradas', sort_order: 1 },
  { slug: 'primi', name: 'Primi Piatti', name_pt: 'Massas e Risotos', sort_order: 2 },
  { slug: 'pizze', name: 'Pizze', name_pt: 'Pizzas', sort_order: 3 },
  { slug: 'secondi', name: 'Secondi', name_pt: 'Pratos principais', sort_order: 4 },
  { slug: 'dolci', name: 'Dolci', name_pt: 'Sobremesas', sort_order: 5 },
  { slug: 'bevande', name: 'Bevande', name_pt: 'Bebidas', sort_order: 6 },
];

const image = (categorySlug) => `/placeholders/${categorySlug}.svg`;

const items = {
  antipasti: [
    { name: 'Bruschetta al Pomodoro', description: 'Pão italiano tostado, tomate fresco, manjericão e azeite', price: 32, tags: { vegetarian: true, bestseller: true } },
    { name: 'Carpaccio di Manzo', description: 'Carpaccio de carne, rúcula, lascas de parmesão e molho de mostarda', price: 45, tags: {} },
    { name: 'Burrata con Prosciutto', description: 'Burrata cremosa, presunto de parma e tomate confit', price: 52, tags: { bestseller: true } },
    { name: 'Arancini al Tartufo', description: 'Bolinhos de risoto recheados com trufa', price: 38, tags: { vegetarian: true } },
  ],
  primi: [
    { name: 'Spaghetti al Pomodoro', description: 'Massa artesanal, molho de tomate fresco e manjericão', price: 48, tags: { vegetarian: true, bestseller: true } },
    { name: 'Fettuccine Alfredo', description: 'Massa fresca, molho branco cremoso e parmesão', price: 54, tags: { vegetarian: true } },
    { name: "Rigatoni all'Amatriciana", description: 'Guanciale, molho de tomate, pimenta e pecorino', price: 58, tags: { spicy: true } },
    { name: 'Risotto ai Funghi', description: 'Risoto cremoso com mix de cogumelos', price: 62, tags: { vegetarian: true } },
    { name: 'Lasagna alla Bolognese', description: 'Camadas de massa, ragu bolonhesa e bechamel', price: 56, tags: { bestseller: true } },
  ],
  pizze: [
    { name: 'Margherita', description: 'Molho de tomate, mozzarella de búfala e manjericão', price: 49, tags: { vegetarian: true, bestseller: true } },
    { name: 'Marinara', description: 'Molho de tomate, alho e orégano', price: 42, tags: { vegetarian: true } },
    { name: 'Quattro Formaggi', description: 'Mozzarella, gorgonzola, parmesão e provolone', price: 58, tags: { vegetarian: true } },
    { name: 'Diavola', description: 'Mozzarella, salame picante e pimenta calabresa', price: 55, tags: { spicy: true } },
    { name: 'Prosciutto e Funghi', description: 'Presunto, cogumelos e mozzarella', price: 57, tags: {} },
  ],
  secondi: [
    { name: 'Osso Buco alla Milanese', description: 'Músculo de vitela cozido lentamente com risoto de açafrão', price: 89, tags: { featured: true } },
    { name: 'Pollo alla Parmigiana', description: 'Filé de frango empanado, molho de tomate e queijo gratinado', price: 62, tags: { bestseller: true } },
    { name: 'Branzino al Forno', description: 'Robalo assado com ervas e legumes', price: 78, tags: {} },
  ],
  dolci: [
    { name: 'Tiramisù', description: 'Clássico doce italiano com café e mascarpone', price: 28, tags: { vegetarian: true, bestseller: true } },
    { name: 'Panna Cotta', description: 'Creme italiano com calda de frutas vermelhas', price: 24, tags: { vegetarian: true } },
    { name: 'Cannoli Siciliani', description: 'Massa crocante recheada com ricota doce', price: 26, tags: { vegetarian: true } },
  ],
  bevande: [
    { name: 'Acqua Minerale', description: 'Água mineral', price: 8, tags: { vegetarian: true } },
    { name: 'Bibita', description: 'Refrigerante', price: 9, tags: { vegetarian: true } },
    { name: 'Vino della Casa (calice)', description: 'Vinho da casa (taça)', price: 32, tags: { vegetarian: true } },
    { name: 'Espresso', description: 'Espresso', price: 10, tags: { vegetarian: true, bestseller: true } },
  ],
};

function seed() {
  const resetTables = db.transaction(() => {
    db.prepare('DELETE FROM items').run();
    db.prepare('DELETE FROM categories').run();
    db.prepare("DELETE FROM sqlite_sequence WHERE name IN ('items', 'categories')").run();
  });
  resetTables();

  const insertCategory = db.prepare(
    'INSERT INTO categories (slug, name, name_pt, sort_order) VALUES (@slug, @name, @name_pt, @sort_order)'
  );
  const insertItem = db.prepare(`
    INSERT INTO items (
      category_id, name, description, price, image_url,
      is_vegetarian, is_spicy, is_bestseller, is_featured, is_sold_out, sort_order
    ) VALUES (
      @category_id, @name, @description, @price, @image_url,
      @is_vegetarian, @is_spicy, @is_bestseller, @is_featured, 0, @sort_order
    )
  `);

  const seedAll = db.transaction(() => {
    for (const category of categories) {
      const info = insertCategory.run(category);
      const categoryId = info.lastInsertRowid;
      const categoryItems = items[category.slug] || [];
      categoryItems.forEach((item, index) => {
        insertItem.run({
          category_id: categoryId,
          name: item.name,
          description: item.description,
          price: item.price,
          image_url: image(category.slug),
          is_vegetarian: item.tags.vegetarian ? 1 : 0,
          is_spicy: item.tags.spicy ? 1 : 0,
          is_bestseller: item.tags.bestseller ? 1 : 0,
          is_featured: item.tags.featured ? 1 : 0,
          sort_order: index + 1,
        });
      });
    }
  });
  seedAll();

  const totalCategories = db.prepare('SELECT COUNT(*) AS c FROM categories').get().c;
  const totalItems = db.prepare('SELECT COUNT(*) AS c FROM items').get().c;
  console.log(`Seed concluído: ${totalCategories} categorias, ${totalItems} itens.`);
}

seed();
