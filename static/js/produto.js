document.addEventListener('DOMContentLoaded', function () {
  const fotoInput = document.getElementById('id_foto');
  const preview = document.getElementById('previewImage');

  if (fotoInput && preview) {
    fotoInput.addEventListener('change', function (event) {
      const file = event.target.files[0];
      if (file && file.type.startsWith('image/')) {
        const reader = new FileReader();
        reader.onload = function (e) {
          preview.setAttribute('src', e.target.result);
        };
        reader.readAsDataURL(file);
      } else {
        preview.setAttribute('src', 'https://via.placeholder.com/150x200');
      }
    });
  }

  // Mensagens de sucesso
  if (document.body.dataset.salvo === 'true') {
    exibirModalSucesso('Produto salvo com sucesso!');
  }
  if (document.body.dataset.excluido === 'true') {
    exibirModalSucesso('Produto excluído com sucesso!');
  }
});

// Preenche o formulário com dados do produto
function preencherFormulario(id, codigo, descricao, ncm, unidade, familia, preco, observacoes, fotoUrl = null) {
  document.getElementById('id_produto_id').value = id;
  document.getElementById('id_codigo').value = codigo;
  document.getElementById('id_descricao').value = descricao;
  document.getElementById('id_ncm').value = ncm;
  document.getElementById('id_unidade').value = unidade;
  document.getElementById('id_familia').value = familia;
  document.getElementById('id_preco').value = preco;
  document.getElementById('id_observacoes').value = observacoes;

  const preview = document.getElementById('previewImage');
  if (preview) {
    if (fotoUrl) {
      preview.src = fotoUrl;
    } else {
      preview.src = "https://via.placeholder.com/150x200";
    }
  }
}

function editarComConfirmacao(botao) {
  const id = botao.dataset.id;
  const codigo = botao.dataset.codigo;
  const descricao = botao.dataset.descricao;
  const ncm = botao.dataset.ncm;
  const unidade = botao.dataset.unidade;
  const familia = botao.dataset.familia;
  const preco = botao.dataset.preco;
  const observacoes = botao.dataset.observacoes;
  const foto = botao.dataset.foto;

  confirmarAcao('Pretende editar esse registro?', () => {
    preencherFormulario(id, codigo, descricao, ncm, unidade, familia, preco, observacoes, foto);
  });
}

function confirmarExclusao(produtoId) {
  confirmarAcao('Deseja realmente excluir este produto?', () => {
    window.location.href = `/produtos/excluir/${produtoId}/`;
  }, 'danger');
}

function confirmarSalvar() {
  confirmarAcao('Deseja salvar este registro?', () => {
    document.querySelector('form').submit();
  }, 'success');
}
// FILTRAR PRODUTOS 

function filtrarTabela(input) {
  const filtro = input.value.toLowerCase();
  const tabela = document.querySelector('table.table');

  if (!tabela) return;

  const linhas = tabela.querySelectorAll('tbody tr');

  linhas.forEach(row => {
    const texto = row.innerText.toLowerCase();
    row.style.display = texto.includes(filtro) ? '' : 'none';
  });
}


