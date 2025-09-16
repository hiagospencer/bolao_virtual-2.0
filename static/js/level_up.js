document.addEventListener('DOMContentLoaded', function() {
    const levelUpData = document.getElementById('level-up-data');
    if (!levelUpData) return;

    const levelUp = levelUpData.dataset.levelUp === 'True';
    const newLevel = parseInt(levelUpData.dataset.newLevel) || 0;

    if (levelUp && newLevel > 0) {
        showLevelUpAnimation(newLevel);
    }
});

function showLevelUpAnimation(newLevel) {
    // Cria o elemento da animação
    const animation = document.createElement('div');
    animation.className = 'level-up-animation';
    animation.innerHTML = `
        <div class="level-up-title">Level Up!</div>
        <div class="level-up-level">${newLevel}</div>
        <div class="level-up-progress">
            <div class="level-up-progress-bar"></div>
        </div>
    `;

    document.body.appendChild(animation);

    // Mostra a animação
    setTimeout(() => {
        animation.style.display = 'block';
        createConfetti();

        // Anima a barra de progresso
        setTimeout(() => {
            const progressBar = animation.querySelector('.level-up-progress-bar');
            if (progressBar) {
                progressBar.style.width = '100%';
            }
        }, 500);
    }, 100);

    // Remove após 4 segundos
    setTimeout(() => {
        animation.style.opacity = '0';
        setTimeout(() => {
            animation.remove();
        }, 500);
    }, 4000);
}

function createConfetti() {
    const colors = ['gold', 'orange', 'white', '#ffcc00', '#ffdd33'];

    for (let i = 0; i < 150; i++) {
        const confetti = document.createElement('div');
        confetti.className = 'confetti';
        confetti.style.left = Math.random() * 100 + 'vw';
        confetti.style.top = -10 + 'px';
        confetti.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
        confetti.style.width = Math.random() * 10 + 5 + 'px';
        confetti.style.height = Math.random() * 10 + 5 + 'px';
        confetti.style.borderRadius = Math.random() > 0.5 ? '50%' : '0';

        document.body.appendChild(confetti);

        animateConfetti(confetti);
    }
}

function animateConfetti(element) {
    const animationDuration = 2000 + Math.random() * 3000;
    const xMovement = (Math.random() - 0.5) * 200;

    const keyframes = [
        {
            transform: 'translate(0, 0) rotate(0deg)',
            opacity: 0
        },
        {
            transform: `translate(${xMovement}px, 20vh) rotate(180deg)`,
            opacity: 1
        },
        {
            transform: `translate(${xMovement * 1.5}px, 100vh) rotate(360deg)`,
            opacity: 0
        }
    ];

    const animation = element.animate(keyframes, {
        duration: animationDuration,
        easing: 'cubic-bezier(0.1, 0.8, 0.9, 1)'
    });

    animation.onfinish = () => element.remove();
}
