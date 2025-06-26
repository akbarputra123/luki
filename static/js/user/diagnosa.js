// diagnosa.js
document.addEventListener('DOMContentLoaded', () => {
  console.log('Halaman Konsultasi Diagnosa siap!');

  const radios = document.querySelectorAll('input[type="radio"]');
  radios.forEach(radio => {
    radio.addEventListener('change', () => {
      radios.forEach(r => r.parentElement.classList.remove('selected'));
      radio.parentElement.classList.add('selected');
    });
  });
});
