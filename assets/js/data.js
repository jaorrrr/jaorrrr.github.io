/**
 * Categorias de vaga e régua de avaliação (seção 3 do briefing).
 *
 * Cada categoria tem três faixas de critérios detectados no texto do currículo:
 *  - base  → requisitos da "Nota 7"
 *  - medio → diferenciais da faixa "acima de 7, abaixo de 10"
 *  - elite → requisitos da "Nota 10"
 *
 * Os critérios usam expressões regulares em português (com tolerância a
 * acentos) para localizar evidências no texto extraído do PDF.
 */
window.CATEGORIAS = {
  "tripulacao-tecnica": {
    nome: "Tripulação Técnica",
    cargoEmail: "Piloto / Copiloto",
    cargos: "Pilotos e Copilotos (Azul e Azul Conecta)",
    icone: "aviao",
    destaque:
      "Destaque no currículo: código CANAC, validade do CMA de 1ª classe, nível de inglês ICAO e tabela de horas de voo (CIV).",
    criterios: {
      base: [
        { id: "pc", rotulo: "Licença de Piloto Comercial (PC) válida", regex: /piloto\s+comercial|licen[çc]a\s+de\s+piloto|\bPCA\b|\bPC\s*[-–—(]/i },
        { id: "mlte", rotulo: "Habilitação Multimotor (MLTE) ativa", regex: /multimotor|\bMLTE\b/i },
        { id: "ifr", rotulo: "Habilitação IFR ativa", regex: /\bIFR\b|voo\s+por\s+instrumentos/i },
        { id: "cma1", rotulo: "CMA de 1ª classe em dia", regex: /CMA[^\n]{0,40}(1|primeira)|certificado\s+m[eé]dico\s+aeron[aá]utic/i },
        { id: "ingles", rotulo: "Inglês em nível funcional (ICAO em andamento ou equivalente)", regex: /ingl[eê]s|\bICAO\b|\bTOEIC\b|\bTOEFL\b/i },
      ],
      medio: [
        { id: "inva", rotulo: "Experiência como instrutor de voo (INVA)", regex: /instrutor[a]?\s+de\s+voo|\bINVA\b/i },
        { id: "horas", rotulo: "Tabela de horas de voo registrada (CIV)", regex: /horas\s+de\s+voo|\bCIV\b|caderneta\s+individual/i },
        { id: "canac", rotulo: "Código CANAC informado", regex: /\bCANAC\b/i },
        { id: "mnte", rotulo: "Habilitação monomotor (MNTE) válida", regex: /monomotor|\bMNTE\b/i },
      ],
      elite: [
        { id: "pla", rotulo: "Teoria de Piloto de Linha Aérea (CCT PLA) aprovada", regex: /\bPLA\b|piloto\s+de\s+linha\s+a[eé]rea/i },
        { id: "icao4", rotulo: "Inglês ICAO nível 4+ válido", regex: /ICAO[^\n]{0,25}(n[ií]vel\s*)?[4-6]/i },
        { id: "jet", rotulo: "Jet Training concluído ou experiência Multi-Crew comercial", regex: /jet\s*training|multi[\s-]?crew|\bMCC\b|opera[çc][aã]o\s+de\s+jato/i },
        { id: "grad", rotulo: "Graduação em Ciências Aeronáuticas concluída", regex: /ci[eê]ncias\s+aeron[aá]uticas/i },
        { id: "visto", rotulo: "Passaporte e visto americano B1/B2 ativos", regex: /visto[^\n]{0,30}(americano|B1|B2)|B1\s*\/\s*B2/i },
      ],
    },
  },

  "tripulacao-comercial": {
    nome: "Tripulação Comercial",
    cargoEmail: "Comissário(a) de Voo",
    cargos: "Comissários de Voo",
    icone: "comissario",
    destaque:
      "Destaque no currículo: código ANAC, CCT ou CHT de comissário, validade do CMA de 2ª classe e fluência em idiomas.",
    criterios: {
      base: [
        { id: "cct", rotulo: "Curso de comissário com aprovação na prova teórica ANAC (CCT/CHT)", regex: /comiss[aá]ri[oa]|\bCCT\b|\bCHT\b/i },
        { id: "cma2", rotulo: "CMA de 2ª classe ativo", regex: /CMA[^\n]{0,40}(2|segunda)|certificado\s+m[eé]dico\s+aeron[aá]utic/i },
        { id: "ingles", rotulo: "Inglês intermediário para conversação", regex: /ingl[eê]s/i },
        { id: "atend", rotulo: "Pelo menos 1 ano de atendimento presencial", regex: /atendimento|recep[çc][aã]o|hotelaria|com[eé]rcio|loja/i },
      ],
      medio: [
        { id: "anac", rotulo: "Código ANAC informado", regex: /\bANAC\b/i },
        { id: "vendas", rotulo: "Histórico em vendas, resolução de problemas ou eventos", regex: /vendas|resolu[çc][aã]o\s+de\s+problemas|eventos|promotor/i },
        { id: "idioma2", rotulo: "Segundo idioma em nível básico/intermediário", regex: /espanhol|franc[eê]s|italiano|alem[aã]o/i },
      ],
      elite: [
        { id: "fluencia", rotulo: "Fluência comprovada em inglês e espanhol", regex: /(ingl[eê]s[^\n]{0,30}(fluente|avan[çc]ad))|((fluente|avan[çc]ad)[^\n]{0,30}ingl[eê]s)/i },
        { id: "espanhol", rotulo: "Espanhol fluente/avançado", regex: /espanhol[^\n]{0,30}(fluente|avan[çc]ad)|(fluente|avan[çc]ad)[^\n]{0,30}espanhol/i },
        { id: "luxo", rotulo: "Experiência em atendimento de luxo/hotelaria", regex: /luxo|alto\s+padr[aã]o|5\s*estrelas|primeira\s+classe|hotelaria/i },
        { id: "passaporte", rotulo: "Passaporte válido e certificado internacional de vacinação", regex: /passaporte|vacina[çc][aã]o\s+internacional|certificado\s+internacional/i },
        { id: "superior", rotulo: "Superior em Turismo, Hotelaria ou Ciências Aeronáuticas", regex: /(superior|gradua[çc][aã]o|bacharel|tecn[oó]log)[^\n]{0,60}(turismo|hotelaria|ci[eê]ncias\s+aeron[aá]uticas)/i },
      ],
    },
  },

  "atendimento-aeroporto": {
    nome: "Atendimento e Aeroporto",
    cargoEmail: "Agente / Coordenador de Aeroporto",
    cargos:
      "Agente de Aeroporto, Agente de Excelência ao Cliente, Coordenador de Aeroporto",
    icone: "balcao",
    destaque:
      "Destaque no currículo: flexibilidade de horário, controle emocional e domínio de sistemas de atendimento.",
    criterios: {
      base: [
        { id: "medio", rotulo: "Ensino médio completo", regex: /ensino\s+m[eé]dio/i },
        { id: "escala", rotulo: "Disponibilidade para escalas (madrugada, feriados, fins de semana)", regex: /disponibilidade|escala|madrugada|feriado|fins?\s+de\s+semana|turno/i },
        { id: "info", rotulo: "Informática básica", regex: /inform[aá]tica|pacote\s+office|\bword\b|\bexcel\b|windows/i },
        { id: "comunic", rotulo: "Boa comunicação e postura profissional", regex: /comunica[çc][aã]o|postura|relacionamento|proatividade/i },
      ],
      medio: [
        { id: "superandamento", rotulo: "Superior em andamento (diferencial)", regex: /superior[^\n]{0,30}(andamento|cursando)|cursando[^\n]{0,40}(superior|gradua[çc][aã]o|faculdade)/i },
        { id: "idiomainter", rotulo: "Inglês ou espanhol intermediário", regex: /ingl[eê]s|espanhol/i },
        { id: "callcenter", rotulo: "Experiência em call center, hotelaria ou caixa de alta rotatividade", regex: /call\s*center|telemarketing|hotelaria|caixa|SAC\b/i },
      ],
      elite: [
        { id: "superior", rotulo: "Superior em Administração, Logística ou Turismo", regex: /(superior|gradua[çc][aã]o|bacharel|tecn[oó]log)[^\n]{0,60}(administra[çc][aã]o|log[ií]stica|turismo)/i },
        { id: "inglesfluente", rotulo: "Inglês fluente para crises com passageiros estrangeiros", regex: /ingl[eê]s[^\n]{0,30}(fluente|avan[çc]ad)|(fluente|avan[çc]ad)[^\n]{0,30}ingl[eê]s/i },
        { id: "gestao", rotulo: "Experiência em gestão de equipes e metas operacionais", regex: /gest[aã]o\s+de\s+equipe|lideran[çc]a|coordena[çc][aã]o|supervis[aã]o|metas/i },
        { id: "gds", rotulo: "Domínio de sistemas globais (SABRE ou Amadeus)", regex: /\bSABRE\b|\bAmadeus\b|\bGDS\b/i },
      ],
    },
  },

  manutencao: {
    nome: "Manutenção",
    cargoEmail: "Técnico / Analista de Manutenção de Aeronaves",
    cargos:
      "Técnico de Manutenção de Aeronaves (CHT ANAC), Auxiliar de Manutenção, Analista de Programação de Manutenção",
    icone: "chave",
    destaque:
      "Destaque no currículo: siglas de CHT (GMP, Célula, Aviônicos), cursos de familiarização por frota e registro profissional.",
    criterios: {
      base: [
        { id: "tecnico", rotulo: "Curso técnico em manutenção de aeronaves concluído", regex: /t[eé]cnico[^\n]{0,50}manuten[çc][aã]o|manuten[çc][aã]o\s+de\s+aeronaves|aeromec[aâ]nic/i },
        { id: "cht", rotulo: "Ao menos uma CHT ativa (GMP, Célula ou Aviônicos)", regex: /\bCHT\b|\bGMP\b|c[eé]lula|avi[oô]nicos/i },
        { id: "inglestec", rotulo: "Inglês técnico intermediário", regex: /ingl[eê]s/i },
        { id: "oficina", rotulo: "Estágio ou prática em oficina homologada", regex: /oficina|homologad|est[aá]gio|hangar|\bMRO\b/i },
      ],
      medio: [
        { id: "industrial", rotulo: "Experiência em manutenção mecânica industrial/automotiva/frotas", regex: /industrial|automotiv|frota|mec[aâ]nica\s+(geral|pesada)/i },
        { id: "organizacao", rotulo: "Boa organização de ferramentas e estoque", regex: /ferramenta|estoque|almoxarifado|\b5S\b|organiza[çc][aã]o/i },
      ],
      elite: [
        { id: "cht3", rotulo: "3 CHTs ativas (GMP, Célula e Aviônicos)", regex: null, especial: "tresCht" },
        { id: "inglesfluente", rotulo: "Inglês técnico fluente para manuais e boletins", regex: /ingl[eê]s[^\n]{0,40}(fluente|avan[çc]ad|t[eé]cnico\s+fluente)|(fluente|avan[çc]ad)[^\n]{0,30}ingl[eê]s/i },
        { id: "familiarizacao", rotulo: "Cursos de familiarização de motores/sistemas modernos", regex: /familiariza[çc][aã]o|\bA320\b|\bE-?jet\b|\bATR\b|\bEmbraer\b|\bAirbus\b/i },
        { id: "engenharia", rotulo: "Graduação em Engenharia Aeronáutica/Mecânica com CREA ativo", regex: /engenharia[^\n]{0,30}(aeron[aá]utica|mec[aâ]nica)/i },
        { id: "crea", rotulo: "Registro CREA ativo", regex: /\bCREA\b/i },
      ],
    },
  },

  "administrativo-logistica": {
    nome: "Áreas Administrativas e Logística",
    cargoEmail: "Analista / Auxiliar Administrativo",
    cargos:
      "Auxiliar de Cargas, Analistas (Excelência ao Cliente, Auditoria, Compras, Planejamento), vagas corporativas na matriz",
    icone: "grafico",
    destaque:
      "Destaque no currículo: Excel avançado, metodologias ágeis e ferramentas de dados (Power BI, SQL).",
    criterios: {
      base: [
        { id: "superior", rotulo: "Superior completo", regex: /superior\s+completo|gradua[çc][aã]o[^\n]{0,20}(completa|conclu[ií]d)|bacharel|forma[dç][oa][^\n]{0,20}em/i },
        { id: "excel", rotulo: "Excel avançado (tabela dinâmica, PROCV, macros)", regex: /excel[^\n]{0,30}avan[çc]ad|tabela\s+din[aâ]mica|\bPROCV\b|macro|\bVBA\b/i },
        { id: "ingles", rotulo: "Inglês intermediário", regex: /ingl[eê]s/i },
        { id: "b2b", rotulo: "Experiência com fornecedores, conciliações ou atendimento B2B", regex: /fornecedor|concilia[çc]|\bB2B\b|faturamento|compras|auditoria|planejamento/i },
      ],
      medio: [
        { id: "logistica", rotulo: "Técnico em logística", regex: /t[eé]cnico[^\n]{0,30}log[ií]stica|log[ií]stica/i },
        { id: "cargas", rotulo: "Recebimento, conferência de notas fiscais e paletização", regex: /nota\s+fiscal|paletiza|recebimento|confer[eê]ncia|expedi[çc][aã]o/i },
        { id: "turnos", rotulo: "Disponibilidade para turnos", regex: /turno|escala|disponibilidade/i },
        { id: "ageis", rotulo: "Metodologias ágeis", regex: /scrum|kanban|[aá]gil|\bagile\b|lean/i },
      ],
      elite: [
        { id: "formacao", rotulo: "Superior em Economia, Eng. de Produção, Administração ou Contabilidade", regex: /(economia|engenharia\s+de\s+produ[çc][aã]o|administra[çc][aã]o|contabilidade|ci[eê]ncias\s+cont[aá]beis)/i },
        { id: "inglesfluente", rotulo: "Inglês fluente corporativo", regex: /ingl[eê]s[^\n]{0,30}(fluente|avan[çc]ad)|(fluente|avan[çc]ad)[^\n]{0,30}ingl[eê]s/i },
        { id: "dados", rotulo: "Python, SQL e Power BI avançado", regex: /python|\bSQL\b|power\s*bi/i },
        { id: "pos", rotulo: "Pós-graduação/MBA ou certificações (CPA, CIA)", regex: /\bMBA\b|p[oó]s[-\s]?gradua[çc]|especializa[çc][aã]o|\bCPA\b|\bCIA\b/i },
      ],
    },
  },

  "programas-entrada": {
    nome: "Programas de Entrada",
    cargoEmail: "Jovem Aprendiz / Estagiário(a)",
    cargos: "Jovem Aprendiz, Estagiário",
    icone: "foguete",
    destaque:
      "Destaque no currículo: projetos acadêmicos, voluntariado, intercâmbio e paixão pelo setor aéreo.",
    criterios: {
      base: [
        { id: "estudando", rotulo: "Graduação em andamento ou ensino médio (para Aprendiz)", regex: /cursando|em\s+andamento|ensino\s+m[eé]dio|gradua[çc][aã]o|estudante/i },
        { id: "office", rotulo: "Office básico", regex: /office|word|excel|powerpoint|inform[aá]tica/i },
        { id: "equipe", rotulo: "Boa comunicação e trabalho em equipe", regex: /comunica[çc][aã]o|trabalho\s+em\s+equipe|colabora[çc][aã]o/i },
      ],
      medio: [
        { id: "publica", rotulo: "Ensino médio em escola pública (Aprendiz)", regex: /escola\s+p[uú]blica|rede\s+p[uú]blica/i },
        { id: "voluntariado", rotulo: "Voluntariado ou projetos sociais", regex: /volunt[aá]ri|projeto\s+social|\bONG\b/i },
        { id: "assiduidade", rotulo: "Assiduidade e foco no aprendizado", regex: /assiduidade|pontualidade|dedica[çc][aã]o|aprendizado/i },
        { id: "aereo", rotulo: "Interesse demonstrado pelo setor aéreo", regex: /avia[çc][aã]o|a[eé]re[oa]|aeron[aá]utic|aeroporto/i },
      ],
      elite: [
        { id: "curso", rotulo: "Cursando Engenharia, Computação, Estatística ou Economia (4º semestre+)", regex: /(engenharia|computa[çc][aã]o|estat[ií]stica|economia|sistemas\s+de\s+informa[çc][aã]o|ci[eê]ncia\s+de\s+dados)/i },
        { id: "ingles", rotulo: "Inglês avançado", regex: /ingl[eê]s[^\n]{0,30}(fluente|avan[çc]ad)|(fluente|avan[çc]ad)[^\n]{0,30}ingl[eê]s/i },
        { id: "programacao", rotulo: "Lógica de programação ou modelagem de dados", regex: /programa[çc][aã]o|python|\bSQL\b|\bjava\b|modelagem\s+de\s+dados|power\s*bi/i },
        { id: "extracurricular", rotulo: "Empresa júnior, competições acadêmicas ou iniciação científica", regex: /empresa\s+j[uú]nior|inicia[çc][aã]o\s+cient[ií]fica|competi[çc][aã]o|olimp[ií]ada|maratona/i },
      ],
    },
  },
};
