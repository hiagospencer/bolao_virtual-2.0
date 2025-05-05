document.addEventListener("DOMContentLoaded", function () {
  // Troca de abas
  const tabBtns = document.querySelectorAll(".tab-btn");
  const tabContents = document.querySelectorAll(".tab-content");

  tabBtns.forEach((btn) => {
    btn.addEventListener("click", function () {
      tabBtns.forEach((b) => b.classList.remove("active"));
      tabContents.forEach((c) => c.classList.remove("active"));
      this.classList.add("active");
      document.getElementById(this.dataset.tab).classList.add("active");
    });
  });

  // Funções genéricas para modais
  function openModal(modalId) {
    document.getElementById(modalId).style.display = "flex";
  }

  function closeModal(modalId) {
    document.getElementById(modalId).style.display = "none";
  }

  // Configuração dos modais
  const modals = {
    newPost: {
      openBtn: ".btn-new-post",
      modalId: "newPostModal"
    },
    newPoll: {
      openBtn: ".btn-new-poll",
      modalId: "newPollModal"
    },
    reply: {
      openBtn: ".btn-comment",
      modalId: "replyModal"
    }
  };

  // Configura eventos para cada modal
  Object.values(modals).forEach(modalConfig => {
    const openBtn = document.querySelector(modalConfig.openBtn);
    const modal = document.getElementById(modalConfig.modalId);

    if (openBtn && modal) {
      // Abrir modal
      openBtn.addEventListener("click", function() {
        // Para o modal de resposta, guarda o ID do tópico
        if (modalConfig.modalId === "replyModal") {
          const topicId = this.closest(".mural-post").dataset.topicId;
          document.getElementById("replyTopicId").value = topicId;
        }
        openModal(modalConfig.modalId);
      });

      // Fechar modal
      const closeBtns = modal.querySelectorAll(".modal-close, .btn-cancel");
      closeBtns.forEach(btn => {
        btn.addEventListener("click", () => closeModal(modalConfig.modalId));
      });

      // Fechar ao clicar fora
      modal.addEventListener("click", function(e) {
        if (e.target === modal) {
          closeModal(modalConfig.modalId);
        }
      });
    }
  });

  // Lógica específica para a enquete (adicionar/remover opções)
  const pollOptionsContainer = document.getElementById("pollOptionsContainer");
  const btnAddOption = document.getElementById("btnAddOption");

  if (btnAddOption && pollOptionsContainer) {
    btnAddOption.addEventListener("click", function() {
      const optionCount = pollOptionsContainer.children.length;
      const newOption = document.createElement("div");
      newOption.className = "poll-option-input";
      newOption.innerHTML = `
        <input type="text" name="opcoes[]" placeholder="Opção ${optionCount + 1}" required>
        <button type="button" class="btn-remove-option">&times;</button>
      `;
      pollOptionsContainer.appendChild(newOption);

      // Mostrar botões de remover em todas as opções
      document.querySelectorAll(".btn-remove-option").forEach(btn => {
        btn.style.display = "inline-block";
      });
    });

    // Remover opção
    pollOptionsContainer.addEventListener("click", function(e) {
      if (e.target.classList.contains("btn-remove-option")) {
        if (pollOptionsContainer.children.length > 2) {
          e.target.parentElement.remove();
        } else {
          alert("Uma enquete precisa ter pelo menos 2 opções!");
        }
      }
    });
  }

  // Interação com posts (like/comentário)
  document.querySelectorAll(".btn-like").forEach((btn) => {
    btn.addEventListener("click", function () {
      const icon = this.querySelector("i");
      if (icon.classList.contains("far")) {
        icon.classList.replace("far", "fas");
        this.style.color = "#e74c3c";
        const currentCount = parseInt(this.textContent.trim()) || 0;
        this.innerHTML = `<i class="fas fa-thumbs-up"></i> ${currentCount + 1}`;
      } else {
        icon.classList.replace("fas", "far");
        this.style.color = "";
        const currentCount = parseInt(this.textContent.trim()) || 1;
        this.innerHTML = `<i class="far fa-thumbs-up"></i> ${currentCount - 1}`;
      }
    });
  });
});

// Adicione esta função no seu JavaScript existente
function setupDynamicElements() {
  // Botão "Ver mais" comentários
  document.querySelectorAll('.btn-view-more').forEach(btn => {
    btn.addEventListener('click', function() {
      const commentsContainer = this.closest('.post-comments');
      commentsContainer.querySelectorAll('.comment:hidden').forEach(c => {
        c.style.display = 'block';
      });
      this.remove();
    });
  });

  // Votar em enquete
  document.querySelectorAll('.poll-option').forEach(option => {
    option.addEventListener('click', function() {
      if (this.classList.contains('voted')) return;

      const pollId = this.closest('.poll-card').dataset.pollId;
      const optionId = this.dataset.optionId;

      // Aqui você faria uma requisição AJAX para registrar o voto
      fetch(`/votar-enquete/${pollId}/${optionId}/`, {
        method: 'POST',
        headers: {
          'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
        }
      })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          // Atualiza a interface
          this.classList.add('voted');
          const percent = data.percent;
          this.querySelector('.option-result').style.width = `${percent}%`;
          this.querySelector('.option-percent').textContent = `${percent}%`;
        }
      });
    });
  });
}

// Chame esta função após carregar conteúdo dinâmico
document.addEventListener("DOMContentLoaded", function() {
  // ... seu código existente ...

  setupDynamicElements();
});
