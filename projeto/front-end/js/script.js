document.addEventListener("DOMContentLoaded", function () {
  const navbar = document.getElementById("mainNav");
  if (navbar) {
    window.addEventListener("scroll", () => {
      navbar.classList.toggle("scrolled", window.scrollY > 30);
    });
  }
  document.querySelectorAll(".toggle-password").forEach(function (btn) {
    btn.addEventListener("click", function () {
      const input = document.getElementById(this.getAttribute("data-target"));
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
  const observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        entry.target.style.opacity = "1";
        entry.target.style.transform = "translateY(0)";
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1, rootMargin: "0px 0px -40px 0px" });
  document.querySelectorAll(".service-card, .stat-card, .feature-card").forEach(function (card, i) {
    card.style.opacity = "0";
    card.style.transform = "translateY(24px)";
    card.style.transition = `opacity 0.4s ease ${i * 0.08}s, transform 0.4s ease ${i * 0.08}s`;
    observer.observe(card);
  });
  document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
    anchor.addEventListener("click", function (e) {
      const targetId = this.getAttribute("href");
      if (targetId === "#") return;
      const target = document.querySelector(targetId);
      if (target) {
        e.preventDefault();
        const top = target.getBoundingClientRect().top + window.scrollY - 80;
        window.scrollTo({ top, behavior: "smooth" });
      }
    });
  });
  const formCadastro = document.getElementById("formCadastro");
  if (formCadastro) {
    formCadastro.addEventListener("submit", function (e) {
      e.preventDefault();
      let valido = true;
      const nome = document.getElementById("nome");
      const email = document.getElementById("email");
      const senha = document.getElementById("senha");
      const confirmarSenha = document.getElementById("confirmarSenha");
      if (!nome.value.trim() || nome.value.trim().length < 3) {
        nome.classList.add("is-invalid");
        valido = false;
      } else {
        nome.classList.remove("is-invalid");
      }
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(email.value.trim())) {
        email.classList.add("is-invalid");
        valido = false;
      } else {
        email.classList.remove("is-invalid");
      }
      if (senha.value.length < 6) {
        senha.classList.add("is-invalid");
        valido = false;
      } else {
        senha.classList.remove("is-invalid");
      }
      if (confirmarSenha.value !== senha.value) {
        confirmarSenha.classList.add("is-invalid");
        valido = false;
      } else {
        confirmarSenha.classList.remove("is-invalid");
      }
      if (valido) {
        const alerta = document.getElementById("alertaCadastro");
        alerta.className = "alert alert-success";
        alerta.innerHTML = '<i class="bi bi-check-circle-fill me-2"></i>Cadastro realizado! Faça login para continuar.';
        formCadastro.reset();
        setTimeout(() => { window.location.href = "login.html"; }, 2000);
      }
    });
  }
  const formLogin = document.getElementById("formLogin");
  if (formLogin) {
    formLogin.addEventListener("submit", function (e) {
      e.preventDefault();
      const email = document.getElementById("email");
      const senha = document.getElementById("senha");
      const alerta = document.getElementById("alertaLogin");
      let valido = true;
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(email.value.trim())) {
        email.classList.add("is-invalid"); valido = false;
      } else { email.classList.remove("is-invalid"); }
      if (!senha.value) {
        senha.classList.add("is-invalid"); valido = false;
      } else { senha.classList.remove("is-invalid"); }
      if (valido) {
        alerta.classList.add("d-none");
        window.location.href = "dashboard.html";
      } else {
        alerta.classList.remove("d-none");
      }
    });
  }
});
