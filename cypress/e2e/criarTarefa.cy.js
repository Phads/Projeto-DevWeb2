describe('Criar tarefa', () => {
  beforeEach(() => {
    cy.login('naruto_123', '12345')
  })

  it('cria uma nova tarefa', () => {
    cy.get('.container > .btn').click()
    cy.url().should('include', '/create')

    cy.get('#id_titulo').type('projeto de testes')
    cy.get('#id_data_entrega').type('23/07/2025')
    cy.get('#id_descricao').type('realizar planejamento, testes unitarios e automatizados')
    cy.get('.btn-primary').click()

    cy.url().should('include', '/home')
  })
})