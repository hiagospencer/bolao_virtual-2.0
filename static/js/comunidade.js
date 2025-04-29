document.addEventListener("DOMContentLoaded", function () {
  // Troca de abas
  const tabBtns = document.querySelectorAll(".tab-btn");
  const tabContents = document.querySelectorAll(".tab-content");

  tabBtns.forEach((btn) => {
    btn.addEventListener("click", function () {
      // Remove classe active de todos os botões e conteúdos
      tabBtns.forEach((b) => b.classList.remove("active"));
      tabContents.forEach((c) => c.classList.remove("active"));

      // Adiciona classe active ao botão clicado
      this.classList.add("active");

      // Mostra o conteúdo correspondente
      const tabId = this.dataset.tab;
      document.getElementById(tabId).classList.add("active");
    });
  });

  // Simulação de criação de novo tópico
  const newTopicBtn = document.querySelector(".btn-new-topic");
  if (newTopicBtn) {
    newTopicBtn.addEventListener("click", function () {
      alert(
        "Funcionalidade de novo tópico será implementada aqui!\nVocê será redirecionado para o formulário de criação."
      );
      // window.location.href = 'novo-topico.html';
    });
  }

  // Simulação de nova mensagem no mural
  const newPostBtn = document.querySelector(".btn-new-post");
  if (newPostBtn) {
    newPostBtn.addEventListener("click", function () {
      alert(
        "Funcionalidade de nova mensagem será implementada aqui!\nUm formulário será exibido para escrever sua mensagem."
      );
    });
  }

  // Simulação de nova enquete
  const newPollBtn = document.querySelector(".btn-new-poll");
  if (newPollBtn) {
    newPollBtn.addEventListener("click", function () {
      alert(
        "Funcionalidade de nova enquete será implementada aqui!\nVocê poderá criar sua própria enquete para a comunidade."
      );
    });
  }

  // Interação com posts (like/comentário)
  document.querySelectorAll(".btn-like").forEach((btn) => {
    btn.addEventListener("click", function () {
      const icon = this.querySelector("i");
      const count =
        this.querySelector(".btn-like span") || this.nextElementSibling;

      if (icon.classList.contains("far")) {
        icon.classList.remove("far");
        icon.classList.add("fas");
        this.style.color = "#e74c3c";

        // Incrementa contador
        const currentCount = parseInt(this.textContent.trim()) || 0;
        this.innerHTML = `<i class="fas fa-thumbs-up"></i> ${currentCount + 1}`;
      } else {
        icon.classList.remove("fas");
        icon.classList.add("far");
        this.style.color = "";

        // Decrementa contador
        const currentCount = parseInt(this.textContent.trim()) || 1;
        this.innerHTML = `<i class="far fa-thumbs-up"></i> ${currentCount - 1}`;
      }
    });
  });
});
