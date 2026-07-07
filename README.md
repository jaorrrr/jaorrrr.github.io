# ✈️ Azul Talentos — Portal de Recrutamento com Triagem Automática (conceito)

> **Aviso legal:** este é um projeto conceitual desenvolvido para fins de
> estudo/portfólio, inspirado na identidade visual da Azul Linhas Aéreas
> Brasileiras S.A., **sem vínculo oficial com a empresa**. O aviso aparece no
> rodapé de todas as páginas e no corpo dos e-mails gerados pelo sistema.

Portal de recrutamento em português do Brasil com triagem automática de
currículos: o candidato se cadastra, envia o currículo em PDF, o texto é
extraído e avaliado por uma régua de critérios por categoria (nota 0–10), e o
avaliador autorizado vê apenas os perfis aprovados (nota ≥ 7), com resumo do
perfil, acesso ao PDF e agendamento de entrevista com e-mail padrão.

## Páginas

| Rota | Conteúdo |
|---|---|
| `/` | Landing page animada (gradiente azul-marinho, glassmorphism, aviões e linhas de rota), botões **Entrar** / **Inscrever-se** (ambos levam a `/vagas/`) e botão **Acesso Restrito** |
| `/vagas/` | **Nossos Cargos** — seis categorias com tooltip listando os cargos específicos |
| `/candidatura/?categoria=…` | Fluxo de candidatura: cadastro simplificado (com consentimento LGPD) → upload **somente PDF** → triagem → redirecionamento |
| `/obrigado/` | Página final "Boa sorte!" — igual para todos; **a nota nunca é exibida ao candidato** |
| `/acesso-restrito/` | Painel do avaliador: login por e-mail, seleção de categoria, seções **Perfis 10/10** e **Perfis 7/10+**, currículo em PDF, resumo da triagem e **Agendar Entrevista** |
| `/sobre-nos/` | Cultura da empresa, critérios de seleção e benefícios |

## Arquitetura desta versão (GitHub Pages = hospedagem estática)

O GitHub Pages não executa código de servidor. Esta versão implementa o
sistema completo **no navegador**, mantendo a mesma interface entre as
camadas para que a troca por um backend real seja um "transplante" simples:

| Requisito da especificação | Nesta demonstração | Em produção (backend real) |
|---|---|---|
| Banco de dados (candidatos, candidaturas, entrevistas) | `localStorage` + IndexedDB (PDFs) — os dados **nunca saem do navegador do visitante** | PostgreSQL (modelo abaixo) |
| Extração de texto do PDF | [pdf.js](https://mozilla.github.io/pdf.js/) no cliente (`assets/vendor/`) | Biblioteca no servidor (ex.: `pdf-parse`) ou envio do PDF direto à API da Anthropic (suporte nativo a documentos) |
| Motor de avaliação por IA | `assets/js/motor.js` — avaliador **determinístico** que aplica a mesma régua da seção 3 do briefing (não é possível guardar uma chave de API com segurança em site estático) | Chamada à API da Anthropic (exemplo abaixo) retornando `{nota, justificativa, resumo}` |
| Validação do e-mail do avaliador **no backend** | Hash SHA-256 do e-mail comparado no cliente (`config.js`) — o endereço não fica em texto claro, mas isso é **ofuscação, não segurança** | Autenticação real no servidor; e-mail autorizado em variável de ambiente |
| Envio automático do e-mail de entrevista | Gera o e-mail padrão (com o aviso legal no rodapé) e abre o cliente de e-mail do avaliador via `mailto:` | Serviço transacional (SES, SendGrid, Resend…) disparado pelo backend |
| Lista do avaliador atualizada dinamicamente | Evento `storage` entre abas + verificação periódica | WebSocket/SSE ou polling da API |

As regras de negócio essenciais estão todas implementadas: cadastro aberto,
upload restrito a PDF (extensão + MIME + assinatura `%PDF`), nota invisível
para o candidato, corte em nota ≥ 7, perfis 10/10 no topo com badge de
prioridade e demais aprovados em ordem decrescente.

## Motor de avaliação

`assets/js/data.js` codifica a régua da seção 3 em três faixas por categoria:

- **base** — requisitos da "Nota 7";
- **medio** — diferenciais da faixa "acima de 7, abaixo de 10";
- **elite** — requisitos da "Nota 10".

`assets/js/motor.js` pontua assim:

1. menos de 50% dos requisitos **base** → nota 0–6 (reprovado na triagem);
2. 50%+ dos requisitos base → nota parte de **7** e sobe com os diferenciais
   (`medio`/`elite`), até **9**;
3. 80%+ dos critérios **elite** (com 75%+ dos base) → **10**.

A saída é idêntica à esperada do modelo de IA: `{ nota, justificativa, resumo }`
— a justificativa é interna e o resumo executivo aparece só para o avaliador.

### Trocando pelo motor de IA real (API da Anthropic)

No backend, substitua a chamada a `MOTOR.avaliarCurriculo` por algo como:

```python
import anthropic

client = anthropic.Anthropic()  # ANTHROPIC_API_KEY via variável de ambiente

def avaliar_curriculo(texto_pdf: str, regua_da_categoria: str) -> dict:
    response = client.messages.parse(
        model="claude-opus-4-8",
        max_tokens=2048,
        system=(
            "Você é um avaliador de currículos de uma companhia aérea. "
            "Aplique estritamente a régua de avaliação fornecida e retorne "
            "nota (0-10), justificativa curta (uso interno) e um resumo "
            "executivo do perfil para o recrutador.\n\n" + regua_da_categoria
        ),
        messages=[{"role": "user", "content": texto_pdf}],
        output_format=AvaliacaoCurriculo,  # Pydantic: nota, justificativa, resumo
    )
    return response.parsed_output
```

A régua completa de cada categoria (o texto da seção 3 do briefing) entra no
`system` prompt; o restante do site não muda.

## Modelo de dados (produção)

```
candidatos    (id, nome, email, telefone, criado_em)
candidaturas  (id, candidato_id, categoria, arquivo_pdf_url,
               nota_ia, justificativa_ia, resumo_ia, status, criado_em)
entrevistas   (id, candidatura_id, data_hora, email_enviado, criado_em)
```

O e-mail do avaliador autorizado deve ficar em variável de ambiente
(`AVALIADOR_EMAIL`) e ser validado em todas as rotas do painel.

## Rodando localmente

```bash
python3 -m http.server 8000
# abra http://localhost:8000
```

(Os caminhos são absolutos a partir da raiz — sirva o site a partir da raiz
do repositório, como o GitHub Pages faz em `usuario.github.io`.)

## Estrutura

```
index.html                  landing page
vagas/                      nossos cargos (6 categorias + tooltips)
candidatura/                fluxo de candidatura
obrigado/                   página final
acesso-restrito/            painel do avaliador
sobre-nos/                  sobre nós
assets/css/styles.css       identidade visual (glassmorphism)
assets/js/config.js         configuração (hash do avaliador, chaves, aviso legal)
assets/js/data.js           categorias + régua de avaliação
assets/js/motor.js          motor de triagem (simulação determinística da IA)
assets/js/storage.js        persistência local (localStorage + IndexedDB)
assets/js/candidatura.js    fluxo do candidato
assets/js/avaliador.js      painel do avaliador
assets/js/ui.js             cabeçalho, rodapé e cenário animado
assets/vendor/pdf*.js       pdf.js 3.11.174 (extração de texto de PDF)
```
