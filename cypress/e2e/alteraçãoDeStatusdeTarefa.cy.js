// cypress/e2e/alteracaoDeStatusTarefa.cy.js

import tarefasPage from '../pages/tarefasPage'; // Importa o Page Object da página de tarefas
// Importar edicaoTarefaPage se o beforeEach precisar criar a tarefa via formulário
import edicaoTarefaPage from '../pages/edicaoTarefaPage';


describe('Alteração de Status de Tarefa para "Concluído"', () => {

  const TITULO_TAREFA_PARA_STATUS = 'Tarefa para Concluir';
  const DATA_ENTREGA_PARA_STATUS = '26/07/2025';
  const DESCRICAO_PARA_STATUS = 'Esta tarefa será concluída no teste de status.';

  beforeEach(() => {
    // 1. Login
    cy.login('sasuke_123', '12345'); // O cy.login já garante que a home está carregada e a API respondida.

    // 2. Garantir que a tarefa para ser concluída esteja em um estado limpo (não concluída)
    cy.log(`Preparando a tarefa "${TITULO_TAREFA_PARA_STATUS}" para o teste de status.`);

    // Tenta encontrar e excluir a tarefa se ela já existe (para evitar duplicidade ou estado sujo)
    tarefasPage.getLinhaTarefa(TITULO_TAREFA_PARA_STATUS).then($el => {
      if ($el.length > 0) {
        tarefasPage.clicarBotaoExcluir(TITULO_TAREFA_PARA_STATUS);
        cy.contains('Tarefa excluída com sucesso!').should('be.visible'); // AJUSTE AQUI: Mensagem de sucesso real
        cy.log(`Tarefa "${TITULO_TAREFA_PARA_STATUS}" excluída para limpeza.`);
      }
    }).catch(() => {
      cy.log(`Tarefa "${TITULO_TAREFA_PARA_STATUS}" não encontrada para exclusão. Prosseguindo.`);
    });

    // 3. Cria a tarefa que será concluída neste teste
    cy.log(`Criando a tarefa original para alteração de status: "${TITULO_TAREFA_PARA_STATUS}"`);
    tarefasPage.clicarBotaoCriarNovaTarefa();
    cy.url().should('include', '/create');

    edicaoTarefaPage.preencherFormulario(TITULO_TAREFA_PARA_STATUS, DATA_ENTREGA_PARA_STATUS, DESCRICAO_PARA_STATUS);
    edicaoTarefaPage.salvarTarefa();

    cy.url().should('include', '/home');
    tarefasPage.getLinhaTarefa(TITULO_TAREFA_PARA_STATUS).should('be.visible'); // Confirma que a tarefa foi criada
    cy.log(`Tarefa "${TITULO_TAREFA_PARA_STATUS}" criada e visível na lista.`);
  });

  it('deve alterar o status da tarefa para "Concluído"', () => {
    cy.log(`Iniciando o teste para concluir a tarefa "${TITULO_TAREFA_PARA_STATUS}".`);

    // Clica no botão "Concluir" da tarefa
    tarefasPage.clicarBotaoConcluir(TITULO_TAREFA_PARA_STATUS);
    cy.log('Clicou no botão "Concluir".');

    // **VERIFICAÇÃO PÓS-ALTERAÇÃO DE STATUS (ASSERÇÕES CRUCIAIS AQUI!)**
    // Verifica se o status da tarefa foi alterado na lista.
    cy.log('Verificando se o status da tarefa foi alterado para "Concluído".');
    tarefasPage.getLinhaTarefa(TITULO_TAREFA_PARA_STATUS)
      .should('exist') // Garante que a linha da tarefa ainda existe
      .within(() => {
        // AJUSTE AQUI: Como sua UI indica que a tarefa foi concluída?
        // Na sua imagem, a coluna "Finalização" mostra "None".
        // Após concluir, ela deve mudar para algo como "Concluído", "Sim", um ícone, etc.
        // Se o texto na coluna "Finalização" muda para "Concluído":
        cy.contains('td', 'Concluído').should('be.visible'); // Verifica se há um <td> com o texto "Concluído"
        // OU, se a coluna finalização tem um ID ou classe específica:
        // cy.get('td.coluna-finalizacao').should('contain', 'Concluído');

        // Opcional: Verificar se o botão "Concluir" desapareceu ou foi desabilitado
        cy.get(':nth-child(6) > .btn-primary').contains('Concluir').should('not.exist'); // Ou .should('be.disabled')
      });

    cy.log('Teste de alteração de status da tarefa concluído com sucesso.');
  });
});