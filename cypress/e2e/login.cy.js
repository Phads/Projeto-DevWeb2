describe('Teste de Login', () => {
  beforeEach(() => {
    cy.visit('http://127.0.0.1:8000/login/')
  })

  it('deve fazer login com credenciais válidas', () => {
    cy.get('#id_username').type('naruto_123')
    cy.get('#id_password').type('12345')
    cy.get('form > .btn').click()

    cy.url().should('include', '/home')
  })})