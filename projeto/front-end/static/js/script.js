document.addEventListener("DOMContentLoaded", function () {
  const navbar = document.getElementById("mainNav");
  if (navbar) {
    window.addEventListener("scroll", () => {
      if (window.scrollY > 30) {
        navbar.classList.add("scrolled");
      } else {
        navbar.classList.remove("scrolled");
      }
    });
  }
  document.querySelectorAll(".toggle-password").forEach(function (btn) {
    btn.addEventListener("click", function () {
      const targetId = this.getAttribute("data-target");
      const input = document.getElementById(targetId);
      if (!input) return;
      const icon = this.querySelector("i");
      if (input.type === "password") {
        input.type = "text";
        icon.classList.replace("bi-eye-fill", "bi-eye-slash-fill");
      } else {
        input.type = "password";
        icon.classList.replace("bi-eye-slash-fill", "bi-eye-fill");
      }
    });
  });
  document.querySelectorAll(".flash-container .alert").forEach(function (alertEl) {
    setTimeout(function () {
      const bsAlert = bootstrap.Alert.getOrCreateInstance(alertEl);
      bsAlert.close();
    }, 5000);
  });
  const inputs = document.querySelectorAll("form .form-control, form .form-select");
  inputs.forEach(function (input) {
    input.addEventListener("blur", function () {
      if (this.value.trim() === "" && this.required) {
        this.classList.add("is-invalid");
      } else {
        this.classList.remove("is-invalid");
      }
    });
    input.addEventListener("input", function () {
      if (this.value.trim() !== "") {
        this.classList.remove("is-invalid");
      }
    });
  });
  document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
    anchor.addEventListener("click", function (e) {
      const targetId = this.getAttribute("href");
      if (targetId === "#") return;
      const target = document.querySelector(targetId);
      if (target) {
        e.preventDefault();
        const offset = 80; 
        const top = target.getBoundingClientRect().top + window.scrollY - offset;
        window.scrollTo({ top, behavior: "smooth" });
      }
    });
  });
  const observerOptions = {
    threshold: 0.1,
    rootMargin: "0px 0px -40px 0px",
  };
  const observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        entry.target.style.opacity = "1";
        entry.target.style.transform = "translateY(0)";
        observer.unobserve(entry.target);
      }
    });
  }, observerOptions);
  document.querySelectorAll(".service-card, .stat-card, .feature-card").forEach(function (card, index) {
    card.style.opacity = "0";
    card.style.transform = "translateY(24px)";
    card.style.transition = `opacity 0.4s ease ${index * 0.08}s, transform 0.4s ease ${index * 0.08}s`;
    observer.observe(card);
  });
});
function confirmarExclusao(url, nome) {
  const modal = document.getElementById("modalExclusao");
  const formExcluir = document.getElementById("formExcluir");
  const nomeEl = document.getElementById("nomeExcluir");
  if (!modal || !formExcluir) return;
  nomeEl.textContent = nome;
  formExcluir.action = url;
  const bsModal = new bootstrap.Modal(modal);
  bsModal.show();
}
