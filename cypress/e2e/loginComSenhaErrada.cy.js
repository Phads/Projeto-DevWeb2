describe('Teste de Login Com Senha Errada ', () => {
  beforeEach(() => {
    cy.visit('http://127.0.0.1:8000/login/')
  })

  it('deve fazer login com credenciais inválidas', () => {
    cy.get('#id_username').type('sasuke_123')
    cy.get('#id_password').type('789234')
    cy.get('form > .btn').click()
    cy.get('.m-0 > li').should('contain', 'Por favor, entre com um usuário')
  })})
