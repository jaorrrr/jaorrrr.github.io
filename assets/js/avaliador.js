/**
 * Painel do avaliador (Acesso Restrito).
 *
 * - Login apenas por e-mail; somente o endereço autorizado (comparado por
 *   hash SHA-256 — ver observação de segurança em config.js) acessa o painel.
 * - Lista de aprovados (nota >= 7) por categoria, em duas seções:
 *     1. Perfis 10/10 (prioridade)
 *     2. Perfis 7/10 ou mais (ordem decrescente de nota)
 *   Atualizada dinamicamente (evento "storage" entre abas + verificação
 *   periódica).
 * - Ações por candidato: baixar/visualizar o PDF, ler o resumo gerado na
 *   triagem e agendar entrevista (gera o e-mail padrão e abre o cliente de
 *   e-mail do avaliador — hospedagem estática não envia e-mail sozinha).
 */
(function () {
  "use strict";

  const telaLogin = document.getElementById("tela-login");
  const telaPainel = document.getElementById("tela-painel");
  const formLogin = document.getElementById("form-login");
  const erroLogin = document.getElementById("erro-login");
  const seletorCategoria = document.getElementById("seletor-categoria");
  const conteudoLista = document.getElementById("conteudo-lista");
  const botaoSair = document.getElementById("botao-sair");

  const modal = document.getElementById("modal-entrevista");
  const modalCandidato = document.getElementById("modal-candidato");
  const campoData = document.getElementById("data-entrevista");
  const campoHora = document.getElementById("hora-entrevista");
  const erroEntrevista = document.getElementById("erro-entrevista");
  const previaEmail = document.getElementById("previa-email");
  const botaoConfirmar = document.getElementById("botao-confirmar-entrevista");
  const botaoCancelarModal = document.getElementById("botao-cancelar-modal");

  let candidaturaSelecionada = null;
  let intervaloAtualizacao = null;

  /* ---------------- autenticação ---------------- */

  async function autorizado(email) {
    const hash = await STORAGE.sha256Hex(email.trim().toLowerCase());
    return hash === CONFIG.HASH_EMAIL_AVALIADOR;
  }

  formLogin.addEventListener("submit", async (evento) => {
    evento.preventDefault();
    erroLogin.hidden = true;
    const email = document.getElementById("email-avaliador").value;
    if (await autorizado(email)) {
      sessionStorage.setItem(CONFIG.CHAVE_SESSAO_AVALIADOR, "1");
      abrirPainel();
    } else {
      erroLogin.textContent =
        "E-mail não autorizado. O acesso a este painel é restrito à equipe de Recrutamento e Seleção.";
      erroLogin.hidden = false;
    }
  });

  botaoSair.addEventListener("click", () => {
    sessionStorage.removeItem(CONFIG.CHAVE_SESSAO_AVALIADOR);
    window.location.reload();
  });

  function abrirPainel() {
    telaLogin.hidden = true;
    telaPainel.hidden = false;
    if (!seletorCategoria.options.length || seletorCategoria.options.length === 1) {
      for (const [id, cat] of Object.entries(window.CATEGORIAS)) {
        const opcao = document.createElement("option");
        opcao.value = id;
        opcao.textContent = cat.nome + " — " + cat.cargos;
        seletorCategoria.appendChild(opcao);
      }
    }
    // Atualização dinâmica: outras abas disparam "storage"; nesta aba,
    // uma verificação periódica cobre chegadas novas.
    window.addEventListener("storage", renderizarLista);
    clearInterval(intervaloAtualizacao);
    intervaloAtualizacao = setInterval(renderizarLista, 4000);
  }

  seletorCategoria.addEventListener("change", renderizarLista);

  if (sessionStorage.getItem(CONFIG.CHAVE_SESSAO_AVALIADOR) === "1") {
    abrirPainel();
  }

  /* ---------------- listagem ---------------- */

  function escapar(texto) {
    const div = document.createElement("div");
    div.textContent = texto == null ? "" : String(texto);
    return div.innerHTML;
  }

  function renderizarLista() {
    const categoriaId = seletorCategoria.value;
    if (!categoriaId) {
      conteudoLista.innerHTML =
        '<p class="vazio">Selecione uma categoria para ver os candidatos aprovados.</p>';
      return;
    }

    const aprovados = STORAGE.listarAprovados(categoriaId);
    const elite = aprovados.filter((c) => c.notaIa === 10);
    const demais = aprovados.filter((c) => c.notaIa < 10);

    if (!aprovados.length) {
      conteudoLista.innerHTML =
        '<p class="vazio">Nenhum candidato aprovado na triagem para esta categoria até o momento.<br/>Novas candidaturas aparecem aqui automaticamente.</p>';
      return;
    }

    let html = "";
    html += '<div class="secao-notas"><h2><span class="badge badge--ouro">★ Prioridade</span> Perfis 10/10</h2>';
    html += elite.length
      ? elite.map((c) => cartaoCandidato(c, true)).join("")
      : '<p class="vazio" style="padding: 18px;">Nenhum perfil 10/10 nesta categoria por enquanto.</p>';
    html += "</div>";

    html += '<div class="secao-notas"><h2><span class="badge badge--verde">Aprovados</span> Perfis 7/10 ou mais</h2>';
    html += demais.length
      ? demais.map((c) => cartaoCandidato(c, false)).join("")
      : '<p class="vazio" style="padding: 18px;">Nenhum candidato nesta faixa por enquanto.</p>';
    html += "</div>";

    conteudoLista.innerHTML = html;

    conteudoLista.querySelectorAll("[data-acao='pdf']").forEach((botao) => {
      botao.addEventListener("click", () => abrirPdf(botao.dataset.id, botao.dataset.nome));
    });
    conteudoLista.querySelectorAll("[data-acao='entrevista']").forEach((botao) => {
      botao.addEventListener("click", () => abrirModalEntrevista(botao.dataset.id));
    });
  }

  function cartaoCandidato(candidatura, ehElite) {
    const entrevista = STORAGE.entrevistaDe(candidatura.id);
    const dataEnvio = new Date(candidatura.criadoEm).toLocaleString("pt-BR", {
      dateStyle: "short",
      timeStyle: "short",
    });

    let acaoEntrevista;
    if (entrevista) {
      const quando = new Date(entrevista.dataHora).toLocaleString("pt-BR", {
        dateStyle: "short",
        timeStyle: "short",
      });
      acaoEntrevista =
        '<span class="badge badge--verde">✔ Entrevista agendada · ' + escapar(quando) + "</span>";
    } else {
      acaoEntrevista =
        '<button class="botao botao--verde botao--mini" data-acao="entrevista" data-id="' +
        escapar(candidatura.id) + '">📅 Agendar Entrevista</button>';
    }

    return (
      '<article class="cartao-candidato' + (ehElite ? " elite" : "") + '">' +
      '<div class="nota-circulo' + (ehElite ? " dez" : "") + '">' + candidatura.notaIa + "</div>" +
      '<div class="dados">' +
      "<h3>" + escapar(candidatura.candidatoNome) +
      (ehElite ? ' <span class="badge badge--ouro">10/10</span>' : "") +
      "</h3>" +
      '<p class="contato">' +
      escapar(candidatura.candidatoEmail) + " · " + escapar(candidatura.candidatoTelefone) +
      " · recebido em " + escapar(dataEnvio) +
      "</p></div>" +
      '<div class="acoes">' +
      '<button class="botao botao--vidro botao--mini" data-acao="pdf" data-id="' +
      escapar(candidatura.id) + '" data-nome="' + escapar(candidatura.nomeArquivo) +
      '">📄 Currículo (PDF)</button>' +
      acaoEntrevista +
      "</div>" +
      '<div class="resumo-ia"><h4>Resumo do perfil (gerado na triagem)</h4>' +
      escapar(candidatura.resumoIa) +
      "</div>" +
      "</article>"
    );
  }

  async function abrirPdf(candidaturaId, nomeArquivo) {
    const blob = await STORAGE.lerPdf(candidaturaId);
    if (!blob) {
      alert("PDF não encontrado neste navegador. Nesta demonstração, os arquivos ficam salvos apenas no navegador em que a candidatura foi enviada.");
      return;
    }
    const url = URL.createObjectURL(blob);
    const janela = window.open(url, "_blank");
    if (!janela) {
      // pop-up bloqueado: força download
      const link = document.createElement("a");
      link.href = url;
      link.download = nomeArquivo || "curriculo.pdf";
      link.click();
    }
    setTimeout(() => URL.revokeObjectURL(url), 60000);
  }

  /* ---------------- agendamento de entrevista ---------------- */

  function abrirModalEntrevista(candidaturaId) {
    const candidatura = STORAGE.listarAprovados(seletorCategoria.value).find(
      (c) => c.id === candidaturaId
    );
    if (!candidatura) return;

    candidaturaSelecionada = candidatura;
    modalCandidato.textContent =
      candidatura.candidatoNome + " · " + candidatura.candidatoEmail;
    campoData.value = "";
    campoHora.value = "";
    campoData.min = new Date().toISOString().slice(0, 10);
    erroEntrevista.hidden = true;
    previaEmail.hidden = true;
    modal.hidden = false;
    campoData.focus();
  }

  botaoCancelarModal.addEventListener("click", fecharModal);
  modal.addEventListener("click", (evento) => {
    if (evento.target === modal) fecharModal();
  });
  document.addEventListener("keydown", (evento) => {
    if (evento.key === "Escape" && !modal.hidden) fecharModal();
  });

  function fecharModal() {
    modal.hidden = true;
    candidaturaSelecionada = null;
  }

  function montarEmail(candidatura, dataISO, hora) {
    const categoria = window.CATEGORIAS[candidatura.categoria];
    const cargo = categoria ? categoria.cargoEmail : "—";
    const dataBr = new Date(dataISO + "T00:00:00").toLocaleDateString("pt-BR");

    const assunto = "Convite para Entrevista — Processo Seletivo " + cargo;
    const corpo =
      "Olá, " + candidatura.candidatoNome + ",\n\n" +
      "Seu perfil avançou para a próxima etapa do processo seletivo para a vaga de " +
      cargo + ". Gostaríamos de convidá-lo(a) para uma entrevista no dia " +
      dataBr + " às " + hora + ".\n\n" +
      "Por favor, confirme sua disponibilidade respondendo este e-mail.\n\n" +
      "Atenciosamente,\n" +
      "Equipe de Recrutamento e Seleção\n\n" +
      "--\n" + CONFIG.AVISO_LEGAL;

    return { assunto, corpo };
  }

  botaoConfirmar.addEventListener("click", () => {
    if (!candidaturaSelecionada) return;
    erroEntrevista.hidden = true;

    const data = campoData.value;
    const hora = campoHora.value;
    if (!data || !hora) {
      erroEntrevista.textContent = "Escolha a data e o horário da entrevista.";
      erroEntrevista.hidden = false;
      return;
    }

    const { assunto, corpo } = montarEmail(candidaturaSelecionada, data, hora);

    // Registra a entrevista (equivale ao registro em banco + disparo pela
    // integração de e-mail no backend real).
    STORAGE.salvarEntrevista({
      candidaturaId: candidaturaSelecionada.id,
      dataHora: data + "T" + hora,
    });

    previaEmail.textContent = "Assunto: " + assunto + "\n\n" + corpo;
    previaEmail.hidden = false;

    // Dispara o e-mail pelo cliente padrão do avaliador.
    const mailto =
      "mailto:" + encodeURIComponent(candidaturaSelecionada.candidatoEmail) +
      "?subject=" + encodeURIComponent(assunto) +
      "&body=" + encodeURIComponent(corpo);
    window.location.href = mailto;

    botaoConfirmar.textContent = "E-mail preparado ✔";
    botaoConfirmar.disabled = true;
    setTimeout(() => {
      botaoConfirmar.textContent = "Confirmar e enviar e-mail";
      botaoConfirmar.disabled = false;
      fecharModal();
      renderizarLista();
    }, 2500);
  });
})();
