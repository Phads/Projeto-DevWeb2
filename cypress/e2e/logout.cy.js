describe('Teste de Logout', () => { 
  
  beforeEach(() => {
    cy.login('sasuke_123', '12345'); 
    cy.url().should('include', '/home'); 
    cy.get('.d-flex > .btn').contains('Logout').should('be.visible'); 
  });
    it('deve fazer logout com sucesso e redirecionar para a página de login', () => {
    cy.log('Tentando fazer logout...');
    cy.get('.d-flex > .btn').contains('Logout').click(); 

    cy.log('Verificando redirecionamento para a página de login.');
    cy.url().should('include', '/login'); 
    cy.get('#id_username').should('be.visible'); 
    cy.get('#id_password').should('be.visible'); 
    cy.contains('h2', 'Lista de Tarefas').should('not.exist');
    cy.contains('projeto final').should('not.exist');

    cy.log('Logout realizado com sucesso e verificado.');
  });
});