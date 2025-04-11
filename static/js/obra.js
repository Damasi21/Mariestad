document.addEventListener('DOMContentLoaded', function () {
    if (document.body.dataset.obraSalva === 'true') {
      exibirModalSucesso('Obra salva com sucesso!');
    }
  
    // Ativa Select2 no campo de tags
    const selectTags = document.getElementById('id_tags');
    if (selectTags) {
      $(selectTags).select2({
        placeholder: "Selecione as tags",
        width: '100%',
        allowClear: true
      });
    }
  });

  function adicionarResponsavel(valorSelecionado = null) {
    const container = document.getElementById('responsaveis-container');
    const grupo = document.createElement('div');
    grupo.classList.add('input-group', 'mb-2');
  
    const select = document.createElement('select');
    select.name = 'responsaveis';
    select.classList.add('form-select');
  
    const original = document.querySelector('select[name=responsaveis]');
    if (original) {
      original.querySelectorAll('option').forEach(opt => {
        const clone = opt.cloneNode(true);
        if (valorSelecionado && clone.value === valorSelecionado) {
          clone.selected = true;
        }
        select.appendChild(clone);
      });
    }
  
    const btnRemover = document.createElement('button');
    btnRemover.type = 'button';
    btnRemover.classList.add('btn', 'btn-outline-danger');
    btnRemover.textContent = '-';
    btnRemover.onclick = () => grupo.remove();
  
    grupo.appendChild(select);
    grupo.appendChild(btnRemover);
    container.appendChild(grupo);
  }


  function confirmarSalvar() {
    confirmarAcao('Deseja salvar esta obra?', () => {
      document.querySelector('form').submit();
    }, 'success');
  }
  
  function confirmarExclusaoObra(id) {
    confirmarAcao('Deseja excluir esta obra?', () => {
      window.location.href = `/obras/excluir/${id}/`;
    }, 'danger');
  }
  
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
  
      const container = document.getElementById('responsaveis-container');
      container.innerHTML = '';
  
      const responsaveisStr = botao.dataset.responsaveis || '';
      const idsResponsaveis = responsaveisStr.split(',').map(s => s.trim()).filter(s => s);
      idsResponsaveis.forEach(id => adicionarResponsavel(id));
  
      if (botao.dataset.tags) {
        $('#id_tags').val(botao.dataset.tags.split(',')).trigger('change');
      }
    });
  }
  
  function filtrarTabela(input, colunaIndex) {
    const filtro = input.value.toLowerCase();
    const linhas = document.querySelectorAll('table tbody tr');
  
    linhas.forEach(row => {
      const celulas = row.querySelectorAll('td');
      const texto = celulas[colunaIndex]?.innerText.toLowerCase() || '';
      row.style.display = texto.includes(filtro) ? '' : 'none';
    });
  }

// JS DO CAMPO DE ANEXO (OBRAS)
function abrirModalInserirAnexos() {
  const lista = document.getElementById('lista-anexos');
  lista.innerHTML = '';

  // Lista os arquivos que já estão visíveis (do formulário anterior)
  const existingFiles = document.querySelectorAll('#lista-anexos li');
  if (existingFiles.length === 0) {
    lista.innerHTML = '<li class="list-group-item">Nenhum anexo encontrado.</li>';
  }

  // Copia arquivos selecionados do input principal (caso tenha algum carregado)
  const inputOriginal = document.getElementById('id_arquivo');
  const inputModal = document.getElementById('id_arquivo_modal');

  inputModal.addEventListener('change', function () {
    const files = inputModal.files;
    inputOriginal.files = inputModal.files;
  });

  new bootstrap.Modal(document.getElementById('modalAnexos')).show();
}

// SALVAR ANEXO 
function salvarAnexos() {
  const inputModal = document.getElementById('id_arquivo_modal');
  const inputForm = document.getElementById('id_arquivo');

  if (inputModal.files.length === 0) {
    alert("Selecione pelo menos um arquivo.");
    return;
  }

  // Não é possível transferir programaticamente os arquivos de um input para outro
  // Mas podemos simplesmente usar os arquivos selecionados no modal no input real
  // Então mostramos uma mensagem e fechamos o modal

  const modal = bootstrap.Modal.getInstance(document.getElementById('modalAnexos'));
  modal.hide();

  exibirModalSucesso("Arquivos anexados ao cadastro. Clique em Salvar para concluir.");
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

//----------------------------------------------------------------------------

function abrirModalAnexos(botao) {
  const obraId = botao.dataset.id;
  sessionStorage.setItem('obraIdSelecionada', obraId);
  carregarAnexos(obraId); // Agora os arquivos virão do servidor

  new bootstrap.Modal(document.getElementById('modalAnexos')).show();
}

// -------------------------------------------------------------------------------

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

      // Recarrega os anexos no modal sem fechar
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


// --------------------------------------------------------------------------
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
// ------------------------------------------------------------------------
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
            <button class="btn btn-sm btn-outline-danger ms-2" onclick="confirmarExclusaoAnexo('${url}')">
              &times;
            </button>
          </div>
        `;

        lista.appendChild(li);
      });
    });
}

// -----------------------------------------------------------------

let urlParaExcluir = null;

function confirmarExclusaoAnexo(url) {
  urlParaExcluir = url;
  const modal = new bootstrap.Modal(document.getElementById('modalConfirmarExclusaoAnexo'));
  modal.show();
}

document.addEventListener('DOMContentLoaded', function () {
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
          carregarAnexos(obraId); // Atualiza a lista no modal
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
