describe('Excluir tarefa existente', () => {
  beforeEach(() => {
    cy.login('sasuke_123', '12345')
  })

  it('Deve excluir a primeira tarefa da lista', () => {
    cy.visit('http://127.0.0.1:8000/home')
    cy.get('table tbody tr', { timeout: 10000 }).should('have.length.greaterThan', 0)
      cy.get('table tbody tr:first-child td:nth-child(2)').then(($td) => {
      const tituloTarefa = $td.text().trim()
      cy.get(':nth-child(1) > :nth-child(6) > .btn-danger').click()
      cy.contains('button', 'Excluir').click()

      cy.contains(tituloTarefa).should('not.exist')
    })
  })
})
