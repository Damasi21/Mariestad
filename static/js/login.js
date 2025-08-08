document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".toggle-password").forEach(button => {
    button.addEventListener("click", () => {
      const targetId = button.getAttribute("data-target");
      const input = document.getElementById(targetId);
      if (input.type === "password") {
        input.type = "text";
        button.innerHTML = "🙈";
      } else {
        input.type = "password";
        button.innerHTML = "👁";
      }
    });
  });
});
