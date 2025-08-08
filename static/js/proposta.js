document.addEventListener("DOMContentLoaded", function () {
  const clienteSelect = document.getElementById("id_cliente");
  const obraSelect = document.getElementById("id_obra");
  const contatoSelect = document.getElementById("id_contato");
  const perfilInput = document.getElementById("id_perfil_contato");
  const freteTech4con = document.getElementById("id_frete_tech4con");
  const freteCliente = document.getElementById("id_frete_cliente");
  const form = document.getElementById("formProposta");
  const condicaoInput = document.getElementById("id_condicao_pagamento");
  const parcelasInput = document.getElementById("id_parcelas_condicao");
  const buscaNumero = document.getElementById("busca_proposta_numero");
  const buscaCliente = document.getElementById("busca_proposta_cliente");


  if (buscaNumero) {
    buscaNumero.addEventListener("input", function () {
      const termo = this.value.trim().toLowerCase();
      const linhas = document.querySelectorAll("#aba-listagem table tbody tr");

      linhas.forEach((linha) => {
        const celulaNumero = linha.querySelector("td:nth-child(1)");
        const texto = celulaNumero?.textContent?.toLowerCase() || "";
        linha.style.display = texto.includes(termo) ? "" : "none";
      });
    });
  }

  if (buscaCliente) {
    buscaCliente.addEventListener("input", function () {
      const termo = this.value.trim().toLowerCase();
      const linhas = document.querySelectorAll("#aba-listagem table tbody tr");

      linhas.forEach((linha) => {
        const celulaCliente = linha.querySelector("td:nth-child(2)");
        const texto = celulaCliente?.textContent?.toLowerCase() || "";
        linha.style.display = texto.includes(termo) ? "" : "none";
      });
    });
  }




  if (clienteSelect) {
  clienteSelect.addEventListener("change", function () {
    const clienteId = this.value;

    fetch(`/propostas/obras/${clienteId}/`)
      .then(resp => resp.json())
      .then(data => {
        obraSelect.innerHTML = '<option value="">Selecione</option>';
        data.obras.forEach(o => {
          const option = document.createElement("option");
          option.value = o.id;
          option.textContent = o.nome;
          obraSelect.appendChild(option);
        });
      });

    fetch(`/propostas/contatos/${clienteId}/`)
      .then(resp => resp.json())
      .then(data => {
        contatoSelect.innerHTML = '<option value="">Selecione</option>';
        data.contatos.forEach(c => {
          const option = document.createElement("option");
          option.value = c.id;
          option.textContent = c.nome;
          option.dataset.perfil = c.perfil;
          contatoSelect.appendChild(option);
        });
      });
  });
}

// 🔁 Preenche automaticamente o campo de observações com o que está salvo na obra
const observacoesProposta = document.getElementById("id_observacoes_proposta");

if (obraSelect) {
  obraSelect.addEventListener("change", function () {
    const obraId = this.value;

    if (obraId && observacoesProposta) {
      fetch(`/propostas/observacoes-obra/${obraId}/`)
        .then(resp => resp.json())
        .then(data => {
          observacoesProposta.value = data.observacoes || "";
        });
    }
  });
}


  if (freteTech4con) {
    freteTech4con.addEventListener("input", function () {
      const valor = parseFloat(this.value.replace(",", ".")) || 0;
      freteCliente.value = (valor * 1.3).toFixed(2);
    });
  }

  if (condicaoInput) {
    condicaoInput.addEventListener("input", function () {
      const valores = this.value.split("/");
      const hoje = new Date();
      const datas = valores.map(dias => {
        const dt = new Date(hoje);
        dt.setDate(dt.getDate() + parseInt(dias.trim()));
        return dt.toLocaleDateString('pt-BR');
      });
      parcelasInput.value = datas.join(" -- ");
    });
  }

if (form) {
  form.addEventListener("submit", function (e) {
    e.preventDefault();

    // ✅ Garante que os produtos são atualizados
    salvarProdutos();

    const produtosJson = document.getElementById("produtos_json").value;
    const produtos = JSON.parse(produtosJson || "[]");

    if (produtos.length === 0) {
      alert("Adicione pelo menos um produto válido antes de salvar a proposta.");
      return;
    }

    setTimeout(() => {
      form.submit();
    }, 100);
  });
}



  setupAutoComplete('busca_cliente', 'resultado_cliente', 'id_cliente', '/buscar-clientes');
  setupAutoComplete('busca_obra', 'resultado_obra', 'id_obra', '/buscar-obras');
  setupAutoComplete('busca_transportadora', 'resultado_transportadora', 'id_transportadora', '/buscar-transportadoras');
});

//-------------------------------------------------------------------------
function adicionarProduto() {
  const tabela = document.getElementById("tabela-produtos");

  const linhaPrincipal = document.createElement("tr");
  const linhaObs = document.createElement("tr");

  linhaPrincipal.innerHTML = `
    <td><select class="form-select produto-select"><option value="">Selecione</option></select></td>
    <td><input type="text" class="form-control descricao"></td>
    <td><input type="text" class="form-control unidade"></td>
    <td><input type="number" class="form-control quantidade" step="0.01"></td>
    <td><input type="number" class="form-control preco" step="0.01"></td>
    <td class="subtotal">0.00</td>
    <td rowspan="2"><button type="button" class="btn btn-danger btn-sm" onclick="removerProduto(this)">X</button></td>
  `;

  linhaObs.innerHTML = `
    <td colspan="6">
      <textarea class="form-control observacao-produto" placeholder="Obserprodutos.forEach(produto =>ações do produto..."></textarea>
    </td>
  `;

  tabela.appendChild(linhaPrincipal);
  tabela.appendChild(linhaObs);

// preenche select de produtos com os dados atuais
  fetch('/propostas/produtos-json/')
    .then(resp => resp.json())
    .then(produtosDisponiveis => {
      const select = linhaPrincipal.querySelector(".produto-select");
      produtosDisponiveis.forEach(p => {
        const opt = document.createElement("option");
        opt.value = p.id;
        opt.textContent = `${p.codigo} - ${p.descricao}`;
        opt.dataset.codigo_completo = `${p.codigo} - ${p.descricao}`;
        opt.dataset.descricao = p.descricao;
        opt.dataset.unidade = p.unidade;
        opt.dataset.preco = p.preco;

       if (typeof produto !== "undefined" && p.codigo && produto.codigo && produto.codigo.startsWith(p.codigo)) {
          opt.selected = true;
        }


        select.appendChild(opt);
      });

    // auto-preenchimento ao alterar produto
    select.addEventListener("change", function () {
      const selected = this.options[this.selectedIndex];
      linhaPrincipal.querySelector(".descricao").value = selected.dataset.descricao || "";
      linhaPrincipal.querySelector(".unidade").value = selected.dataset.unidade || "";
      linhaPrincipal.querySelector(".preco").value = selected.dataset.preco || "";
      atualizarSubtotal.call(linhaPrincipal.querySelector(".quantidade"));
    });
  });



  linhaPrincipal.querySelector(".quantidade").addEventListener("input", atualizarSubtotal);
  linhaPrincipal.querySelector(".preco").addEventListener("input", atualizarSubtotal);

  const campos = linhaPrincipal.querySelectorAll("select, input");
  campos.forEach(campo => {
    campo.addEventListener("change", salvarProdutos);
  });
  linhaObs.querySelector(".observacao-produto").addEventListener("input", salvarProdutos);

}

//-------------------------------------------------------------------------------------
function atualizarSubtotal() {
  const linha = this.closest("tr");
  const qtd = parseFloat(linha.querySelector(".quantidade").value) || 0;
  const preco = parseFloat(linha.querySelector(".preco").value) || 0;
  const subtotal = qtd * preco;
  linha.querySelector(".subtotal").textContent = subtotal.toFixed(2);
  atualizarTotalProdutos();
}

function atualizarTotalProdutos() {
  let total = 0;
  document.querySelectorAll("#tabela-produtos tr").forEach((linha) => {
    const subtotalCell = linha.querySelector(".subtotal");
    if (subtotalCell) {
      const valor = parseFloat(subtotalCell.textContent.replace(",", ".")) || 0;
      total += valor;
    }
  });

  const totalSpan = document.getElementById("totalProdutos");
  if (totalSpan) {
    totalSpan.textContent = total.toLocaleString("pt-BR", {
      style: "decimal",
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    });
  }
}
//---------------------------------------------------------------
function removerProduto(botao) {
  const linha = botao.closest("tr");
  const linhaObs = linha.nextElementSibling;
  linha.remove();
  if (linhaObs && linhaObs.querySelector(".observacao-produto")) {
    linhaObs.remove();
  }
  atualizarTotalProdutos();
}

//---------------------------------------------------------------
function setupAutoComplete(inputId, resultId, hiddenInputId, url) {
  const input = document.getElementById(inputId);
  const resultado = document.getElementById(resultId);
  const hiddenInput = document.getElementById(hiddenInputId);

  input.addEventListener('input', function () {
    const termo = input.value.trim();
    if (termo.length < 1) {
      resultado.innerHTML = '';
      return;
    }

    fetch(`${url}?q=${termo}`)
      .then(resp => resp.json())
      .then(dados => {
        resultado.innerHTML = '';

        dados.forEach(item => {
          const div = document.createElement('div');
          div.className = 'list-group-item list-group-item-action';
          div.textContent = item.texto;
          div.dataset.id = item.id;

          div.addEventListener('click', () => {
            input.value = item.texto;
            hiddenInput.value = item.id;
            resultado.innerHTML = '';

            if (inputId === 'busca_cliente') {
              carregarDadosCliente(item.id);
            }

            if (inputId === 'busca_obra') {
              fetch(`/propostas/observacoes-obra/${item.id}/`)
                .then(resp => resp.json())
                .then(data => {
                  const campoObs = document.getElementById("id_observacoes_proposta");
                  if (campoObs && campoObs.value.trim() === "") {
                    campoObs.value = data.observacoes || "";
                  }
                });
            }
          });

          resultado.appendChild(div);
        });
      });
  });

  document.addEventListener('click', function (e) {
    if (!resultado.contains(e.target) && e.target !== input) {
      resultado.innerHTML = '';
    }
  });
}

// ---------------------------------------------------------------

function carregarDadosCliente(clienteId) {
  const contatoSelect = document.getElementById("id_contato");
  const perfilInput = document.getElementById("id_perfil_contato");
  const vendedorSelect = document.getElementById("id_vendedor");

  fetch(`/propostas/dados-cliente/?cliente_id=${clienteId}`)
    .then(response => response.json())
    .then(data => {
      // Preencher contatos
      contatoSelect.innerHTML = '<option value="">Selecione um contato</option>';
      data.contatos.forEach(c => {
        const opt = document.createElement("option");
        opt.value = c.id;
        opt.textContent = c.nome;
        opt.dataset.perfil = c.perfil;
        contatoSelect.appendChild(opt);
      });

      contatoSelect.addEventListener("change", function () {
        const selected = this.options[this.selectedIndex];
        perfilInput.value = selected.dataset.perfil || "";
      });

      // Preencher vendedores
      vendedorSelect.innerHTML = '<option value="">Selecione um vendedor</option>';
      if (data.vendedores && data.vendedores.length > 0) {
        data.vendedores.forEach(v => {
          const opt = document.createElement("option");
          opt.value = v.id;
          opt.textContent = v.nome;
          vendedorSelect.appendChild(opt);
        });
        // Seleciona o primeiro por padrão
        vendedorSelect.value = data.vendedores[0].id;
      }
    });
}

// ---------------------------------------------------------------

function preencherVendedorPadrao(dadosCliente) {
  const select = document.getElementById("id_vendedor");
  select.innerHTML = '<option value="">Selecione um vendedor</option>';

  if (dadosCliente.vendedores && dadosCliente.vendedores.length > 0) {
    dadosCliente.vendedores.forEach(v => {
      const option = document.createElement("option");
      option.value = v.id;
      option.textContent = v.nome;
      select.appendChild(option);
    });

    // Seleciona o primeiro por padrão
    select.value = dadosCliente.vendedores[0].id;
  }
}


// ---------------------------------------------------------------
function visualizarProposta(id) {
  fetch(`/propostas/carregar/${id}/`)
    .then(response => response.json())
    .then(dados => {
      document.getElementById("proposta_id").value = dados.id;

      // CLIENTE
      if (dados.cliente) {
        document.getElementById("id_cliente").value = dados.cliente.id;
        document.getElementById("busca_cliente").value = dados.cliente.texto;
        carregarDadosCliente(dados.cliente.id);
      }


      // OBRA
      document.getElementById("id_obra").value = dados.obra;
      fetch(`/buscar-obras?q=`)
        .then(resp => resp.json())
        .then(obras => {
          const obra = obras.find(o => o.id == dados.obra);
          if (obra) {
            document.getElementById("busca_obra").value = obra.texto;
          }
        });

      // CONTATO
      setTimeout(() => {
        document.getElementById("id_contato").value = dados.contato;
        document.getElementById("id_perfil_contato").value = dados.perfil_contato || "";
      }, 500);
      document.getElementById("id_perfil_contato").value = dados.perfil_contato;
      document.getElementById("id_status_proposta").value = dados.status_proposta;
      document.getElementById("id_transportadora").value = dados.transportadora;
      document.getElementById("id_tipo_frete").value = dados.tipo_frete;
      document.getElementById("id_peso_liquido").value = dados.peso_liquido;
      document.getElementById("id_peso_bruto").value = dados.peso_bruto;
      document.getElementById("id_volume").value = dados.volume;
      document.getElementById("id_quantidade_volumes").value = dados.quantidade_volumes;
      document.getElementById("id_frete_tech4con").value = dados.frete_tech4con;
      document.getElementById("id_frete_cliente").value = dados.frete_cliente;
      document.getElementById("id_condicao_pagamento").value = dados.condicao_pagamento;
      document.getElementById("id_parcelas_condicao").value = dados.parcelas_condicao;
      document.getElementById("id_endereco_proposta").value = dados.endereco_proposta;
      document.getElementById("id_numero_proposta").value = dados.numero_proposta;
      document.getElementById("id_complemento_proposta").value = dados.complemento_proposta;
      document.getElementById("id_bairro_proposta").value = dados.bairro_proposta;
      document.getElementById("id_cep_proposta").value = dados.cep_proposta;
      document.getElementById("id_cidade_proposta").value = dados.cidade_proposta;
      document.getElementById("id_estado_proposta").value = dados.estado_proposta;
      document.getElementById("id_observacoes_proposta").value = dados.observacoes_proposta;
      document.getElementById("id_nome_entrega").value = dados.nome_entrega || "";

      // Carrega produtos
      const tabela = document.getElementById("tabela-produtos");
      tabela.innerHTML = "";
      const produtos = JSON.parse(dados.produtos_json || "[]");

       produtos.forEach(produto => {
        const linhaPrincipal = document.createElement("tr");
        const linhaObs = document.createElement("tr");

        linhaPrincipal.innerHTML = `
          <td><select class="form-select produto-select"><option value="">Selecione</option></select></td>
          <td><input type="text" class="form-control descricao" name="descricao[]" value="${produto.descricao}"></td>
          <td><input type="text" class="form-control unidade" name="unidade[]" value="${produto.unidade}"></td>
          <td><input type="number" class="form-control quantidade" name="quantidade[]" step="0.01" value="${produto.quantidade}"></td>
          <td><input type="number" class="form-control preco" name="preco[]" step="0.01" value="${produto.preco}"></td>
          <td class="subtotal">${(produto.quantidade * produto.preco).toFixed(2)}</td>
          <td rowspan="2"><button type="button" class="btn btn-danger btn-sm" onclick="removerProduto(this)">X</button></td>
        `;

        linhaObs.innerHTML = `
          <td colspan="6">
            <textarea class="form-control observacao-produto" placeholder="Observações do produto...">${produto.observacao_produto_proposta || ""}</textarea>
          </td>
        `;

        tabela.appendChild(linhaPrincipal);
        tabela.appendChild(linhaObs);

        fetch('/propostas/produtos-json/')
          .then(resp => resp.json())
          .then(produtosDisponiveis => {
            const select = linhaPrincipal.querySelector(".produto-select");
            produtosDisponiveis.forEach(p => {
              const opt = document.createElement("option");
              opt.value = p.id;
              opt.textContent = p.codigo; 
              opt.dataset.codigo = p.codigo;
              opt.dataset.descricao = p.descricao;
              opt.dataset.unidade = p.unidade;
              opt.dataset.preco = p.preco;

             if (produto.id_produto && p.id && parseInt(produto.id_produto) === parseInt(p.id)) {
             opt.selected = true;
              }

              select.appendChild(opt);
            });

            select.addEventListener("change", function () {
              const selected = this.options[this.selectedIndex];
              linhaPrincipal.querySelector(".descricao").value = selected.dataset.descricao || "";
              linhaPrincipal.querySelector(".unidade").value = selected.dataset.unidade || "";
              linhaPrincipal.querySelector(".preco").value = selected.dataset.preco || "";
              atualizarSubtotal.call(linhaPrincipal.querySelector(".quantidade"));
            });
          });

        linhaPrincipal.querySelector(".quantidade").addEventListener("input", atualizarSubtotal);
        linhaPrincipal.querySelector(".preco").addEventListener("input", atualizarSubtotal);
      });

      atualizarTotalProdutos();

      // Troca para a aba de cadastro
      document.getElementById("aba-cadastro-tab").click();
    });
}

// ---------------------------------------------------------------

function confirmarExclusao(id) {
  confirmarAcao("Deseja realmente excluir esta proposta?", () => {
    fetch(`/propostas/excluir/${id}/`, {
      method: "POST",
      headers: {
        "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value
      }
    })
    .then(resp => resp.json())
    .then(data => {
      if (data.status === "ok") {
        exibirModalSucesso("Proposta excluída com sucesso!");
        setTimeout(() => {
          window.location.reload();
        }, 1000);
      } else {
        alert("Erro ao excluir: " + (data.mensagem || "erro desconhecido"));
      }
    });
  }, 'danger');
}
// ---------------------------------------------------------------

function salvarProdutos() {
  const linhas = document.querySelectorAll("#tabela-produtos tr");
  const produtos = [];

  for (let i = 0; i < linhas.length; i += 2) {
    const linha = linhas[i];
    const observacao = linhas[i + 1]?.querySelector(".observacao-produto")?.value || "";
    const selected = linha.querySelector(".produto-select")?.selectedOptions[0];

    if (!selected || !selected.value) {
      continue;
    }

    const produto = {
      id_produto: selected.value,
      codigo: selected.dataset.codigo_completo || selected.textContent || "",
      descricao: linha.querySelector(".descricao")?.value || "",
      unidade: linha.querySelector(".unidade")?.value || "",
      quantidade: parseFloat(linha.querySelector(".quantidade")?.value || 0),
      preco: parseFloat(linha.querySelector(".preco")?.value || 0),
      subtotal: parseFloat(
        (linha.querySelector(".quantidade")?.value || 0) *
        (linha.querySelector(".preco")?.value || 0)
      ),
      observacao_produto_proposta: observacao
    };

    produtos.push(produto);
  }

  document.getElementById("produtos_json").value = JSON.stringify(produtos);
}
  
// ------------------------PROPOSTA PDF---------------------------------------

function abrirModalEscolhaPDF(propostaId) {
  const btnCompleta = document.getElementById("btnPdfCompleta");
  const btnResumida = document.getElementById("btnPdfResumida");

  btnCompleta.href = `/propostas/pdf-completa/${propostaId}/`;
  btnResumida.href = `/propostas/pdf-resumida/${propostaId}/`;  // futuro

  const modal = new bootstrap.Modal(document.getElementById("modalEscolherPDF"));
  modal.show();
}

// ------------------------busca Obs de Obra ---------------------------------------


document.getElementById("busca_obra").addEventListener("input", function () {
  const termo = this.value.trim();

  if (termo.length >= 2) {
    fetch(`/buscar-obras?q=${termo}`)
      .then((response) => response.json())
      .then((obras) => {
        const lista = document.getElementById("resultado_obra");
        lista.innerHTML = "";

        obras.forEach((obra) => {
          const item = document.createElement("a");
          item.classList.add("list-group-item", "list-group-item-action");
          item.textContent = obra.texto;
          item.dataset.id = obra.id;

          item.onclick = function () {
            document.getElementById("busca_obra").value = obra.texto;
            document.getElementById("id_obra").value = obra.id;
            lista.innerHTML = "";

            // Buscar observações da obra
            fetch(`/obras/observacoes/${obra.id}/`)
              .then((r) => r.json())
              .then((dados) => {
                const campoObs = document.getElementById("id_observacoes_proposta");
                if (dados.observacoes && campoObs.value.trim() === "") {
                  campoObs.value = dados.observacoes;
                }
              });
          };

          lista.appendChild(item);
        });
      });
  }
});
