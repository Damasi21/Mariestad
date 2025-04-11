document.addEventListener('DOMContentLoaded', function () {
    if (document.body.dataset.contatoSalvo === 'true') {
      exibirModalSucesso('Contato salvo com sucesso!');
    }
  });
  
  function editarContato(botao) {
    confirmarAcao('Deseja realmente editar este contato?', () => {
      document.getElementById('id_contato_id').value = botao.dataset.id;
      document.getElementById('id_nome').value = botao.dataset.nome;
      document.getElementById('id_cargo').value = botao.dataset.cargo;
      document.getElementById('id_telefone1').value = botao.dataset.telefone1;
      document.getElementById('id_telefone2').value = botao.dataset.telefone2;
      document.getElementById('id_email').value = botao.dataset.email;
      document.getElementById('id_observacoes').value = botao.dataset.observacoes;
    });
  }
  
  
  function confirmarSalvar() {
    confirmarAcao('Deseja salvar este contato?', () => {
      document.querySelector('form').submit();
    }, 'success');
  }
  
  function confirmarExclusaoContato(id) {
    confirmarAcao('Deseja realmente excluir este contato?', () => {
      window.location.href = `/contatos/excluir/${id}/`;
    }, 'danger');
  }
  
  // Busca por coluna (índice)
  function filtrarTabela(input, colunaIndex) {
    const filtro = input.value.toLowerCase();
    const linhas = document.querySelectorAll('table tbody tr');
  
    linhas.forEach(row => {
      const celulas = row.querySelectorAll('td');
      const texto = celulas[colunaIndex]?.innerText.toLowerCase() || '';
      row.style.display = texto.includes(filtro) ? '' : 'none';
    });
  }
  