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

  // Configuração dos modals
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

  // Configura elementos dinâmicos
  setupDynamicElements();
});

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

  // Configura eventos de votação
  document.querySelectorAll('.poll-option:not(.view-only)').forEach(option => {
    option.addEventListener('click', function() {
      if (!this.classList.contains('voting-in-progress') &&
          !this.classList.contains('view-only')) {
        votePoll(this);
      }
    });
  });
}

function votePoll(optionElement) {
  const pollCard = optionElement.closest('.poll-card');
  const pollId = pollCard.dataset.pollId;
  const optionId = optionElement.dataset.optionId;

  // Debug: verifique os IDs antes de enviar
  console.log('Enviando voto para enquete:', pollId, 'opção:', optionId);

  fetch(`/interacao/votar-enquete/${pollId}/${optionId}/`, {
    method: 'POST',
    headers: {
      'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
      'Accept': 'application/json',
    },
    credentials: 'include'  // Importante para cookies de sessão
  })
  .then(response => {
    console.log('Resposta recebida, status:', response.status); // Debug
    if (!response.ok) {
      // Captura detalhes do erro HTTP
      return response.json().then(err => {
        throw new Error(err.message || `HTTP error! status: ${response.status}`);
      });
    }
    return response.json();
  })
  .then(data => {
    console.log('Dados recebidos:', data); // Debug
    if (data.success) {
      updatePollAfterVote(pollCard, data.results, optionId, data.total_votos);
    } else {
      throw new Error(data.message || 'Erro no servidor');
    }
  })
  .catch(error => {
    console.error('Erro completo:', error); // Debug detalhado
    let errorMsg = 'Erro de conexão';

    if (error.message.includes('Failed to fetch')) {
      errorMsg = 'Sem conexão com o servidor';
    } else if (error.message.includes('404')) {
      errorMsg = 'Enquete não encontrada';
    } else if (error.message) {
      errorMsg = error.message;
    }

    showPollError(pollCard, errorMsg);
  })
  .finally(() => {
    optionElement.classList.remove('voting-in-progress');
  });
}

function updatePollAfterVote(pollCard, results, votedOptionId, totalVotos) {
  // Atualiza todas as opções com as porcentagens
  results.forEach(result => {
    const option = pollCard.querySelector(`.poll-option[data-option-id="${result.id}"]`);
    const percentElement = option.querySelector('.option-percent');
    const resultBar = option.querySelector('.option-result');

    percentElement.textContent = `${result.percent}%`;
    percentElement.style.display = 'inline';
    resultBar.style.width = `${result.percent}%`;

    // Transforma todas as opções em modo visualização
    option.classList.add('view-only');
    option.style.pointerEvents = 'none';

    // Destaca a opção votada pelo usuário
    if (result.id == votedOptionId) {
      option.classList.add('user-vote');
      const badge = document.createElement('span');
      badge.className = 'your-vote-badge';
      badge.textContent = 'Seu voto';
      option.appendChild(badge);
    }
  });

  // Atualiza o total de votos
  const totalElement = pollCard.querySelector('.poll-meta span:first-child');
  if (totalElement) {
    totalElement.textContent = `Total de votos: ${totalVotos}`;
  }

  // Adiciona mensagem "Você já votou"
  const alreadyVoted = document.createElement('span');
  alreadyVoted.className = 'already-voted';
  alreadyVoted.textContent = 'Você já votou nesta enquete';
  pollCard.querySelector('.poll-meta').appendChild(alreadyVoted);
}

function showPollError(pollCard, message) {
  const errorElement = document.createElement('div');
  errorElement.className = 'poll-error';
  errorElement.textContent = message;

  // Insere antes das opções
  const optionsContainer = pollCard.querySelector('.poll-options');
  if (optionsContainer.firstChild) {
    optionsContainer.insertBefore(errorElement, optionsContainer.firstChild);
  } else {
    optionsContainer.appendChild(errorElement);
  }

  // Remove a mensagem após 5 segundos
  setTimeout(() => {
    errorElement.remove();
  }, 5000);
}
