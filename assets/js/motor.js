/**
 * Motor de avaliação de currículos — versão demonstração.
 *
 * NOTA DE ARQUITETURA: a especificação prevê um modelo de IA (API da
 * Anthropic/Claude) avaliando o texto do currículo no backend. Como o
 * GitHub Pages é hospedagem estática (não há onde guardar a chave da API
 * com segurança), esta demonstração usa um avaliador DETERMINÍSTICO que
 * aplica a mesma régua de critérios da seção 3 do briefing sobre o texto
 * extraído do PDF. A interface de saída é idêntica à do motor de IA real:
 *   { nota, justificativa, resumo }
 * de modo que trocar esta função por uma chamada ao backend com Claude
 * não exige nenhuma outra mudança no site. Veja o README.
 */
(function () {
  "use strict";

  /** Normaliza o texto extraído do PDF para facilitar a busca. */
  function normalizar(texto) {
    return (texto || "")
      .replace(/ /g, " ")
      .replace(/[ \t]+/g, " ")
      .trim();
  }

  /** Testa um critério (regex comum ou regra especial). */
  function atendeCriterio(criterio, texto) {
    if (criterio.especial === "tresCht") {
      // Nota 10 de Manutenção: as três CHTs precisam aparecer.
      return (
        /\bGMP\b/i.test(texto) &&
        /c[eé]lula/i.test(texto) &&
        /avi[oô]nicos/i.test(texto)
      );
    }
    return criterio.regex ? criterio.regex.test(texto) : false;
  }

  function avaliarFaixa(criterios, texto) {
    const atendidos = [];
    const pendentes = [];
    for (const c of criterios) {
      (atendeCriterio(c, texto) ? atendidos : pendentes).push(c.rotulo);
    }
    return {
      atendidos,
      pendentes,
      fracao: criterios.length ? atendidos.length / criterios.length : 0,
      total: criterios.length,
    };
  }

  /**
   * Avalia o texto de um currículo para uma categoria.
   * @returns {{nota:number, justificativa:string, resumo:string}}
   */
  function avaliarCurriculo(textoBruto, categoriaId) {
    const categoria = window.CATEGORIAS[categoriaId];
    if (!categoria) throw new Error("Categoria desconhecida: " + categoriaId);

    const texto = normalizar(textoBruto);
    const base = avaliarFaixa(categoria.criterios.base, texto);
    const medio = avaliarFaixa(categoria.criterios.medio, texto);
    const elite = avaliarFaixa(categoria.criterios.elite, texto);

    let nota;
    if (!texto || texto.length < 40) {
      // PDF sem texto legível (por exemplo, digitalização sem OCR).
      nota = 0;
    } else if (base.fracao < 0.5) {
      // Não cobre os requisitos essenciais da faixa "Nota 7".
      nota = Math.min(6, Math.round(base.fracao * 10) + (elite.atendidos.length ? 1 : 0));
    } else {
      // Cobre os essenciais: parte de 7 e sobe conforme os diferenciais.
      const bonus = Math.round(medio.fracao * 1.4 + elite.fracao * 1.6);
      nota = Math.min(9, 7 + bonus);
      if (elite.fracao >= 0.8 && base.fracao >= 0.75) nota = 10;
    }

    return {
      nota,
      justificativa: montarJustificativa(nota, base, medio, elite),
      resumo: montarResumo(categoria, nota, base, medio, elite, texto),
    };
  }

  function montarJustificativa(nota, base, medio, elite) {
    const linhas = [
      `Requisitos essenciais (faixa nota 7): ${base.atendidos.length}/${base.total} atendidos.`,
      `Diferenciais (faixa 8–9): ${medio.atendidos.length}/${medio.total} atendidos.`,
      `Critérios de elite (nota 10): ${elite.atendidos.length}/${elite.total} atendidos.`,
      `Nota final atribuída: ${nota}/10.`,
    ];
    if (base.pendentes.length && nota < 7) {
      linhas.push(`Requisitos essenciais não localizados: ${base.pendentes.join("; ")}.`);
    }
    return linhas.join(" ");
  }

  function montarResumo(categoria, nota, base, medio, elite, texto) {
    const fortes = [...elite.atendidos, ...base.atendidos, ...medio.atendidos].slice(0, 5);
    const lacunas = elite.pendentes.slice(0, 3);

    let perfil;
    if (nota === 10) {
      perfil = "Perfil de elite — atende ao padrão máximo da régua para a categoria e está pronto para priorização imediata.";
    } else if (nota >= 8) {
      perfil = "Perfil acima do requisito mínimo, com diferenciais relevantes além da faixa de entrada.";
    } else if (nota >= 7) {
      perfil = "Perfil operacional sólido — cobre os requisitos essenciais da categoria.";
    } else {
      perfil = "Perfil abaixo do requisito mínimo definido para a categoria neste momento.";
    }

    const partes = [
      `Candidatura para ${categoria.nome} (${categoria.cargos}). ${perfil}`,
    ];
    if (fortes.length) {
      partes.push(`Pontos fortes identificados no currículo: ${fortes.join("; ")}.`);
    } else {
      partes.push("Não foram identificadas evidências claras dos requisitos da categoria no texto do currículo.");
    }
    if (nota >= 7 && lacunas.length) {
      partes.push(`Para alcançar o perfil 10/10, faltam evidências de: ${lacunas.join("; ")}.`);
    }
    if (texto.length < 40) {
      partes.push("Atenção: o PDF enviado não contém texto legível (possível digitalização sem OCR).");
    }
    return partes.join(" ");
  }

  window.MOTOR = { avaliarCurriculo };
})();
