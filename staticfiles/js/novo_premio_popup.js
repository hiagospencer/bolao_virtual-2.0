document.addEventListener('DOMContentLoaded', function() {
    const popup = document.getElementById('novoPremioPopup');
    const closeBtn = document.querySelector('.np-close-btn');
    const closeBtnFooter = document.querySelector('.np-btn-close');
    const disableBtn = document.querySelector('.np-btn-disable');
    const ultimoPremioId = "{{ ultimo_premio.id }}"; // Passado pelo context

    // Verifica preferências do usuário
    const popupDisabled = localStorage.getItem('np_popup_disabled');
    const ultimoPremioVisto = localStorage.getItem('np_ultimo_premio');

    // Mostra popup se:
    // 1. Não está desativado
    // 2. É um prêmio novo
    if (popupDisabled !== 'true' && ultimoPremioVisto !== ultimoPremioId) {
        setTimeout(() => {
            popup.classList.add('np-active');
        }, 3000); // Mostra após 3 segundos
    }

    // Fechar popup (botão X e botão Fechar)
    [closeBtn, closeBtnFooter].forEach(btn => {
        btn.addEventListener('click', function() {
            popup.classList.remove('np-active');
            localStorage.setItem('np_ultimo_premio', ultimoPremioId);
        });
    });

    // Desativar popups futuros
    disableBtn.addEventListener('click', function() {
        popup.classList.remove('np-active');
        localStorage.setItem('np_popup_disabled', 'true');
        localStorage.setItem('np_ultimo_premio', ultimoPremioId);
    });

    // Fechar ao clicar fora
    popup.addEventListener('click', function(e) {
        if (e.target === this) {
            popup.classList.remove('np-active');
            localStorage.setItem('np_ultimo_premio', ultimoPremioId);
        }
    });
});
