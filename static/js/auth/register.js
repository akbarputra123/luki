document.addEventListener("DOMContentLoaded", function () {
  // Efek interaktif input
  const inputs = document.querySelectorAll("input");
  inputs.forEach(input => {
    input.addEventListener("focus", () => {
      input.style.backgroundColor = "#e6f0ff";
    });
    input.addEventListener("blur", () => {
      input.style.backgroundColor = "white";
    });
  });
});
