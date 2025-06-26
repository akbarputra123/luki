document.addEventListener("DOMContentLoaded", function () {
  const sidebar = document.querySelector(".sidebar");
  const menuBtn = document.querySelector(".mobile-menu-btn");
  const closeBtn = document.querySelector(".sidebar-close");
  const overlay = document.querySelector(".overlay");

  menuBtn.addEventListener("click", () => {
    sidebar.classList.add("show");
    overlay.classList.add("show");
    menuBtn.style.display = "none";  // ⬅️ Sembunyikan tombol menu setelah diklik
  });

  closeBtn.addEventListener("click", () => {
    sidebar.classList.remove("show");
    overlay.classList.remove("show");
    menuBtn.style.display = "block"; // ⬅️ Tampilkan kembali saat sidebar ditutup
  });

  overlay.addEventListener("click", () => {
    sidebar.classList.remove("show");
    overlay.classList.remove("show");
    menuBtn.style.display = "block"; // ⬅️ Tampilkan kembali saat overlay diklik
  });
});
