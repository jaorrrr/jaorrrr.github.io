/**
 * Configuração do portal (versão demonstração estática).
 *
 * SEGURANÇA — LIMITAÇÃO DA HOSPEDAGEM ESTÁTICA:
 * Em produção, o e-mail do avaliador deve ficar em variável de ambiente no
 * BACKEND e a autorização deve ser validada no servidor (a especificação do
 * projeto exige isso). O GitHub Pages não executa código de servidor, então
 * esta demonstração guarda apenas o hash SHA-256 do e-mail autorizado —
 * o endereço não aparece em texto claro no código, mas isso é ofuscação,
 * não segurança real. Veja o README para o desenho do backend definitivo.
 */
window.CONFIG = {
  // sha256 do e-mail autorizado do avaliador
  HASH_EMAIL_AVALIADOR:
    "23293d2db263d674b28206caf2126569924a5843bfd572758a1dc1558386a0e5",

  // nota mínima para aparecer na lista do avaliador
  NOTA_CORTE: 7,

  // chaves de armazenamento local
  CHAVE_CANDIDATOS: "azul_demo_candidatos",
  CHAVE_CANDIDATURAS: "azul_demo_candidaturas",
  CHAVE_ENTREVISTAS: "azul_demo_entrevistas",
  CHAVE_SESSAO_AVALIADOR: "azul_demo_sessao_avaliador",

  AVISO_LEGAL:
    "Este é um projeto conceitual desenvolvido para fins de estudo/portfólio, " +
    "inspirado na identidade visual da Azul Linhas Aéreas Brasileiras S.A., " +
    "sem vínculo oficial com a empresa.",
};
