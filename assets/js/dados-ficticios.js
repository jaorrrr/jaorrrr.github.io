/**
 * Popula o painel com candidaturas e entrevistas fictícias na primeira
 * visita, apenas para fins de demonstração/portfólio. Não sobrescreve
 * dados reais: só roda quando o localStorage do painel ainda está vazio.
 * Segue exatamente o formato gravado por STORAGE.salvarCandidatura /
 * STORAGE.salvarEntrevista (ver assets/js/storage.js).
 */
(function () {
  "use strict";

  const NOMES = [
    "Ana Beatriz Souza", "Carlos Eduardo Lima", "Fernanda Ribeiro", "Gustavo Almeida",
    "Juliana Castro", "Marcelo Teixeira", "Patrícia Nogueira", "Rafael Andrade",
    "Camila Ferreira", "Bruno Cardoso", "Larissa Martins", "Thiago Barbosa",
    "Vanessa Pereira", "Diego Rocha", "Isabela Correia", "Felipe Gonçalves",
    "Mariana Duarte", "Rodrigo Sales", "Beatriz Freitas", "Lucas Monteiro",
    "Renata Vieira", "André Moraes", "Débora Pinto", "Vinícius Tavares",
  ];

  function nomeArquivo(nome) {
    return nome.toLowerCase().replace(/[^a-z ]/g, "").replace(/\s+/g, "-") + "-curriculo.pdf";
  }

  function emailDe(nome) {
    return (
      nome.toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/\s+/g, ".") +
      "@exemplo.com.br"
    );
  }

  function telefoneAleatorio() {
    const ddd = 11 + Math.floor(Math.random() * 79);
    const numero = 90000000 + Math.floor(Math.random() * 9999999);
    return "(" + ddd + ") " + String(numero).slice(0, 5) + "-" + String(numero).slice(5);
  }

  function dataAleatoria(diasAtras) {
    const agora = Date.now();
    const passado = agora - Math.random() * diasAtras * 24 * 60 * 60 * 1000;
    return new Date(passado).toISOString();
  }

  function resumoFicticio(nome, categoriaNome, nota) {
    if (nota === 10) {
      return (
        "Perfil de destaque para " + categoriaNome + ". " + nome.split(" ")[0] +
        " atende a todos os requisitos obrigatórios e apresenta diferenciais de elite " +
        "identificados no currículo, com forte aderência ao cargo."
      );
    }
    if (nota >= 8) {
      return (
        nome.split(" ")[0] + " atende aos requisitos-base da vaga de " + categoriaNome +
        " e apresenta ao menos um diferencial relevante identificado na triagem automática."
      );
    }
    return (
      nome.split(" ")[0] + " atende aos requisitos mínimos para " + categoriaNome +
      " identificados no currículo enviado."
    );
  }

  function jaTemDados() {
    try {
      const candidaturas = JSON.parse(localStorage.getItem(CONFIG.CHAVE_CANDIDATURAS)) || [];
      return candidaturas.length > 0;
    } catch {
      return false;
    }
  }

  function semear() {
    if (typeof window.CATEGORIAS === "undefined" || typeof window.CONFIG === "undefined") return;
    if (jaTemDados()) return;

    const categoriasIds = Object.keys(window.CATEGORIAS);
    const candidatos = [];
    const candidaturas = [];
    const entrevistas = [];
    let indiceNome = 0;

    categoriasIds.forEach((categoriaId) => {
      const categoria = window.CATEGORIAS[categoriaId];
      const quantidade = 5 + Math.floor(Math.random() * 3); // 5–7 por categoria

      for (let i = 0; i < quantidade; i++) {
        const nome = NOMES[indiceNome % NOMES.length];
        indiceNome++;

        // distribuição de notas: poucos 10, mais 7–9, alguns abaixo do corte (arquivados)
        const sorteio = Math.random();
        let nota;
        if (sorteio < 0.12) nota = 10;
        else if (sorteio < 0.55) nota = 7 + Math.floor(Math.random() * 2);
        else if (sorteio < 0.85) nota = 8;
        else nota = 4 + Math.floor(Math.random() * 3); // 4–6, fica arquivado

        const id = STORAGE.uid();
        const candidatoId = STORAGE.uid();
        const email = emailDe(nome + "." + i);
        const telefone = telefoneAleatorio();
        const criadoEm = dataAleatoria(45);

        candidatos.push({ id: candidatoId, nome, email, telefone, criadoEm });

        candidaturas.push({
          id,
          candidatoId,
          candidatoNome: nome,
          candidatoEmail: email,
          candidatoTelefone: telefone,
          categoria: categoriaId,
          nomeArquivo: nomeArquivo(nome),
          notaIa: nota,
          justificativaIa: "Avaliação automática gerada a partir dos critérios da categoria " + categoria.nome + ".",
          resumoIa: resumoFicticio(nome, categoria.nome, nota),
          status: nota >= window.CONFIG.NOTA_CORTE ? "aprovado_triagem" : "arquivado",
          criadoEm,
        });

        // ~40% dos aprovados já têm entrevista marcada
        if (nota >= window.CONFIG.NOTA_CORTE && Math.random() < 0.4) {
          const diasFuturos = 1 + Math.floor(Math.random() * 20);
          const dataEntrevista = new Date(Date.now() + diasFuturos * 24 * 60 * 60 * 1000);
          const hora = 9 + Math.floor(Math.random() * 8);
          dataEntrevista.setHours(hora, 0, 0, 0);
          entrevistas.push({
            id: STORAGE.uid(),
            candidaturaId: id,
            dataHora: dataEntrevista.toISOString().slice(0, 16),
            emailEnviado: true,
            criadoEm: dataAleatoria(10),
          });
        }
      }
    });

    localStorage.setItem(window.CONFIG.CHAVE_CANDIDATOS, JSON.stringify(candidatos));
    localStorage.setItem(window.CONFIG.CHAVE_CANDIDATURAS, JSON.stringify(candidaturas));
    localStorage.setItem(window.CONFIG.CHAVE_ENTREVISTAS, JSON.stringify(entrevistas));
  }

  window.DADOS_FICTICIOS = { semear };
  semear();
})();
