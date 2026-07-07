/**
 * Fluxo de candidatura:
 *   1. cadastro simplificado (nome, e-mail, telefone + consentimento)
 *   2. upload do currículo — SOMENTE PDF (verificação de extensão, MIME e
 *      assinatura %PDF nos primeiros bytes)
 *   3. extração do texto com pdf.js + avaliação pelo motor (régua da seção 3)
 *   4. redirecionamento para /obrigado/ — a nota NUNCA é exibida ao candidato
 */
(function () {
  "use strict";

  const TAMANHO_MAXIMO = 10 * 1024 * 1024; // 10 MB

  pdfjsLib.GlobalWorkerOptions.workerSrc = "/assets/vendor/pdf.worker.min.js";

  // ---- categoria escolhida na página /vagas/ ----
  const parametros = new URLSearchParams(window.location.search);
  const categoriaId = parametros.get("categoria");
  const categoria = window.CATEGORIAS[categoriaId];

  if (!categoria) {
    // Sem categoria válida não há candidatura: volta para a lista de cargos.
    window.location.replace("/vagas/");
    return;
  }

  document.getElementById("titulo-categoria").textContent =
    "Candidatura — " + categoria.nome;
  document.getElementById("subtitulo-categoria").textContent =
    "Cargos desta área: " + categoria.cargos;

  // ---- elementos ----
  const formCadastro = document.getElementById("form-cadastro");
  const erroCadastro = document.getElementById("erro-cadastro");
  const passoUpload = document.getElementById("passo-upload");
  const passoProcessando = document.getElementById("passo-processando");
  const areaUpload = document.getElementById("area-upload");
  const inputArquivo = document.getElementById("arquivo");
  const nomeArquivo = document.getElementById("nome-arquivo");
  const erroUpload = document.getElementById("erro-upload");
  const botaoEnviar = document.getElementById("botao-enviar");
  const etapa1 = document.getElementById("etapa-1");
  const etapa2 = document.getElementById("etapa-2");
  const etapa3 = document.getElementById("etapa-3");

  let candidato = null;
  let arquivoPdf = null;

  function mostrarErro(elemento, mensagem) {
    elemento.textContent = mensagem;
    elemento.hidden = !mensagem;
  }

  // ---- passo 1: cadastro (aberto a qualquer pessoa, sem aprovação prévia) ----
  formCadastro.addEventListener("submit", (evento) => {
    evento.preventDefault();
    mostrarErro(erroCadastro, "");

    const nome = document.getElementById("nome").value.trim();
    const email = document.getElementById("email").value.trim();
    const telefone = document.getElementById("telefone").value.trim();
    const consentiu = document.getElementById("consentimento").checked;

    if (nome.length < 5 || !nome.includes(" ")) {
      return mostrarErro(erroCadastro, "Informe seu nome completo.");
    }
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email)) {
      return mostrarErro(erroCadastro, "Informe um e-mail válido.");
    }
    if (telefone.replace(/\D/g, "").length < 10) {
      return mostrarErro(erroCadastro, "Informe um telefone válido com DDD.");
    }
    if (!consentiu) {
      return mostrarErro(
        erroCadastro,
        "É necessário autorizar o uso dos dados para avaliarmos a sua candidatura."
      );
    }

    candidato = STORAGE.salvarCandidato({ nome, email, telefone });

    formCadastro.hidden = true;
    passoUpload.hidden = false;
    etapa1.classList.replace("ativa", "feita");
    etapa2.classList.add("ativa");
  });

  // ---- passo 2: upload somente PDF ----
  areaUpload.addEventListener("click", () => inputArquivo.click());
  areaUpload.addEventListener("keydown", (evento) => {
    if (evento.key === "Enter" || evento.key === " ") {
      evento.preventDefault();
      inputArquivo.click();
    }
  });
  areaUpload.addEventListener("dragover", (evento) => {
    evento.preventDefault();
    areaUpload.classList.add("arrastando");
  });
  areaUpload.addEventListener("dragleave", () =>
    areaUpload.classList.remove("arrastando")
  );
  areaUpload.addEventListener("drop", (evento) => {
    evento.preventDefault();
    areaUpload.classList.remove("arrastando");
    if (evento.dataTransfer.files.length) {
      validarArquivo(evento.dataTransfer.files[0]);
    }
  });
  inputArquivo.addEventListener("change", () => {
    if (inputArquivo.files.length) validarArquivo(inputArquivo.files[0]);
  });

  async function validarArquivo(arquivo) {
    mostrarErro(erroUpload, "");
    arquivoPdf = null;
    botaoEnviar.disabled = true;
    nomeArquivo.hidden = true;

    const nomeMinusculo = (arquivo.name || "").toLowerCase();
    const mimeOk =
      arquivo.type === "application/pdf" ||
      (arquivo.type === "" && nomeMinusculo.endsWith(".pdf"));

    if (!nomeMinusculo.endsWith(".pdf") || !mimeOk) {
      return mostrarErro(
        erroUpload,
        "Apenas arquivos PDF são aceitos. Converta seu currículo para PDF e tente novamente."
      );
    }
    if (arquivo.size > TAMANHO_MAXIMO) {
      return mostrarErro(erroUpload, "O arquivo excede o limite de 10 MB.");
    }

    // assinatura %PDF- nos primeiros bytes
    const cabecalho = new Uint8Array(await arquivo.slice(0, 5).arrayBuffer());
    const assinatura = String.fromCharCode(...cabecalho);
    if (!assinatura.startsWith("%PDF")) {
      return mostrarErro(
        erroUpload,
        "O arquivo enviado não parece ser um PDF válido."
      );
    }

    arquivoPdf = arquivo;
    nomeArquivo.textContent = "✔ " + arquivo.name;
    nomeArquivo.hidden = false;
    botaoEnviar.disabled = false;
  }

  // ---- passo 3: extração, avaliação e envio ----
  botaoEnviar.addEventListener("click", async () => {
    if (!arquivoPdf || !candidato) return;

    passoUpload.hidden = true;
    passoProcessando.hidden = false;
    etapa2.classList.replace("ativa", "feita");
    etapa3.classList.add("ativa");

    try {
      const texto = await extrairTextoPdf(arquivoPdf);
      const avaliacao = MOTOR.avaliarCurriculo(texto, categoriaId);
      await STORAGE.salvarCandidatura({
        candidato,
        categoria: categoriaId,
        avaliacao,
        arquivoPdf,
      });
    } catch (erro) {
      // Mesmo com falha de leitura, registra a candidatura com nota 0 para
      // que o fluxo do candidato nunca seja interrompido nem exponha a nota.
      console.error("Falha ao processar o currículo:", erro);
      try {
        await STORAGE.salvarCandidatura({
          candidato,
          categoria: categoriaId,
          avaliacao: {
            nota: 0,
            justificativa: "Falha na leitura do PDF: " + (erro && erro.message),
            resumo:
              "Não foi possível extrair o texto do currículo enviado. Recomenda-se solicitar reenvio em PDF com texto selecionável.",
          },
          arquivoPdf,
        });
      } catch (erroGravacao) {
        console.error("Falha ao registrar a candidatura:", erroGravacao);
      }
    }

    // Independentemente da nota, o candidato segue para a página final.
    setTimeout(() => window.location.assign("/obrigado/"), 1200);
  });

  async function extrairTextoPdf(arquivo) {
    const dados = await arquivo.arrayBuffer();
    const pdf = await pdfjsLib.getDocument({ data: dados }).promise;
    const partes = [];
    for (let numero = 1; numero <= pdf.numPages; numero++) {
      const pagina = await pdf.getPage(numero);
      const conteudo = await pagina.getTextContent();
      partes.push(conteudo.items.map((item) => item.str).join(" "));
    }
    return partes.join("\n");
  }
})();
