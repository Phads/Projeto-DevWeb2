describe('Registro de usuário com dados inválidos', () => {
  it('Deve mostrar erro com e-mail inválido', () => {
    cy.visit('http://127.0.0.1:8000/registro/')
    
    cy.get('#id_username').type('fernando_123')
    cy.get('#id_first_name').type('Fernando')
    cy.get('#id_email').type('a@a') // e-mail inválido
    cy.get('#id_password').type('12345')
    cy.get('#id_password2').type('12345')
    
    cy.get('form > .btn').click()

    cy.get('#id_email')
    .parent()
    .should('contain', 'Informe um endereço de email válido')

  })
})
