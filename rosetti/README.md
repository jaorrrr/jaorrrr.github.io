# Rosetti — Cardápio Digital

> **Aviso:** este é um projeto conceitual/portfólio de um cardápio digital para um
> restaurante italiano fictício chamado "Rosetti", sem vínculo com qualquer
> estabelecimento real.

Aplicação full-stack com cardápio digital (pensado para acesso via QR code no
celular) e um painel administrativo para gerenciar pratos e preços sem mexer
em código.

## Demo publicada (versão estática)

Uma versão sem backend real, com os mesmos dados iniciais e o mesmo painel
administrativo (mas salvando as edições no `localStorage` do navegador em vez
de num servidor), está publicada em:

**https://jaorrrr.github.io/cardapio-rosetti/**

Essa versão existe porque o GitHub Pages só serve arquivos estáticos — não dá
para rodar o backend Express ali. Ela é gerada a partir deste mesmo código
(`npm run build:static`, ver seção abaixo) e vive na pasta `/cardapio-rosetti`
na raiz do repositório. Para a experiência completa, com banco de dados e
API de verdade, rode o projeto localmente (próxima seção).

## Identidade visual

- **Cores:** branco (`#FAFAFA`), vermelho italiano (`#C8102E`) e preto (`#1A1A1A`),
  com uma linha tricolore (verde/branco/vermelho) como acento.
- **Tipografia:** Playfair Display (títulos) + Inter (corpo do texto).
- **Placeholders de prato:** ilustrações SVG locais por categoria (folha de
  manjericão/azeitona, pizza, taça de vinho etc.), sem depender de serviços
  externos de imagem.

## Stack

- **Backend:** Node.js + Express + SQLite (`better-sqlite3`)
- **Frontend:** React + Vite + Tailwind CSS + React Router

## Estrutura de pastas

```
rosetti/
├── backend/
│   ├── src/
│   │   ├── db.js              conexão e schema do SQLite
│   │   ├── seed.js            popula categorias e pratos iniciais
│   │   ├── server.js          servidor Express
│   │   ├── serialize.js       serialização de itens para JSON
│   │   ├── middleware/auth.js autenticação HTTP Basic do admin
│   │   └── routes/
│   │       ├── categories.js  GET /api/categories
│   │       ├── items.js       GET /api/items (busca e filtros)
│   │       └── admin.js       CRUD protegido /api/admin/*
│   └── data/rosetti.db        banco SQLite (gerado pelo seed)
└── frontend/
    ├── public/placeholders/   ilustrações SVG por categoria
    └── src/
        ├── api.js             cliente HTTP da API real (usado em `npm run dev`)
        ├── localApi.js        mesma interface, mas em localStorage (build estático)
        ├── localData.js       seed embutido, espelha backend/src/seed.js
        ├── dataClient.js       escolhe api.js ou localApi.js conforme o modo do build
        ├── authStorage.js     helpers de sessão (usados pelos dois modos)
        ├── components/        Header, CategoryNav, SearchBar, MenuItemCard, ItemForm…
        └── pages/
            ├── Menu.jsx        página principal do cardápio
            └── Admin.jsx       login + painel administrativo
```

## Como rodar localmente

Requer Node.js 18+.

### 1. Backend (porta 4000)

```bash
cd rosetti/backend
npm install
npm run seed   # cria/recria o banco SQLite com as categorias e pratos iniciais
npm run dev    # inicia a API em http://localhost:4000
```

Variáveis de ambiente opcionais (crie um `.env` a partir de `.env.example`):

```
PORT=4000
ADMIN_USER=admin
ADMIN_PASSWORD=rosetti123
```

### 2. Frontend (porta 5173)

Em outro terminal:

```bash
cd rosetti/frontend
npm install
npm run dev    # inicia o site em http://localhost:5173
```

O Vite já está configurado para fazer proxy de `/api` para `http://localhost:4000`,
então basta abrir **http://localhost:5173** com o backend rodando.

### 3. Acessar

- **Cardápio:** http://localhost:5173/
- **Painel administrativo:** http://localhost:5173/admin
  - Usuário: `admin`
  - Senha: `rosetti123` (ou o valor de `ADMIN_PASSWORD` definido no backend)

## Versão estática (a que está publicada no GitHub Pages)

O frontend roda em dois modos, escolhidos por uma variável de build
(`VITE_DATA_MODE`):

- **`npm run dev` / `npm run build`** — modo normal, fala com a API real
  (`src/api.js`) via `/api/*`.
- **`npm run build:static`** — usa `src/localApi.js` em vez da API: os dados
  iniciais vêm de `src/localData.js` (mesmo seed do backend) e qualquer
  criação/edição/remoção feita no `/admin` é salva no `localStorage` do
  próprio navegador. Também troca o roteador para `HashRouter` (URLs com
  `#/admin`), necessário porque o GitHub Pages não tem como redirecionar
  `/admin` de volta ao `index.html`.

Para gerar e publicar essa versão:

```bash
cd rosetti/frontend
npm run build:static
# copie o conteúdo de dist/ para a pasta cardapio-rosetti/ na raiz do repositório
```

**Limitações da versão estática** (inerentes a qualquer site sem backend):
o login do admin compara um hash SHA-256 da senha embutido no bundle — isso
ofusca a senha (`admin` / `rosetti123` por padrão), mas **não é segurança
real**, já que o hash é público em qualquer build JS. Da mesma forma, os
dados ficam só no navegador de quem edita, sem sincronizar entre visitantes.
Para uso em produção de verdade, use o backend Express (seção anterior).

## API

| Método | Rota | Descrição |
|---|---|---|
| GET | `/api/categories` | Lista as categorias do cardápio |
| GET | `/api/items` | Lista pratos (filtros via query string: `category`, `search`, `vegetarian=true`, `featured=true`) |
| GET | `/api/items/:id` | Detalhe de um prato |
| GET | `/api/admin/items` | Lista todos os pratos, incluindo esgotados (autenticado) |
| POST | `/api/admin/items` | Cria um prato (autenticado) |
| PUT | `/api/admin/items/:id` | Edita um prato (autenticado) |
| PATCH | `/api/admin/items/:id/toggle` | Alterna `is_sold_out` ou `is_featured` (autenticado) |
| DELETE | `/api/admin/items/:id` | Remove um prato (autenticado) |

As rotas `/api/admin/*` exigem HTTP Basic Auth (`ADMIN_USER` / `ADMIN_PASSWORD`).

## Banco de dados

SQLite via `better-sqlite3`, com duas tabelas: `categories` e `items`
(chave estrangeira `items.category_id → categories.id`). Para produção, a
mesma estrutura pode ser portada para PostgreSQL trocando apenas a camada de
acesso a dados (`db.js`) — as queries usadas são SQL padrão.

Rodar `npm run seed` novamente a qualquer momento recria o banco do zero com
os dados iniciais (Antipasti, Primi Piatti, Pizze, Secondi, Dolci e Bevande).
