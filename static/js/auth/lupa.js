// lupa.js
document.addEventListener('DOMContentLoaded', function () {
    const input = document.querySelector('input[name="username"]');
    const form = document.querySelector('form');

    form.addEventListener('submit', function (e) {
        if (input.value.trim() === '') {
            e.preventDefault();
            alert('Username tidak boleh kosong!');
            input.focus();
        }
    });
});
