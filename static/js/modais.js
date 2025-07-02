function abrirModalPDF(propostaId) {
  document.getElementById("btnPdfCompleta").href = `/proposta/${propostaId}/pdf/`;
  const modal = new bootstrap.Modal(document.getElementById("modalEscolherPDF"));
  modal.show();
}