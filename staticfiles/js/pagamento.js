// Temporizador de pagamento
let timeLeft = 30 * 60; // 30 minutos em segundos
const timerElement = document.getElementById('payment-timer');

function updateTimer() {
  const minutes = Math.floor(timeLeft / 60);
  const seconds = timeLeft % 60;

  timerElement.textContent = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;

  if (timeLeft > 0) {
    timeLeft--;
    setTimeout(updateTimer, 1000);
  } else {
    timerElement.textContent = "Expirado!";
    timerElement.style.color = "#e74c3c";
  }
}

// Iniciar o temporizador
updateTimer();

// Copiar chave PIX
document.getElementById('copy-pix-btn').addEventListener('click', function() {
  const pixKey = document.getElementById('pix-key').textContent;
  navigator.clipboard.writeText(pixKey).then(() => {
    const originalText = this.innerHTML;
    this.innerHTML = '<i class="fas fa-check"></i> Copiado!';

    setTimeout(() => {
      this.innerHTML = originalText;
    }, 2000);
  }).catch(err => {
    console.error('Erro ao copiar texto: ', err);
  });
});
