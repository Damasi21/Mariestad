// Ativa Select2 para tags e exibe modal após salvar
document.addEventListener("DOMContentLoaded", function () {
    const cnpj = document.getElementById("id_cnpj");
    const cep = document.getElementById("id_cep");
    const tel = document.getElementById("id_telefone");
  
    if (document.body.dataset.clienteSalvo === 'true') {
      exibirModalSucesso('Cliente salvo com sucesso!');
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
  
    if (cnpj) {
      cnpj.addEventListener("input", function () {
        cnpj.value = cnpj.value
          .replace(/\D/g, '')
          .replace(/^(\d{2})(\d)/, '$1.$2')
          .replace(/^(\d{2})\.(\d{3})(\d)/, '$1.$2.$3')
          .replace(/\.(\d{3})(\d)/, '.$1/$2')
          .replace(/(\d{4})(\d)/, '$1-$2')
          .slice(0, 18);
      });
    }
  
    if (cep) {
      cep.addEventListener("input", function () {
        cep.value = cep.value
          .replace(/\D/g, '')
          .replace(/^(\d{5})(\d)/, '$1-$2')
          .slice(0, 9);
      });
    }
  
    if (tel) {
      tel.addEventListener("input", function () {
        tel.value = tel.value
          .replace(/\D/g, '')
          .replace(/^(\d{2})(\d)/g, '($1) $2')
          .replace(/(\d{5})(\d{4})$/, '$1-$2')
          .slice(0, 15);
      });
    }
  });
  

  // Função chamada ao clicar em "Editar"
function editarCliente(botao) {
  document.getElementById("id_cliente_id").value = botao.dataset.id;
  document.getElementById("id_cnpj").value = botao.dataset.cnpj;
  document.getElementById("id_razao_social").value = botao.dataset.razao_social;
  document.getElementById("id_nome_fantasia").value = botao.dataset.nome_fantasia;
  document.getElementById("id_email").value = botao.dataset.email;
  document.getElementById("id_telefone").value = botao.dataset.telefone;
  document.getElementById("id_endereco").value = botao.dataset.endereco;
  document.getElementById("id_numero").value = botao.dataset.numero;
  document.getElementById("id_complemento").value = botao.dataset.complemento;
  document.getElementById("id_bairro").value = botao.dataset.bairro;
  document.getElementById("id_cep").value = botao.dataset.cep;
  document.getElementById("id_cidade").value = botao.dataset.cidade;
  document.getElementById("id_estado").value = botao.dataset.estado;
  document.getElementById("id_status").value = botao.dataset.status;
  document.getElementById("id_observacoes").value = botao.dataset.observacoes;

  if (botao.dataset.tags) {
    $('#id_tags').val(botao.dataset.tags.split(',')).trigger('change');
  }

  const abaCadastro = document.querySelector('#aba-cadastro-tab');
  if (abaCadastro) new bootstrap.Tab(abaCadastro).show();
}


  
  // Busca CNPJ via ReceitaWS
  document.getElementById("btnBuscarCNPJ")?.addEventListener("click", function () {
    const cnpj = document.getElementById("id_cnpj").value.replace(/\D/g, '');
    if (cnpj.length !== 14) {
      exibirModalErro("CNPJ inválido. Insira 14 dígitos.");
      return;
    }
  
    fetch(`/buscar_dados_empresa/?cnpj=${cnpj}`)
      .then(response => response.json())
      .then(data => {
        if (data.error) {
          exibirModalErro("Erro ao buscar CNPJ: " + data.error);
        } else {
          document.getElementById("id_razao_social").value = data.nome || "";
          document.getElementById("id_nome_fantasia").value = data.fantasia || "";
          document.getElementById("id_endereco").value = data.logradouro || "";
          document.getElementById("id_numero").value = data.numero || "";
          document.getElementById("id_complemento").value = data.complemento || "";
          document.getElementById("id_bairro").value = data.bairro || "";
          document.getElementById("id_cep").value = data.cep || "";
          document.getElementById("id_cidade").value = data.municipio || "";
          document.getElementById("id_estado").value = data.uf || "";
          document.getElementById("id_email").value = data.email || "";
          document.getElementById("id_telefone").value = data.telefone || "";
        }
      })
      .catch(() => exibirModalErro("Erro ao buscar os dados da empresa."));
  });
  
  // Confirmação visual antes de salvar
  function confirmarSalvar() {
    const razao = document.getElementById("id_razao_social").value.trim();
    const cnpj = document.getElementById("id_cnpj").value.trim();
    if (!razao || !cnpj) {
      exibirModalErro("Preencha os campos obrigatórios: CNPJ e Razão Social.");
      return;
    }
  
    confirmarAcao("Deseja salvar este cliente?", () => {
      document.getElementById("formCliente").submit();
    }, "success");
  }
  
  // Modal de erro reutilizando o modal de sucesso
  function exibirModalErro(msg) {
    const modal = new bootstrap.Modal(document.getElementById("modalSucesso"));
    const header = document.querySelector("#modalSucesso .modal-header");
    const corpo = document.getElementById("modalMensagemSucesso");
  
    header.classList.remove("bg-success");
    header.classList.add("bg-danger");
    corpo.textContent = msg;
    modal.show();
  }
  
// ---------------------------------------------------------------------------
// ABRIR MODAL CONTATOS 
 
function abrirModalContatos() {
    const clienteId = document.getElementById("id_cliente_id").value;
    if (!clienteId) {
      exibirModalErro("Você precisa salvar o cliente antes de adicionar contatos.");
      return;
    }
  
    // Define o cliente_id oculto no form do modal
    document.getElementById("contato_cliente_id").value = clienteId;
  
    // Limpa a lista
    document.getElementById("listaContatosCliente").innerHTML = "Carregando contatos...";
  
    // Requisição AJAX para listar contatos do cliente
    fetch(`/clientes/contatos/?cliente_id=${clienteId}`)
      .then(resp => resp.json())
      .then(data => {
        if (data.length === 0) {
          document.getElementById("listaContatosCliente").innerHTML = "<p>Nenhum contato encontrado.</p>";
          return;
        }
  
        const html = `
          <table class="table table-bordered table-striped mt-3">
            <thead>
              <tr>
                <th>Nome</th>
                <th>Cargo</th>
                <th>Telefone 1</th>
                <th>Email</th>
                <th class="text-center" style="width: 100px;">Ações</th>
              </tr>
            </thead>
            <tbody>
              ${data.map(contato => `
                <tr>
                  <td>${contato.nome}</td>
                  <td>${contato.cargo}</td>
                  <td>${contato.telefone1 || ''}</td>
                  <td>${contato.email || ''}</td>
                  <td class="text-center">
                    <button class="btn btn-sm btn-outline-primary me-1" onclick="carregarContato(${contato.id})">
                      <i class="bi bi-pencil"></i>
                    </button>
                    <button class="btn btn-sm btn-outline-danger" onclick="excluirContato(${contato.id})">
                      <i class="bi bi-trash"></i>
                    </button>
                  </td>
                </tr>
              `).join('')}
            </tbody>
          </table>
        `;
  
        document.getElementById("listaContatosCliente").innerHTML = html;
      })
      .catch(() => {
        document.getElementById("listaContatosCliente").innerHTML = "<p class='text-danger'>Erro ao buscar contatos.</p>";
      });
  
    const modal = new bootstrap.Modal(document.getElementById("modalContatosCliente"));
    modal.show();
  }
  
  
// Submete novo contato via AJAX
document.getElementById("formNovoContato")?.addEventListener("submit", function (e) {
  e.preventDefault();

  const form = e.target;
  const formData = new FormData(form);

  // Captura segura do token CSRF a partir do form principal
  const csrfInput = document.querySelector('#formCliente [name=csrfmiddlewaretoken]');
  const csrfToken = csrfInput ? csrfInput.value : "";

  const contatoId = document.getElementById("id_contato_id").value;
  const url = contatoId
    ? `/clientes/editar-contato/${contatoId}/`
    : "/clientes/salvar-contato/";

  fetch(url, {
    method: "POST",
    headers: {
      "X-CSRFToken": csrfToken
    },
    body: formData
  })
    .then(resp => resp.json())
    .then(data => {
      if (data.status === "ok") {
        abrirModalContatos();  // Atualiza a tabela de contatos
        form.reset();
        document.getElementById("id_contato_id").value = "";
      } else {
        exibirModalErro("Erro ao salvar contato.");
      }
    })
    .catch(() => {
      exibirModalErro("Erro inesperado ao salvar contato.");
    });
});



  // EXCLUI CONTATO DE CLIENTES 

  function excluirContato(contatoId) {
    if (!confirm("Deseja realmente excluir este contato?")) return;
  
    fetch(`/clientes/excluir-contato/${contatoId}/`, {
      method: "DELETE",
      headers: {
        "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value
      }
    })
      .then(resp => resp.json())
      .then(data => {
        if (data.status === "ok") {
          abrirModalContatos(); // Atualiza a lista automaticamente
        } else {
          exibirModalErro("Erro ao excluir contato.");
        }
      })
      .catch(() => {
        exibirModalErro("Erro ao excluir contato.");
      });
  }

  // Ao fechar o modal de contatos pelo 'X', voltar para aba de Cadastro
  document.getElementById("modalContatosCliente").addEventListener("hidden.bs.modal", function () {
    // Remove qualquer backdrop residual
    document.querySelectorAll('.modal-backdrop').forEach(el => el.remove());
    document.body.classList.remove('modal-open');
    document.body.style = '';
  
    if (document.body.dataset.resetCliente === "true") {
      limparFormularioCliente();
      document.body.dataset.resetCliente = "false";
    }
  });
  

  // EDITAR CONTATO DE CLIENTES 

  function carregarContato(id) {
    fetch(`/clientes/contato/${id}/`)
      .then(resp => resp.json())
      .then(data => {
        document.getElementById("id_contato_id").value = data.id;
        document.getElementById("contato_cliente_id").value = data.cliente_id;
        document.querySelector('[name="nome"]').value = data.nome;
        document.querySelector('[name="cargo"]').value = data.cargo;
        document.querySelector('[name="telefone1"]').value = data.telefone1 || "";
        document.querySelector('[name="telefone2"]').value = data.telefone2 || "";
        document.querySelector('[name="email"]').value = data.email || "";
        document.querySelector('[name="observacoes"]').value = data.observacoes || "";
      })
      .catch(() => {
        exibirModalErro("Erro ao carregar dados do contato.");
      });
  }

  //--------------------------------------------------------------------------

  // Aplica máscara nos campos de telefone dentro do modal de contatos
function aplicarMascaraTelefone(contatoSelector) {
  const campo = document.querySelector(contatoSelector);
  if (!campo) return;

  campo.addEventListener("input", function () {
    campo.value = campo.value
      .replace(/\D/g, "")
      .replace(/^(\d{2})(\d)/g, "($1) $2")
      .replace(/(\d{5})(\d{4})$/, "$1-$2")
      .slice(0, 15);
  });
}

// Ativa as máscaras assim que o modal for aberto
document.getElementById("modalContatosCliente").addEventListener("shown.bs.modal", function () {
  setTimeout(() => {
    aplicarMascaraTelefone('[name="telefone1"]');
    aplicarMascaraTelefone('[name="telefone2"]');
  }, 100); // pequeno atraso para garantir que os inputs estejam prontos
});

  