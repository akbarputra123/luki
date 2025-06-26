function bukaModalEdit(id, kode, nama, deskripsi, kategori) {
  document.getElementById('edit_id').value = id;
  document.getElementById('edit_kode_gejala').value = kode;
  document.getElementById('edit_nama_gejala').value = nama;
  document.getElementById('edit_deskripsi').value = deskripsi;
  document.getElementById('edit_kategori').value = kategori;

  // Update form action sesuai ID
  document.getElementById('formEditGejala').action = `/admin/gejala/edit/${id}`;
  document.getElementById('modalEdit').style.display = 'block';
}

function tutupModal() {
  document.getElementById('modalEdit').style.display = 'none';
}
function bukaModalEdit(id, kode, nama, deskripsi, kategori) {
  document.getElementById('edit_id').value = id;
  document.getElementById('edit_kode_gejala').value = kode;
  document.getElementById('edit_nama_gejala').value = nama;
  document.getElementById('edit_deskripsi').value = deskripsi;
  document.getElementById('edit_kategori').value = kategori;

  document.getElementById('formEditGejala').action = '/admin/gejala/edit/' + id;
  document.getElementById('modalEdit').style.display = 'block';
}

function tutupModal() {
  document.getElementById('modalEdit').style.display = 'none';
}

// Tambahkan agar modal bisa ditutup dengan Escape
document.addEventListener('keydown', function(event) {
  if (event.key === 'Escape') {
    tutupModal();
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
