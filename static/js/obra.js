// Ao carregar a página
document.addEventListener('DOMContentLoaded', function () {
  if (document.body.dataset.obraSalva === 'true') {
    exibirModalSucesso('Obra salva com sucesso!');
  }

  const selectTags = document.getElementById('id_tags');
  if (selectTags) {
    $(selectTags).select2({
      placeholder: "Selecione as tags",
      width: '100%',
      allowClear: true
    });
  }

  const btnConfirmar = document.getElementById('btnConfirmarExclusaoAnexo');
  if (btnConfirmar) {
    btnConfirmar.addEventListener('click', function () {
      if (!urlParaExcluir) return;

      fetch('/obras/excluir-anexo/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ url: urlParaExcluir })
      })
      .then(res => res.json())
      .then(data => {
        if (data.status === 'ok') {
          const obraId = sessionStorage.getItem('obraIdSelecionada');
          carregarAnexos(obraId);
        } else {
          alert("Erro ao excluir o anexo.");
        }
      })
      .catch(() => alert("Erro na comunicação com o servidor."));

      const modal = bootstrap.Modal.getInstance(document.getElementById('modalConfirmarExclusaoAnexo'));
      modal.hide();
      urlParaExcluir = null;
    });
  }
});

// Confirma o envio do formulário
function confirmarSalvar() {
  confirmarAcao('Deseja salvar esta obra?', () => {
    document.querySelector('form').submit();
  }, 'success');
}

// Confirma a exclusão de uma obra
function confirmarExclusaoObra(id) {
  confirmarAcao('Deseja excluir esta obra?', () => {
    window.location.href = `/obras/excluir/${id}/`;
  }, 'danger');
}

// Preenche o formulário ao clicar em "Editar"
function editarObra(botao) {
  confirmarAcao('Deseja editar esta obra?', () => {
    document.getElementById('id_obra_id').value = botao.dataset.id;
    document.getElementById('id_nome').value = botao.dataset.nome;
    document.getElementById('id_endereco').value = botao.dataset.endereco;
    document.getElementById('id_data_inicio').value = botao.dataset.datainicio;
    document.getElementById('id_data_termino').value = botao.dataset.datatermino;
    document.getElementById('id_cidade').value = botao.dataset.cidade;
    document.getElementById('id_estado').value = botao.dataset.estado;
    document.getElementById('id_status').value = botao.dataset.status;
    document.getElementById('id_observacoes_obra').value = botao.dataset.observacoesObra || '';




    // Limpa os responsáveis antes de recarregar
    const container = document.getElementById('responsaveis-container');
    container.innerHTML = '';

    const responsaveisStr = botao.dataset.responsaveis || '';
    const idsResponsaveis = responsaveisStr.split(',').map(s => s.trim()).filter(s => s);

    // Para cada ID, buscamos o cliente no array
    idsResponsaveis.forEach(id => {
      const cliente = clientesDisponiveis.find(c => c.id == id);
      if (cliente) {
        adicionarResponsavel(cliente);
      } else {
        console.warn(`Cliente com ID ${id} não encontrado na lista.`);
      }
    });

    if (botao.dataset.tags) {
      $('#id_tags').val(botao.dataset.tags.split(',')).trigger('change');
    }
  });
}


// Filtra tabela da listagem por coluna
function filtrarTabela(input, colunaIndex) {
  const filtro = input.value.toLowerCase();
  const linhas = document.querySelectorAll('table tbody tr');

  linhas.forEach(row => {
    const celulas = row.querySelectorAll('td');
    const texto = celulas[colunaIndex]?.innerText.toLowerCase() || '';
    row.style.display = texto.includes(filtro) ? '' : 'none';
  });
}

// ------------------------ ANEXOS ------------------------

function abrirModalInserirAnexos() {
  const lista = document.getElementById('lista-anexos');
  lista.innerHTML = '';

  const existingFiles = document.querySelectorAll('#lista-anexos li');
  if (existingFiles.length === 0) {
    lista.innerHTML = '<li class="list-group-item">Nenhum anexo encontrado.</li>';
  }

  const inputOriginal = document.getElementById('id_arquivo');
  const inputModal = document.getElementById('id_arquivo_modal');

  inputModal.addEventListener('change', function () {
    inputOriginal.files = inputModal.files;
  });

  new bootstrap.Modal(document.getElementById('modalAnexos')).show();
}

function salvarAnexos() {
  const input = document.getElementById('id_arquivo_modal');
  const arquivos = input.files;
  const obraId = sessionStorage.getItem('obraIdSelecionada');

  if (!obraId || arquivos.length === 0) {
    alert("Selecione pelo menos um arquivo.");
    return;
  }

  const formData = new FormData();
  formData.append('obra_id', obraId);
  for (let i = 0; i < arquivos.length; i++) {
    formData.append('arquivo', arquivos[i]);
  }

  fetch('/obras/anexar/', {
    method: 'POST',
    headers: {
      'X-CSRFToken': getCookie('csrftoken')
    },
    body: formData
  })
  .then(response => response.json())
  .then(data => {
    if (data.status === 'ok') {
      input.value = '';
      carregarAnexos(obraId);
    } else {
      alert("Erro ao salvar os arquivos.");
    }
  })
  .catch(error => {
    console.error("Erro:", error);
    alert("Erro ao salvar os arquivos.");
  });
}

function carregarAnexos(obraId) {
  fetch(`/obras/listar-anexos/${obraId}/`)
    .then(res => res.json())
    .then(data => {
      const lista = document.getElementById('lista-anexos');
      lista.innerHTML = '';

      if (data.anexos.length === 0) {
        lista.innerHTML = '<li class="list-group-item">Nenhum anexo encontrado.</li>';
        return;
      }

      data.anexos.forEach(url => {
        const li = document.createElement('li');
        li.classList.add('list-group-item');
        const nome = decodeURIComponent(url.split('/').pop());
        li.innerHTML = `
          <div class="d-flex justify-content-between align-items-center w-100">
            <a href="${url}" target="_blank">${nome}</a>
            <button class="btn btn-sm btn-outline-danger ms-2" onclick="confirmarExclusaoAnexo('${url}')">&times;</button>
          </div>
        `;
        lista.appendChild(li);
      });
    });
}

function abrirModalAnexos(botao) {
  const obraId = botao.dataset.id;
  sessionStorage.setItem('obraIdSelecionada', obraId);
  carregarAnexos(obraId);

  new bootstrap.Modal(document.getElementById('modalAnexos')).show();
}

let urlParaExcluir = null;

function confirmarExclusaoAnexo(url) {
  urlParaExcluir = url;
  const modal = new bootstrap.Modal(document.getElementById('modalConfirmarExclusaoAnexo'));
  modal.show();
}

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// RESPONSAVEIS -------------------------------------
// --------------------- NOVA BUSCA DE RESPONSÁVEIS ---------------------

window.filtrarClientes = function () {
  const termo = document.getElementById('buscaCliente').value.toLowerCase().trim();
  const container = document.getElementById('listaClientesResultado');
  container.innerHTML = '';

  if (!termo) {
    container.innerHTML = '<div class="text-muted p-2">Digite parte do nome para buscar.</div>';
    return;
  }

  const resultados = clientesDisponiveis.filter(c => c.nome.toLowerCase().includes(termo));

  if (resultados.length === 0) {
    container.innerHTML = '<div class="text-danger p-2">Nenhum cliente encontrado.</div>';
    return;
  }

  resultados.forEach(cliente => {
    const item = document.createElement('div');
    item.className = 'list-group-item list-group-item-action';
    item.innerHTML = `<strong>${cliente.nome}</strong><br><small>${cliente.tag}</small>`;
    item.ondblclick = () => adicionarResponsavel(cliente);
    container.appendChild(item);
  });
};

function adicionarResponsavel(cliente) {
  const container = document.getElementById("responsaveis-container");

  if (document.getElementById(`responsavel-${cliente.id}`)) {
    alert("Este cliente já foi adicionado.");
    return;
  }

  const div = document.createElement("div");
  div.classList.add("d-flex", "align-items-center", "mb-2");
  div.id = `responsavel-${cliente.id}`;

  div.innerHTML = `
    <div class="flex-grow-1 p-2 border rounded bg-light me-2">
      <strong>${cliente.nome}</strong><br><small>${cliente.tag}</small>
    </div>
    <button type="button" class="btn btn-outline-danger btn-sm" onclick="removerResponsavel(${cliente.id})">&times;</button>
    <input type="hidden" name="responsaveis" value="${cliente.id}">
  `;

  container.appendChild(div);
  document.getElementById('buscaCliente').value = '';
  document.getElementById('listaClientesResultado').innerHTML = '';
}

window.removerResponsavel = function (id) {
  const div = document.getElementById(`responsavel-${id}`);
  if (div) div.remove();
};
