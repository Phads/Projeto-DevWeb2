describe('Testes Negativos de Exclusão de Tarefa', () => {
  beforeEach(() => {
    // 1. Logar no sistema
    cy.login('sasuke_123', '12345'); // Use suas credenciais válidas
    cy.url().should('include', '/home'); // Confirma que o login foi bem-sucedido
  });

  // --- Cenário 1: Cancelar a Exclusão ---
  it('não deve excluir a tarefa se o usuário cancelar a ação', () => {
    cy.get(':nth-child(1) > :nth-child(6) > .btn-danger').click()
    cy.get('.container > form > .btn-danger').click()

  });

});