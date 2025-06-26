document.addEventListener('DOMContentLoaded', function () {
  const modal = document.getElementById('editModal');
  const form = document.getElementById('editForm');
  const closeModalBtn = document.getElementById('closeModal');

  const idInput = document.getElementById('edit_id');
  const mbInput = document.getElementById('edit_mb');
  const mdInput = document.getElementById('edit_md');
  const penyakitSelect = document.getElementById('edit_penyakit_id');
  const gejalaSelect = document.getElementById('edit_gejala_id');

  // Handler tombol edit
  document.querySelectorAll(".edit-button").forEach(button => {
    button.addEventListener("click", function (e) {
      e.preventDefault();

      idInput.value = this.dataset.id;
      mbInput.value = this.dataset.mb;
      mdInput.value = this.dataset.md;
      penyakitSelect.value = this.dataset.penyakitId;
      gejalaSelect.value = this.dataset.gejalaId;

      form.action = this.dataset.url;
      modal.style.display = "block";
    });
  });

  // Tombol close (X)
  closeModalBtn.addEventListener("click", function () {
    modal.style.display = "none";
  });

  // Tombol batal di dalam form
  window.tutupModal = function () {
    modal.style.display = "none";
  };

  // Klik di luar modal
  window.addEventListener("click", function (e) {
    if (e.target === modal) {
      modal.style.display = "none";
    }
  });

  // Tutup modal dengan tombol Escape
  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape") {
      modal.style.display = "none";
    }
  });

  // Flash message hilang otomatis setelah 2 detik
  const flashMessages = document.querySelectorAll('.flash');
  if (flashMessages.length > 0) {
    setTimeout(() => {
      flashMessages.forEach(msg => {
        msg.style.transition = 'opacity 0.5s ease';
        msg.style.opacity = '0';
        setTimeout(() => msg.remove(), 500);
      });
    }, 2000);
  }
});
