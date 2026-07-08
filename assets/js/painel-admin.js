/**
 * Painel do avaliador — abas de Dashboard, Ranking Geral e assistente de
 * IA "Alpha". Lê os mesmos dados de STORAGE/CATEGORIAS usados pela lista
 * de candidatos (avaliador.js); aqui só agregamos e exibimos de outra forma.
 */
(function () {
  "use strict";

  const abasNav = document.getElementById("abas-painel");
  const gradeKpi = document.getElementById("grade-kpi");
  const barrasCategorias = document.getElementById("barras-categorias");
  const rankingLista = document.getElementById("ranking-lista");

  if (!abasNav) return;

  /* ---------------- navegação entre abas ---------------- */

  abasNav.querySelectorAll(".aba-botao").forEach((botao) => {
    botao.addEventListener("click", () => ativarAba(botao.dataset.aba));
  });

  function ativarAba(nome) {
    abasNav.querySelectorAll(".aba-botao").forEach((b) => {
      b.classList.toggle("ativa", b.dataset.aba === nome);
    });
    document.querySelectorAll(".aba-conteudo").forEach((secao) => {
      secao.hidden = secao.id !== "aba-" + nome;
    });
    if (nome === "dashboard") renderizarDashboard();
    if (nome === "ranking") renderizarRanking();
  }

  /* ---------------- dados agregados ---------------- */

  function todasAsCandidaturas() {
    try {
      return JSON.parse(localStorage.getItem(CONFIG.CHAVE_CANDIDATURAS)) || [];
    } catch {
      return [];
    }
  }

  function todasAsEntrevistas() {
    try {
      return JSON.parse(localStorage.getItem(CONFIG.CHAVE_ENTREVISTAS)) || [];
    } catch {
      return [];
    }
  }

  function estatisticas() {
    const candidaturas = todasAsCandidaturas();
    const aprovados = candidaturas.filter((c) => c.notaIa >= CONFIG.NOTA_CORTE);
    const elite = candidaturas.filter((c) => c.notaIa === 10);
    const entrevistas = todasAsEntrevistas();
    const vagas = Object.keys(window.CATEGORIAS || {}).length;
    const taxa = candidaturas.length
      ? Math.round((aprovados.length / candidaturas.length) * 100)
      : 0;
    return { candidaturas, aprovados, elite, entrevistas, vagas, taxa };
  }

  function porCategoria() {
    const candidaturas = todasAsCandidaturas();
    return Object.entries(window.CATEGORIAS || {}).map(([id, cat]) => {
      const aprovadosCat = candidaturas.filter(
        (c) => c.categoria === id && c.notaIa >= CONFIG.NOTA_CORTE
      );
      return { id, nome: cat.nome, total: aprovadosCat.length };
    });
  }

  /* ---------------- dashboard ---------------- */

  function renderizarDashboard() {
    const s = estatisticas();

    gradeKpi.innerHTML = [
      cartaoKpi("📥", "Candidaturas recebidas", s.candidaturas.length),
      cartaoKpi("✅", "Aprovados na triagem", s.aprovados.length, s.taxa + "% de aprovação"),
      cartaoKpi("⭐", "Perfis 10/10", s.elite.length, true),
      cartaoKpi("📅", "Entrevistas agendadas", s.entrevistas.length),
      cartaoKpi("💼", "Categorias de vaga abertas", s.vagas),
    ].join("");

    const categorias = porCategoria().sort((a, b) => b.total - a.total);
    const maior = Math.max(1, ...categorias.map((c) => c.total));
    barrasCategorias.innerHTML = categorias
      .map(
        (c) => `
      <div class="barra-categoria">
        <div class="barra-categoria__topo"><strong>${escapar(c.nome)}</strong><span>${c.total} aprovado(s)</span></div>
        <div class="barra-categoria__trilho">
          <div class="barra-categoria__preenchimento" style="width:${(c.total / maior) * 100}%"></div>
        </div>
      </div>`
      )
      .join("");
  }

  function cartaoKpi(icone, rotulo, valor, extraOuDestaque) {
    const destaque = extraOuDestaque === true;
    const subvalor = typeof extraOuDestaque === "string" ? extraOuDestaque : "";
    return `
      <div class="kpi-card${destaque ? " destaque" : ""}">
        <div class="rotulo">${icone} ${escapar(rotulo)}</div>
        <div class="valor">${valor}</div>
        ${subvalor ? `<div class="subvalor">${escapar(subvalor)}</div>` : ""}
      </div>`;
  }

  /* ---------------- ranking geral ---------------- */

  function rankingGeral(limite) {
    const candidaturas = todasAsCandidaturas().filter((c) => c.notaIa >= CONFIG.NOTA_CORTE);
    return candidaturas
      .sort((a, b) => b.notaIa - a.notaIa || a.criadoEm.localeCompare(b.criadoEm))
      .slice(0, limite || 10);
  }

  function renderizarRanking() {
    const lista = rankingGeral(10);
    if (!lista.length) {
      rankingLista.innerHTML = '<p class="vazio">Nenhum candidato aprovado até o momento.</p>';
      return;
    }
    rankingLista.innerHTML = lista
      .map((c, indice) => {
        const posicao = indice + 1;
        const classeTop = posicao <= 3 ? " top" + posicao : "";
        const medalha = posicao === 1 ? "🥇" : posicao === 2 ? "🥈" : posicao === 3 ? "🥉" : posicao;
        const categoria = window.CATEGORIAS[c.categoria];
        return `
        <div class="ranking-item${classeTop}">
          <div class="ranking-posicao">${medalha}</div>
          <div class="ranking-dados">
            <h3>${escapar(c.candidatoNome)}</h3>
            <p>${escapar(categoria ? categoria.nome : c.categoria)}</p>
          </div>
          <div class="ranking-nota">${c.notaIa}/10</div>
        </div>`;
      })
      .join("");
  }

  function escapar(texto) {
    const div = document.createElement("div");
    div.textContent = texto == null ? "" : String(texto);
    return div.innerHTML;
  }

  /* ---------------- Alpha (assistente de IA) ---------------- */

  const alphaMensagens = document.getElementById("alpha-mensagens");
  const alphaForm = document.getElementById("alpha-form");
  const alphaPergunta = document.getElementById("alpha-pergunta");
  const alphaSugestoes = document.getElementById("alpha-sugestoes");

  function alphaMensagem(texto, autor) {
    const div = document.createElement("div");
    div.className = "alpha-msg " + autor;
    div.textContent = texto;
    alphaMensagens.appendChild(div);
    alphaMensagens.scrollTop = alphaMensagens.scrollHeight;
  }

  function alphaResponder(pergunta) {
    const p = pergunta.toLowerCase();
    const s = estatisticas();

    if (p.includes("quantos") && p.includes("aprovad")) {
      return `Até agora, ${s.aprovados.length} de ${s.candidaturas.length} candidaturas foram aprovadas na triagem (nota ≥ ${CONFIG.NOTA_CORTE}) — uma taxa de aprovação de ${s.taxa}%.`;
    }

    if (p.includes("categoria") && (p.includes("mais") || p.includes("maior"))) {
      const categorias = porCategoria().sort((a, b) => b.total - a.total);
      const lider = categorias[0];
      return lider && lider.total
        ? `A categoria com mais aprovados é "${lider.nome}", com ${lider.total} candidato(s) aprovado(s).`
        : "Ainda não há aprovados suficientes para apontar uma categoria líder.";
    }

    if (p.includes("lidera") || (p.includes("ranking") && (p.includes("quem") || p.includes("top") || p.includes("primeiro")))) {
      const topo = rankingGeral(1)[0];
      return topo
        ? `${topo.candidatoNome} lidera o ranking geral com nota ${topo.notaIa}/10.`
        : "Ainda não há candidatos aprovados para formar o ranking.";
    }

    if (p.includes("entrevista")) {
      return `Existem ${s.entrevistas.length} entrevista(s) agendada(s) no momento.`;
    }

    if (p.includes("10/10") || p.includes("elite") || p.includes("nota 10") || p.includes("nota máxima")) {
      return `Temos ${s.elite.length} perfil(is) com nota 10/10 registrados no painel.`;
    }

    if (p.includes("vaga") && (p.includes("quantas") || p.includes("categoria"))) {
      return `Há ${s.vagas} categorias de vaga abertas no processo seletivo.`;
    }

    if (p.includes("oi") || p.includes("olá") || p.includes("ola") || p.includes("bom dia") || p.includes("boa tarde")) {
      return "Olá! Sou a Alpha, assistente de IA do painel. Posso responder sobre candidaturas, aprovações, ranking e entrevistas. O que você quer saber?";
    }

    return "Ainda estou aprendendo a responder isso. Tente perguntar sobre candidatos aprovados, a categoria com mais aprovações, o ranking geral ou as entrevistas agendadas.";
  }

  alphaForm.addEventListener("submit", (evento) => {
    evento.preventDefault();
    const texto = alphaPergunta.value.trim();
    if (!texto) return;
    alphaMensagem(texto, "usuario");
    alphaPergunta.value = "";
    setTimeout(() => alphaMensagem(alphaResponder(texto), "bot"), 350);
  });

  alphaSugestoes.querySelectorAll(".alpha-sugestao").forEach((botao) => {
    botao.addEventListener("click", () => {
      alphaMensagem(botao.textContent, "usuario");
      setTimeout(() => alphaMensagem(alphaResponder(botao.textContent), "bot"), 350);
    });
  });

  alphaMensagem(
    "Olá, eu sou a Alpha ✨ — assistente de IA do painel. Posso resumir candidaturas, apontar a categoria com mais aprovações ou dizer quem lidera o ranking geral. Use as sugestões abaixo ou digite sua pergunta.",
    "bot"
  );

  /* ---------------- inicialização ---------------- */

  renderizarDashboard();

  // mantém dashboard/ranking em dia conforme novas candidaturas chegam
  window.addEventListener("storage", atualizarAbaAtiva);
  setInterval(atualizarAbaAtiva, 4000);

  function atualizarAbaAtiva() {
    const ativa = abasNav.querySelector(".aba-botao.ativa");
    if (!ativa) return;
    if (ativa.dataset.aba === "dashboard") renderizarDashboard();
    if (ativa.dataset.aba === "ranking") renderizarRanking();
  }
})();
