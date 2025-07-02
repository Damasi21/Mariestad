// configuracoes.js atualizado para Status, Tags, StatusCliente e Vendedores

// === FUNÇÕES DE EDIÇÃO ===
window.editarStatus = function(id, nome) {
  document.getElementById('id_status_id').value = id;
  document.getElementById('id_nome').value = nome;
};

window.editarTag = function(id, nome) {
  document.getElementById('id_tag_id').value = id;
  document.getElementById('id_nome').value = nome;
};

window.editarStatusCliente = function(id, nome) {
  document.getElementById('id_status_cliente_id').value = id;
  document.getElementById('id_nome').value = nome;
};

window.editarVendedor = function(id, nome, funcao, telefone, email) {
  document.getElementById('id_vendedor_id').value = id;
  document.getElementById('id_nome').value = nome;
  document.getElementById('id_funcao').value = funcao;
  document.getElementById('id_telefone').value = telefone;
  document.getElementById('id_email').value = email;
};

// === FUNÇÃO DE EXCLUSÃO DE VENDEDOR ===
window.confirmarExclusaoVendedor = function(id) {
  confirmarAcao("Deseja excluir este vendedor?", () => {
    window.location.href = `/configuracoes/vendedores/excluir/${id}/`;
  }, 'danger');
};

// === FILTRO DE TABELA ===
window.filtrarTabela = function(input) {
  const filtro = input.value.toLowerCase();
  const linhas = input.closest('div.container').querySelectorAll('table tbody tr');

  linhas.forEach(row => {
    const texto = row.innerText.toLowerCase();
    row.style.display = texto.includes(filtro) ? '' : 'none';
  });
};

// === MODAL DE CONFIRMAÇÃO REUTILIZÁVEL ===
function confirmarAcao(mensagem, callback, cor = 'warning') {
  const modal = new bootstrap.Modal(document.getElementById('modalConfirmacao'));
  const texto = document.getElementById('modalMensagemConfirmacao');
  const header = document.getElementById('modalHeaderConfirmacao');
  const botao = document.getElementById('btnConfirmarAcao');

  texto.textContent = mensagem;

  header.classList.remove('bg-success', 'bg-danger', 'bg-warning');
  header.classList.add(`bg-${cor}`);

  botao.className = `btn btn-${cor}`;
  botao.onclick = () => {
    modal.hide();
    callback();
  };

  modal.show();
}

// === FUNÇÕES DE CONFIRMAÇÃO DE CADA ENTIDADE ===
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


document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('.btn-editar').forEach(botao => {
    botao.addEventListener('click', () => {
      const id = botao.dataset.id;
      const nome = botao.dataset.nome;
      const funcao = botao.dataset.funcao;
      const telefone = botao.dataset.telefone;
      const email = botao.dataset.email;
      window.editarVendedor(id, nome, funcao, telefone, email);
    });
  });


  document.querySelectorAll('.btn-excluir').forEach(botao => {
    botao.addEventListener('click', () => {
      const id = botao.dataset.id;
      window.confirmarExclusaoVendedor(id); // ✅ agora sim
    });
  });
});
