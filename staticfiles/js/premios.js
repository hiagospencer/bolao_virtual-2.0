document.addEventListener('DOMContentLoaded', function() {
  // Troca de abas
  const tabBtns = document.querySelectorAll('.tab-btn');
  const tabContents = document.querySelectorAll('.tab-content');

  tabBtns.forEach(btn => {
    btn.addEventListener('click', function() {
      // Remove classe active de todos os botões e conteúdos
      tabBtns.forEach(b => b.classList.remove('active'));
      tabContents.forEach(c => c.classList.remove('active'));

      // Adiciona classe active ao botão clicado
      this.classList.add('active');

      // Mostra o conteúdo correspondente
      const tabId = this.dataset.tab;
      document.getElementById(tabId).classList.add('active');
    });
  });

  // Filtros de prêmios disponíveis
  const typeFilter = document.getElementById('type-filter');
  const difficultyFilter = document.getElementById('difficulty-filter');

  if(typeFilter && difficultyFilter) {
    typeFilter.addEventListener('change', filterRewards);
    difficultyFilter.addEventListener('change', filterRewards);
  }

  function filterRewards() {
    const type = typeFilter.value;
    const difficulty = difficultyFilter.value;

    console.log(`Filtrando por: Tipo=${type}, Dificuldade=${difficulty}`);
    // Aqui você implementaria a lógica real de filtragem
    // Por enquanto é apenas uma simulação
  }

  // Efeito de hover nos cards de troféus
  const trophyCards = document.querySelectorAll('.trophy-card');
  trophyCards.forEach(card => {
    card.addEventListener('mouseenter', function() {
      const icon = this.querySelector('.trophy-icon i');
      if(icon) {
        icon.style.transform = 'scale(1.1)';
        icon.style.transition = 'transform 0.3s';
      }
    });

    card.addEventListener('mouseleave', function() {
      const icon = this.querySelector('.trophy-icon i');
      if(icon) {
        icon.style.transform = 'scale(1)';
      }
    });
  });

  // Simulação de progresso (pode ser substituído por dados reais)
  simulateProgress();
});

function simulateProgress() {
  const progressBars = document.querySelectorAll('.progress-fill');

  progressBars.forEach(bar => {
    const targetWidth = bar.style.width;
    bar.style.width = '0%';

    setTimeout(() => {
      bar.style.transition = 'width 1.5s ease-out';
      bar.style.width = targetWidth;
    }, 200);
  });
}
