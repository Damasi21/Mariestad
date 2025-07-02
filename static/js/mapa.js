let todosMarcadores = [];
let mapa = null;

function initMap() {
  mapa = new google.maps.Map(document.getElementById('map'), {
    center: { lat: -14.235, lng: -51.925 },
    zoom: 5
  });

  window.__mapRef = mapa;
  const geocoder = new google.maps.Geocoder();

  // 🔴 Carregar clientes
  fetch('/clientes/mapa/json/')
    .then(res => res.json())
    .then(clientes => {
      clientes.forEach(cliente => {
        const enderecoCompleto = `${cliente.endereco}, ${cliente.numero}, ${cliente.cidade} - ${cliente.estado}, ${cliente.cep}, Brasil`;

        geocoder.geocode({ address: enderecoCompleto }, function (results, status) {
          if (status === 'OK') {
            adicionarMarcador(cliente, results[0].geometry.location, mapa);
          } else {
            const fallbackEndereco = `${cliente.cidade} - ${cliente.estado}, Brasil`;
            geocoder.geocode({ address: fallbackEndereco }, function (fallbackResults, fallbackStatus) {
              if (fallbackStatus === 'OK') {
                adicionarMarcador(cliente, fallbackResults[0].geometry.location, mapa, true);
              }
            });
          }
        });
      });
    });

  // 🔵 Carregar obras
  fetch('/obras/mapa/json/')
    .then(res => res.json())
    .then(obras => {
      obras.forEach(obra => {
        const enderecoObra = `${obra.endereco}, ${obra.cidade} - ${obra.estado}, Brasil`;

        geocoder.geocode({ address: enderecoObra }, function (results, status) {
          if (status === 'OK') {
            adicionarMarcadorObra(obra, results[0].geometry.location);
          } else {
            const fallbackEndereco = `${obra.cidade} - ${obra.estado}, Brasil`;
            geocoder.geocode({ address: fallbackEndereco }, function (fallbackResults, fallbackStatus) {
              if (fallbackStatus === 'OK') {
                adicionarMarcadorObra(obra, fallbackResults[0].geometry.location, true);
              } else {
                console.warn("❌ Obra ignorada (falha dupla):", obra.nome, fallbackEndereco, fallbackStatus);
              }
            });
          }
        });
      });
    });
}
// --------------------- ---------------------------------------

function adicionarMarcador(cliente, location, mapa, isFallback = false) {
  const marker = new google.maps.Marker({
    position: location,
    map: mapa,
    title: cliente.nome,
    icon: {
      url: getIconByStatus(cliente.status_nome),
      scaledSize: new google.maps.Size(32, 32)
    }
  });

  const info = new google.maps.InfoWindow({
    content: `
      <strong>${cliente.nome}</strong><br>
      ${cliente.endereco}, ${cliente.numero}, ${cliente.cidade} - ${cliente.estado}, ${cliente.cep}<br>
      Status: ${cliente.status_nome}
      ${isFallback ? "<br><em>(Localização aproximada)</em>" : ""}
    `
  });

  marker.addListener('click', function () {
    info.open(mapa, marker);
  });

  todosMarcadores.push({
    marker: marker,
    status: cliente.status_nome?.trim().toLowerCase()
  });
}
// --------------------- ---------------------------------------

function adicionarMarcadorObra(obra, location, isFallback = false) {
  const marker = new google.maps.Marker({
    position: location,
    map: mapa,
    title: `[OBRA] ${obra.nome}`,
    icon: {
      url: obterIconeObra(obra.status_nome),
      scaledSize: new google.maps.Size(40, 40)
    }
  });

  // 👉 Adiciona tags se existirem
  const tagsHtml = obra.tags && obra.tags.length
    ? `<br><strong>Tags:</strong> ${obra.tags.join(", ")}`
    : "";

  const info = new google.maps.InfoWindow({
    content: `
      <strong>[OBRA]</strong> ${obra.nome}<br>
      ${obra.endereco}, ${obra.cidade} - ${obra.estado}
      ${isFallback ? "<br><em>(Localização aproximada)</em>" : ""}
      ${tagsHtml}
    `
  });

  marker.addListener('click', function () {
    info.open(mapa, marker);
  });

  // 🔧 Adiciona ao filtro com normalização de acento e minúsculo
  const statusNormalizado = (obra.status_nome || "Sem status")
    .trim()
    .toLowerCase()
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "");

  todosMarcadores.push({
    marker: marker,
    status: statusNormalizado
  });
}


// --------------------- ---------------------------------------

function getIconByStatus(status) {
  if (!status) return "http://maps.google.com/mapfiles/ms/icons/purple-dot.png";

  const key = status.trim().toLowerCase();

  const cores = {
    "parceiro": "ltblue",
    "premium": "blue",
    "ouro": "green",
    "prata": "yellow",
    "bronze": "orange",
    "risco": "red",
    "inativo": "purple"
  };

  const cor = cores[key] || "purple";
  return `http://maps.google.com/mapfiles/ms/icons/${cor}-dot.png`;
}


// --------------------- ---------------------------------------

function obterIconeObra(status) {
  switch (status?.toLowerCase()) {
    case "ganha":
      return "/media/icone_mapa_ganha.png";
    case "perdida":
      return "/media/icone_mapa_perdida.png";
    case "em execução":
    case "em execucao":
      return "/media/icone_mapa_emexecucao.png";
    case "a executar":
      return "/media/icone_mapa_aexecutar.png";
    default:
      return "https://maps.google.com/mapfiles/kml/shapes/construction.png";
  }
}


// --------------------- ---------------------------------------

function filtrarMarcadoresPorStatus() {
  const statusSelecionado = document.getElementById("filtroStatus").value.toLowerCase();

  todosMarcadores.forEach(({ marker, status }) => {
    const visivel = !statusSelecionado || status === statusSelecionado;
    marker.setVisible(visivel);
  });
}

function irParaCidade() {
  const cidade = document.getElementById("cidadeBusca").value.trim();
  if (!cidade) return;

  const geocoder = new google.maps.Geocoder();
  geocoder.geocode({ address: `${cidade}, Brasil` }, function(results, status) {
    if (status === "OK") {
      mapa.setCenter(results[0].geometry.location);
      mapa.setZoom(11);
    } else {
      alert("Cidade não encontrada.");
    }
  });
}

window.initMap = initMap;
