// configuracoes.js atualizado para telas separadas de Status, Tags e StatusCliente

document.addEventListener('DOMContentLoaded', function () {

  // EDITAR STATUS
  window.editarStatus = function (id, nome) {
    document.getElementById('id_status_id').value = id;
    document.getElementById('id_nome').value = nome;
  };

  // EDITAR TAG
  window.editarTag = function (id, nome) {
    document.getElementById('id_tag_id').value = id;
    document.getElementById('id_nome').value = nome;
  };

  // EDITAR STATUS CLIENTE
  window.editarStatusCliente = function (id, nome) {
    document.getElementById('id_status_cliente_id').value = id;
    document.getElementById('id_nome').value = nome;
  };
});

// Filtro por coluna reutilizável
function filtrarTabela(input) {
  const filtro = input.value.toLowerCase();
  const linhas = input.closest('div.container').querySelectorAll('table tbody tr');

  linhas.forEach(row => {
    const texto = row.innerText.toLowerCase();
    row.style.display = texto.includes(filtro) ? '' : 'none';
  });
}


function confirmarAcao(mensagem, callback, cor = 'warning') {
  const modal = new bootstrap.Modal(document.getElementById('modalConfirmacao'));
  const texto = document.getElementById('modalMensagemConfirmacao');  // <- corrigido aqui
  const header = document.getElementById('modalHeaderConfirmacao');  // <- para cor
  const botao = document.getElementById('btnConfirmarAcao');

  texto.textContent = mensagem;

  // Define cor do header dinamicamente
  header.classList.remove('bg-success', 'bg-danger', 'bg-warning');
  header.classList.add(`bg-${cor}`);

  // Cor do botão
  botao.className = `btn btn-${cor}`;
  botao.onclick = () => {
    modal.hide();
    callback();
  };

  modal.show();
}


function confirmarSalvarStatus() {
  confirmarAcao("Deseja realmente salvar/editar este status?", () => {
    document.querySelector('form').submit();
  }, 'success');
}

function confirmarExclusaoStatus(id) {
  confirmarAcao("Deseja excluir este status?", () => {
    window.location.href = `/status-obra/excluir/${id}/`;
  }, 'danger');
}

function confirmarSalvarTag() {
  confirmarAcao("Deseja realmente salvar/editar esta tag?", () => {
    document.querySelector('form').submit();
  }, 'success');
}

function confirmarExclusaoTag(id) {
  confirmarAcao("Deseja excluir esta tag?", () => {
    window.location.href = `/tags/excluir/${id}/`;
  }, 'danger');
}


function confirmarSalvarStatusCliente() {
  confirmarAcao("Deseja realmente salvar/editar este status de cliente?", () => {
    document.querySelector('form').submit();
  }, 'success');
}


function confirmarExclusaoStatusCliente(id) {
  confirmarAcao("Deseja excluir este status de cliente?", () => {
    window.location.href = `/status-cliente/excluir/${id}/`;
  }, 'danger');
}


