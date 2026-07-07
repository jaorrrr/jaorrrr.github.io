/**
 * Camada de persistência da demonstração.
 *
 * Em produção estes dados morariam em um banco relacional no backend
 * (tabelas candidatos / candidaturas / entrevistas — ver README). Nesta
 * demonstração estática tudo fica NO NAVEGADOR DO VISITANTE:
 *   - registros           → localStorage
 *   - arquivos PDF        → IndexedDB (suporta blobs grandes)
 * Nada é enviado a servidor algum — os dados pessoais não saem da máquina.
 */
(function () {
  "use strict";

  const NOME_BANCO = "azul_demo_pdfs";
  const STORE = "pdfs";

  function abrirBanco() {
    return new Promise((resolve, reject) => {
      const req = indexedDB.open(NOME_BANCO, 1);
      req.onupgradeneeded = () => {
        if (!req.result.objectStoreNames.contains(STORE)) {
          req.result.createObjectStore(STORE);
        }
      };
      req.onsuccess = () => resolve(req.result);
      req.onerror = () => reject(req.error);
    });
  }

  async function guardarPdf(chave, blob) {
    const db = await abrirBanco();
    return new Promise((resolve, reject) => {
      const tx = db.transaction(STORE, "readwrite");
      tx.objectStore(STORE).put(blob, chave);
      tx.oncomplete = () => resolve();
      tx.onerror = () => reject(tx.error);
    });
  }

  async function lerPdf(chave) {
    const db = await abrirBanco();
    return new Promise((resolve, reject) => {
      const tx = db.transaction(STORE, "readonly");
      const req = tx.objectStore(STORE).get(chave);
      req.onsuccess = () => resolve(req.result || null);
      req.onerror = () => reject(req.error);
    });
  }

  function lerLista(chave) {
    try {
      return JSON.parse(localStorage.getItem(chave)) || [];
    } catch {
      return [];
    }
  }

  function gravarLista(chave, lista) {
    localStorage.setItem(chave, JSON.stringify(lista));
  }

  function uid() {
    return Date.now().toString(36) + "-" + Math.random().toString(36).slice(2, 10);
  }

  async function sha256Hex(texto) {
    const dados = new TextEncoder().encode(texto);
    const hash = await crypto.subtle.digest("SHA-256", dados);
    return [...new Uint8Array(hash)]
      .map((b) => b.toString(16).padStart(2, "0"))
      .join("");
  }

  /* ---------- operações de domínio ---------- */

  function salvarCandidato({ nome, email, telefone }) {
    const candidatos = lerLista(CONFIG.CHAVE_CANDIDATOS);
    const existente = candidatos.find(
      (c) => c.email.toLowerCase() === email.toLowerCase()
    );
    if (existente) {
      existente.nome = nome;
      existente.telefone = telefone;
      gravarLista(CONFIG.CHAVE_CANDIDATOS, candidatos);
      return existente;
    }
    const novo = { id: uid(), nome, email, telefone, criadoEm: new Date().toISOString() };
    candidatos.push(novo);
    gravarLista(CONFIG.CHAVE_CANDIDATOS, candidatos);
    return novo;
  }

  async function salvarCandidatura({ candidato, categoria, avaliacao, arquivoPdf }) {
    const candidaturas = lerLista(CONFIG.CHAVE_CANDIDATURAS);
    const registro = {
      id: uid(),
      candidatoId: candidato.id,
      candidatoNome: candidato.nome,
      candidatoEmail: candidato.email,
      candidatoTelefone: candidato.telefone,
      categoria,
      nomeArquivo: arquivoPdf.name,
      notaIa: avaliacao.nota,
      justificativaIa: avaliacao.justificativa,
      resumoIa: avaliacao.resumo,
      status: avaliacao.nota >= CONFIG.NOTA_CORTE ? "aprovado_triagem" : "arquivado",
      criadoEm: new Date().toISOString(),
    };
    await guardarPdf(registro.id, arquivoPdf);
    candidaturas.push(registro);
    gravarLista(CONFIG.CHAVE_CANDIDATURAS, candidaturas);
    return registro;
  }

  function listarAprovados(categoria) {
    return lerLista(CONFIG.CHAVE_CANDIDATURAS)
      .filter((c) => c.categoria === categoria && c.notaIa >= CONFIG.NOTA_CORTE)
      .sort((a, b) => b.notaIa - a.notaIa || a.criadoEm.localeCompare(b.criadoEm));
  }

  function salvarEntrevista({ candidaturaId, dataHora }) {
    const entrevistas = lerLista(CONFIG.CHAVE_ENTREVISTAS);
    const registro = {
      id: uid(),
      candidaturaId,
      dataHora,
      emailEnviado: true,
      criadoEm: new Date().toISOString(),
    };
    entrevistas.push(registro);
    gravarLista(CONFIG.CHAVE_ENTREVISTAS, entrevistas);
    return registro;
  }

  function entrevistaDe(candidaturaId) {
    return lerLista(CONFIG.CHAVE_ENTREVISTAS).find(
      (e) => e.candidaturaId === candidaturaId
    );
  }

  window.STORAGE = {
    salvarCandidato,
    salvarCandidatura,
    listarAprovados,
    salvarEntrevista,
    entrevistaDe,
    lerPdf,
    sha256Hex,
    uid,
  };
})();
