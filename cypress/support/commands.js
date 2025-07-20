Cypress.Commands.add('login', (username, password) => {
  cy.visit('http://127.0.0.1:8000/login/')
  cy.get('#id_username').type(username)
  cy.get('#id_password').type(password)
  cy.get('form > .btn').click()
  cy.url().should('include', '/home');
})