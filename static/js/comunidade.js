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

  // Sistema de respostas para posts principais
  document.querySelectorAll('.btn-comment').forEach(btn => {
    btn.addEventListener('click', function() {
      const formId = this.dataset.target;
      const form = document.getElementById(formId);

      // Esconde todos os outros formulários primeiro
      document.querySelectorAll('.reply-form').forEach(f => {
        if (f.id !== formId) f.style.display = 'none';
      });

      // Alterna o formulário atual
      form.style.display = form.style.display === 'none' ? 'block' : 'none';
    });
  });

  // Sistema de respostas para comentários
  document.querySelectorAll('.btn-reply-comment').forEach(btn => {
    btn.addEventListener('click', function() {
      const formId = this.dataset.target;
      const form = document.getElementById(formId);

      // Esconde todos os outros formulários de comentários
      document.querySelectorAll('.reply-comment-form').forEach(f => {
        if (f.id !== formId) f.style.display = 'none';
      });

      // Alterna o formulário atual
      form.style.display = form.style.display === 'none' ? 'block' : 'none';
    });
  });

  // Cancelar resposta a post principal
  document.querySelectorAll('.btn-cancel-reply').forEach(btn => {
    btn.addEventListener('click', function() {
      this.closest('.reply-form').style.display = 'none';
    });
  });

  // Cancelar resposta a comentário
  document.querySelectorAll('.btn-cancel-reply-comment').forEach(btn => {
    btn.addEventListener('click', function() {
      this.closest('.reply-comment-form').style.display = 'none';
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
  // Botões de editar/excluir post
  document.querySelectorAll('.btn-edit-post').forEach(btn => {
    btn.addEventListener('click', function() {
      const postId = this.dataset.postId;
      editPost(postId);
    });
  });

  document.querySelectorAll('.btn-delete-post').forEach(btn => {
    btn.addEventListener('click', function() {
      const postId = this.dataset.postId;
      if (confirm('Tem certeza que deseja excluir este post?')) {
        deletePost(postId);
      }
    });
  });

  // Botões de editar/excluir comentário
  document.querySelectorAll('.btn-edit-comment').forEach(btn => {
    btn.addEventListener('click', function() {
      const commentId = this.dataset.commentId;
      editComment(commentId);
    });
  });

  document.querySelectorAll('.btn-delete-comment').forEach(btn => {
    btn.addEventListener('click', function() {
      const commentId = this.dataset.commentId;
      if (confirm('Tem certeza que deseja excluir este comentário?')) {
        deleteComment(commentId);
      }
    });
  });
}

// Funções para manipulação de posts e comentários
function editPost(postId) {
  const postElement = document.querySelector(`.mural-post[data-topic-id="${postId}"]`);
  const postTitle = postElement.querySelector('.post-content h3').textContent;
  const postContent = postElement.querySelector('.post-content p').textContent;

  // Preenche o modal de edição (você precisará criar este modal)
  document.getElementById('editPostTitle').value = postTitle;
  document.getElementById('editPostContent').value = postContent;
  document.getElementById('editPostId').value = postId;

  openModal('editPostModal');
}

function deletePost(postId) {
  fetch(`/interacao/excluir-post/${postId}/`, {
    method: 'POST',
    headers: {
      'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
      'Content-Type': 'application/json',
    },
    credentials: 'same-origin'
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      document.querySelector(`.mural-post[data-topic-id="${postId}"]`).remove();
    } else {
      alert(data.message || 'Erro ao excluir post');
    }
  })
  .catch(error => {
    console.error('Error:', error);
    alert('Erro de conexão');
  });
}

function deleteComment(commentId) {
  fetch(`/interacao/excluir-comentario/${commentId}/`, {
    method: 'POST',
    headers: {
      'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
      'Content-Type': 'application/json',
    },
    credentials: 'same-origin'
  })
  .then(response => response.json())
  .then(data => {
    if (data.success) {
      document.querySelector(`.comment[data-comment-id="${commentId}"]`).remove();
    } else {
      alert(data.message || 'Erro ao excluir comentário');
    }
  })
  .catch(error => {
    console.error('Error:', error);
    alert('Erro de conexão');
  });
}

function votePoll(optionElement) {
  const pollCard = optionElement.closest('.poll-card');
  const pollId = pollCard.dataset.pollId;
  const optionId = optionElement.dataset.optionId;

  // Desativa temporariamente todos os botões
  pollCard.querySelectorAll('.poll-option').forEach(opt => {
    opt.style.pointerEvents = 'none';
  });

  // Mostra indicador de carregamento
  optionElement.classList.add('voting-in-progress');

  fetch(`/interacao/votar-enquete/${pollId}/${optionId}/`, {
    method: 'POST',
    headers: {
      'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
      'Content-Type': 'application/json',
    },
    credentials: 'same-origin'
  })
  .then(response => {
    if (!response.ok) throw new Error('Erro na requisição');
    return response.json();
  })
  .then(data => {
    if (data.success) {
      updatePollAfterVote(pollCard, data.results, optionId, data.total_votos);
    } else {
      showPollError(pollCard, data.message || 'Erro ao registrar voto');
    }
  })
  .catch(error => {
    console.error('Error:', error);
    showPollError(pollCard, 'Erro de conexão com o servidor');
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
