document.addEventListener('DOMContentLoaded', function () {
    const statusForm = document.querySelector('form');
    const tagForm = document.querySelectorAll('form')[1];
    const statusClienteForm = document.querySelectorAll('form')[2];  // terceiro formulário da tela
  
    if (document.body.dataset.statusSalvo === 'true') {
      exibirModalSucesso('Status salvo com sucesso!');
    }
    if (document.body.dataset.tagSalvo === 'true') {
      exibirModalSucesso('Tag salva com sucesso!');
    }

    if (document.body.dataset.statusClienteSalvo === 'true') {
      exibirModalSucesso('Status de Cliente salvo com sucesso!');
    }
  
    window.editarStatus = function (botao) {
      document.getElementById('id_status_id').value = botao.dataset.id;
      document.getElementById('id_nome').value = botao.dataset.nome;
    };
  
    window.editarTag = function (botao) {
      document.getElementById('id_tag_id').value = botao.dataset.id;
      document.getElementById('id_nome').value = botao.dataset.nome;
    };

    window.editarStatusCliente = function (botao) {
      document.getElementById("id_status_cliente_id").value = botao.dataset.id;
      document.getElementById("id_nome_cliente").value = botao.dataset.nome;
    }
  
    window.confirmarSalvarStatus = function () {
      confirmarAcao('Deseja salvar o status?', () => {
        statusForm.submit();
      }, 'success');
    };
  
    window.confirmarSalvarTag = function () {
      confirmarAcao('Deseja salvar a tag?', () => {
        tagForm.submit();
      }, 'success');
    };

    window.confirmarSalvarStatusCliente = function () {
      confirmarAcao('Deseja salvar o status de cliente?', () => {
        statusClienteForm.submit();
      }, 'success');
    };
  
    window.confirmarExclusaoStatus = function (id) {
      confirmarAcao('Deseja excluir este status?', () => {
        window.location.href = `/status/excluir/${id}/`;
      }, 'danger');
    };
  

    window.confirmarExclusaoTag = function (id) {
      confirmarAcao('Deseja excluir esta tag?', () => {
        window.location.href = `/tags/excluir/${id}/`;
      }, 'danger');
    };

    window.confirmarExclusaoStatusCliente = function (id) {
      confirmarAcao('Deseja excluir este status de cliente?', () => {
        window.location.href = `/status-cliente/excluir/${id}/`;
      }, 'danger');
    };

  });
  // ------------------------------------------------------------------------------

    // BUSCA DE TAGS E STATUS 
    
  function filtrarTabela(input) {
    const filtro = input.value.toLowerCase();
    const linhas = input.closest('div.card').querySelectorAll('table tbody tr');
  
    linhas.forEach(row => {
      const texto = row.innerText.toLowerCase();
      row.style.display = texto.includes(filtro) ? '' : 'none';
    });
  }
  
  // ------------------------------------------------------------------------------

