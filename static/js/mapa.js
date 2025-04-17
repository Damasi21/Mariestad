function initMap() {
    const mapa = new google.maps.Map(document.getElementById('map'), {
      center: { lat: -14.235, lng: -51.925 },
      zoom: 5
    });
  
    fetch('/clientes/mapa/json/')
      .then(res => res.json())
      .then(clientes => {
        const geocoder = new google.maps.Geocoder();
  
        clientes.forEach(cliente => {
          const enderecoCompleto = `${cliente.endereco}, ${cliente.numero}, ${cliente.cidade} - ${cliente.estado}, Brasil`;
          console.log("Endereço completo:", enderecoCompleto);
  
          geocoder.geocode({ address: enderecoCompleto }, function(results, status) {
            if (status === 'OK') {
              const marker = new google.maps.Marker({
                position: results[0].geometry.location,
                map: mapa,
                title: cliente.nome,
                icon: getIconByStatus(cliente.status_nome)
              });
  
              const info = new google.maps.InfoWindow({
                content: `<strong>${cliente.nome}</strong><br>${enderecoCompleto}<br>Status: ${cliente.status_nome}`
              });
  
              marker.addListener('click', function () {
                info.open(mapa, marker);
              });
            } else {
              console.warn("Falha na geocodificação:", enderecoCompleto, "→", status);
            }
          });
        });
      });
  }
  
  function getIconByStatus(status) {
    const cores = {
      "VERDE": "http://maps.google.com/mapfiles/ms/icons/green-dot.png",
      "VERMELHO": "http://maps.google.com/mapfiles/ms/icons/red-dot.png",
      "AMARELO": "http://maps.google.com/mapfiles/ms/icons/yellow-dot.png"
    };
    return cores[status] || "http://maps.google.com/mapfiles/ms/icons/blue-dot.png";
  }
  
  window.onload = initMap;
  