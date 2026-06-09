/**
 * script.js – Lógica JavaScript do BoostPro.
 * Responsável por: navbar scroll, toggle de senha, modal de exclusão, auto-dismiss de alertas.
 */

document.addEventListener("DOMContentLoaded", function () {

  // ─────────────────────────────────────────────
  // 1. Navbar – adiciona classe ao rolar a página
  // ─────────────────────────────────────────────
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

  // ─────────────────────────────────────────────
  // 2. Toggle de visibilidade da senha
  //    Funciona em qualquer botão com classe .toggle-password
  //    e atributo data-target="<id_do_input>"
  // ─────────────────────────────────────────────
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

  // ─────────────────────────────────────────────
  // 3. Auto-dismiss de flash messages após 5 segundos
  // ─────────────────────────────────────────────
  document.querySelectorAll(".flash-container .alert").forEach(function (alertEl) {
    setTimeout(function () {
      // Usa a API do Bootstrap para fechar o alerta com animação
      const bsAlert = bootstrap.Alert.getOrCreateInstance(alertEl);
      bsAlert.close();
    }, 5000);
  });

  // ─────────────────────────────────────────────
  // 4. Validação em tempo real (highlight de erros)
  //    Marca campos como inválidos ao sair do campo (blur)
  // ─────────────────────────────────────────────
  const inputs = document.querySelectorAll("form .form-control, form .form-select");

  inputs.forEach(function (input) {
    input.addEventListener("blur", function () {
      if (this.value.trim() === "" && this.required) {
        this.classList.add("is-invalid");
      } else {
        this.classList.remove("is-invalid");
      }
    });

    // Remove marcação de erro ao começar a digitar
    input.addEventListener("input", function () {
      if (this.value.trim() !== "") {
        this.classList.remove("is-invalid");
      }
    });
  });

  // ─────────────────────────────────────────────
  // 5. Scroll suave para âncoras internas (#)
  // ─────────────────────────────────────────────
  document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
    anchor.addEventListener("click", function (e) {
      const targetId = this.getAttribute("href");
      if (targetId === "#") return;

      const target = document.querySelector(targetId);
      if (target) {
        e.preventDefault();
        const offset = 80; // altura da navbar fixa
        const top = target.getBoundingClientRect().top + window.scrollY - offset;
        window.scrollTo({ top, behavior: "smooth" });
      }
    });
  });

  // ─────────────────────────────────────────────
  // 6. Animação de entrada dos cards de serviço
  //    Usa IntersectionObserver para animar ao entrar na tela
  // ─────────────────────────────────────────────
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

  // Aplica nos service-cards e stat-cards
  document.querySelectorAll(".service-card, .stat-card, .feature-card").forEach(function (card, index) {
    card.style.opacity = "0";
    card.style.transform = "translateY(24px)";
    card.style.transition = `opacity 0.4s ease ${index * 0.08}s, transform 0.4s ease ${index * 0.08}s`;
    observer.observe(card);
  });

});


// ─────────────────────────────────────────────
// 7. Modal de confirmação de exclusão
//    Chamado pelos botões de excluir nas tabelas admin.
//    Parâmetros: url (action do form), nome (texto a exibir)
// ─────────────────────────────────────────────
function confirmarExclusao(url, nome) {
  const modal = document.getElementById("modalExclusao");
  const formExcluir = document.getElementById("formExcluir");
  const nomeEl = document.getElementById("nomeExcluir");

  if (!modal || !formExcluir) return;

  // Preenche os dados do modal
  nomeEl.textContent = nome;
  formExcluir.action = url;

  // Abre o modal via Bootstrap JS
  const bsModal = new bootstrap.Modal(modal);
  bsModal.show();
}
