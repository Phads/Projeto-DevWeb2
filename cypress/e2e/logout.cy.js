describe('Teste de Logout', () => { // Este é o único "describe" de nível superior para este arquivo

  // Este bloco beforeEach é o que o Cypress vai usar para configurar o ambiente
  // para CADA teste 'it' dentro deste describe.
  beforeEach(() => {
    // Primeiro, precisamos estar logados para poder fazer logout.
    cy.login('sasuke_123', '12345'); // Usa o comando customizado de login
    cy.url().should('include', '/home'); // Confirma que estamos na home após o login
    // GARANTIR que o botão de Logout esteja visível antes de tentar clicar
    // Use o seletor que você mapeou e o texto 'Logout'
    cy.get('.d-flex > .btn').contains('Logout').should('be.visible'); // Mapeado anteriormente
  });

  // Este é o seu teste específico de logout
  it('deve fazer logout com sucesso e redirecionar para a página de login', () => {
    cy.log('Tentando fazer logout...');

    // Clica no botão de Logout usando o seletor que você mapeou e o texto.
    cy.get('.d-flex > .btn').contains('Logout').click(); // Mapeado anteriormente

    cy.log('Verificando redirecionamento para a página de login.');

    // Verifica se a URL mudou para a página de login.
    cy.url().should('include', '/login'); // Ou '/'

    // Asserções para confirmar que a sessão foi encerrada (elementos da tela de login visíveis)
    cy.get('#id_username').should('be.visible'); // Campo de usuário da tela de login
    cy.get('#id_password').should('be.visible'); // Campo de senha da tela de login

    // Opcional: Verificar se elementos da página logada não estão mais visíveis.
    cy.contains('h2', 'Lista de Tarefas').should('not.exist');
    cy.contains('projeto final').should('not.exist');

    cy.log('Logout realizado com sucesso e verificado.');
  });

  // Se você tivesse outros testes de logout (ex: "não deve fazer logout se houver erro X"), eles viriam aqui.
  // it('outro teste de logout...', () => { ... });

});