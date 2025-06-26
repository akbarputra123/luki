document.addEventListener("DOMContentLoaded", function () {
  const modal = document.getElementById("detailModal");
  const closeBtn = document.querySelector(".close-btn");

  document.querySelectorAll(".detail-btn").forEach(button => {
    button.addEventListener("click", () => {
      document.getElementById("modal-tanggal").textContent = button.dataset.tanggal;
      document.getElementById("modal-penyakit").textContent = button.dataset.penyakit;
      document.getElementById("modal-keyakinan").textContent = button.dataset.keyakinan;

      modal.style.display = "flex"; // PENTING
    });
  });

  closeBtn.onclick = () => modal.style.display = "none";
  window.onclick = event => {
    if (event.target == modal) modal.style.display = "none";
  };
});
