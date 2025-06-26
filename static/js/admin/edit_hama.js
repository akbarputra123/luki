function openEditModal(id, kode, nama, deskripsi, solusi) {
  document.getElementById("edit_id").value = id;
  document.getElementById("edit_kode_penyakit").value = kode;
  document.getElementById("edit_nama_penyakit").value = nama;
  document.getElementById("edit_deskripsi").value = deskripsi;
  document.getElementById("edit_solusi").value = solusi;

  document.getElementById("editForm").action = "/admin/hama/edit/" + id;
  document.getElementById("editModal").style.display = "block";
}

function closeEditModal() {
  document.getElementById("editModal").style.display = "none";
}
function openEditModal(id, kode, nama, deskripsi, solusi) {
  document.getElementById("edit_id").value = id;
  document.getElementById("edit_kode_penyakit").value = kode;
  document.getElementById("edit_nama_penyakit").value = nama;
  document.getElementById("edit_deskripsi").value = deskripsi;
  document.getElementById("edit_solusi").value = solusi;

  document.getElementById("editForm").action = "/admin/hama/edit/" + id;
  document.getElementById("editModal").style.display = "block";
}

function closeEditModal() {
  document.getElementById("editModal").style.display = "none";
}

// Tambahkan support tombol ESC
document.addEventListener("keydown", function (event) {
  if (event.key === "Escape") {
    closeEditModal();
  }
});

// Sembunyikan flash message setelah 2 detik
document.addEventListener('DOMContentLoaded', function () {
  const flashMessages = document.querySelectorAll('.flash');
  if (flashMessages.length > 0) {
    setTimeout(() => {
      flashMessages.forEach(msg => {
        msg.style.transition = 'opacity 0.5s ease';
        msg.style.opacity = '0';
        setTimeout(() => msg.remove(), 500); // Hapus dari DOM setelah animasi
      });
    }, 2000); // 2 detik
  }
});
