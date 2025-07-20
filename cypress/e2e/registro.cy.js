describe('registro', () => {
  it('Deve se registrar com dados válidos', () => {
    cy.visit('http://127.0.0.1:8000/registro/')
    cy.get('#id_username').type('sakura_123')
    cy.get('#id_first_name').type('sakura')
    cy.get('#id_email').type('sakura@gmail.com')
    cy.get('#id_password').type('12345')
    cy.get('#id_password2').type('12345')
    cy.get('form > .btn').click()

    cy.url().should('include', '/home');
  })
})