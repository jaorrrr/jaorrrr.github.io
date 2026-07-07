/**
 * Componentes compartilhados: cenário aeronáutico de fundo, cabeçalho e
 * rodapé (com o aviso legal obrigatório). Injetados em todas as páginas.
 */
(function () {
  "use strict";

  const AVIAO_SVG =
    '<svg viewBox="0 0 64 64" fill="currentColor" aria-hidden="true">' +
    '<path d="M62 32c0 1.9-1.6 3.4-3.5 3.4H41.2L26.7 58.1c-.4.6-1.1 1-1.8 1h-4.6c-.9 0-1.5-.9-1.2-1.7l7.1-21.9H13.4l-4.8 6.4c-.3.4-.7.6-1.2.6H4.2c-.8 0-1.4-.8-1.2-1.6L6 32 3 23.1c-.2-.8.4-1.6 1.2-1.6h3.2c.5 0 .9.2 1.2.6l4.8 6.4h12.8l-7.1-21.9c-.3-.8.3-1.7 1.2-1.7h4.6c.7 0 1.4.4 1.8 1l14.5 22.7h17.3c1.9 0 3.5 1.5 3.5 3.4z"/></svg>';

  function montarCeu() {
    const ceu = document.createElement("div");
    ceu.className = "ceu";
    ceu.setAttribute("aria-hidden", "true");
    ceu.innerHTML =
      '<svg class="rota" viewBox="0 0 1200 800" preserveAspectRatio="none">' +
      '<path d="M -40 720 C 260 560, 420 640, 620 420 S 980 160, 1260 60" />' +
      '<path d="M -40 300 C 300 340, 700 120, 1260 260" />' +
      '<circle cx="620" cy="420" r="5"/><circle cx="1050" cy="215" r="5"/><circle cx="230" cy="330" r="5"/>' +
      "</svg>" +
      '<div class="aviao" style="color:#ffffff">' + AVIAO_SVG + "</div>" +
      '<div class="aviao aviao--2" style="color:#ffc72c">' + AVIAO_SVG + "</div>";
    document.body.prepend(ceu);
  }

  function montarTopo() {
    const ativo = document.body.dataset.pagina || "";
    const topo = document.createElement("header");
    topo.className = "topo";
    topo.innerHTML =
      '<div class="topo__conteudo">' +
      '<a class="marca" href="/">' +
      '<span style="color:#ffc72c">' + AVIAO_SVG + "</span>" +
      "<span>Azul Talentos<small>conceito de estudo — não oficial</small></span>" +
      "</a>" +
      "<nav>" +
      botaoNav("/vagas/", "Nossos Cargos", ativo === "vagas") +
      botaoNav("/sobre-nos/", "Sobre Nós", ativo === "sobre") +
      '<a class="botao botao--vidro botao--mini" href="/acesso-restrito/">🔒 Acesso Restrito</a>' +
      "</nav></div>";
    document.body.prepend(topo);
  }

  function botaoNav(href, rotulo, ativo) {
    return (
      '<a class="botao botao--vidro botao--mini" ' +
      (ativo ? 'style="border-color:#ffc72c;color:#ffc72c" ' : "") +
      'href="' + href + '">' + rotulo + "</a>"
    );
  }

  function montarRodape() {
    const rodape = document.createElement("footer");
    rodape.className = "rodape";
    rodape.innerHTML =
      '<div class="rodape__conteudo">' +
      '<p class="aviso-legal"><strong>Aviso legal:</strong> ' + CONFIG.AVISO_LEGAL + "</p>" +
      '<div class="links">' +
      '<a href="/">Início</a>' +
      '<a href="/vagas/">Nossos Cargos</a>' +
      '<a href="/sobre-nos/">Sobre Nós</a>' +
      '<a href="/acesso-restrito/">Acesso Restrito</a>' +
      "</div></div>";
    document.body.append(rodape);
  }

  document.addEventListener("DOMContentLoaded", () => {
    montarCeu();
    montarTopo();
    montarRodape();
  });
})();
