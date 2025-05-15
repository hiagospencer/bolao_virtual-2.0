document.addEventListener("DOMContentLoaded", function () {
  // Verifica o estado de autenticação (simulado - substitua pela sua lógica real)
  const isAuthenticated = checkAuthStatus(); // Esta função deve ser implementada conforme seu backend

  // Elementos do DOM
  const loginBtn = document.querySelector(".btn-login");
  const registerBtn = document.querySelector(".btn-register");
  const loggedUser = document.getElementById("logged-user");
  const userAvatar = document.getElementById("user-avatar");
  const usernameDisplay = document.getElementById("username-display");
  const logoutBtn = document.getElementById("logout-btn");
  const palpitesDropdown = document.getElementById("palpites-dropdown");


  const dropdowns = document.querySelectorAll('.brasileirao-dropdown');

    dropdowns.forEach(dropdown => {
        const toggle = dropdown.querySelector('a:first-child');
        const menu = dropdown.querySelector('.brasileirao-dropdown-menu');

        if (toggle && menu) {
            toggle.addEventListener('click', function(e) {
                if (window.innerWidth <= 768) {
                    e.preventDefault();
                    dropdown.classList.toggle('active');

                    // Fecha outros dropdowns
                    document.addEventListener('click', function(e) {
                        if (window.innerWidth <= 768 && !e.target.closest('.brasileirao-dropdown')) {
                            dropdowns.forEach(d => d.classList.remove('active'));
                        }
                    });
                }
            });
        }
    });

  // Fecha dropdowns ao clicar fora (mobile)
  document.addEventListener('click', function(e) {
    if (window.innerWidth <= 768 && !e.target.closest('.brasileirao-dropdown')) {
      dropdowns.forEach(d => d.classList.remove('active'));
    }
  });

  // Funções simuladas - substitua pelas suas implementações reais
  function checkAuthStatus() {
    // Implemente a verificação real do estado de autenticação
    // Pode verificar cookies, localStorage, ou fazer uma requisição ao backend
    return localStorage.getItem("isAuthenticated") === "true"; // Exemplo simples
  }

  function getUserData() {
    // Implemente para buscar dados do usuário logado
    try {
      return JSON.parse(localStorage.getItem("userData")); // Exemplo simples
    } catch {
      return null;
    }
  }
});

// Alternar visibilidade da senha
document.querySelectorAll(".toggle-password").forEach((button) => {
  button.addEventListener("click", function () {
    const input = this.previousElementSibling;
    const icon = this.querySelector("i");

    if (input.type === "password") {
      input.type = "text";
      icon.classList.replace("fa-eye", "fa-eye-slash");
    } else {
      input.type = "password";
      icon.classList.replace("fa-eye-slash", "fa-eye");
    }
  });

});


// Menu Mobile
document.addEventListener('DOMContentLoaded', function() {
  const toggleBtn = document.getElementById("mobileMenuToggle");
  const closeBtn = document.getElementById('mobileMenuClose');
  const overlay = document.getElementById('mobileMenuOverlay');

  if (toggleBtn) {
    toggleBtn.addEventListener('click', function () {
      document.body.classList.add('mobile-menu-open');
    });
  }

  // Fechar menu
  function closeMobileMenu() {
    document.body.classList.remove('mobile-menu-open');
  }

  if (closeBtn) closeBtn.addEventListener('click', closeMobileMenu);
  if (overlay) overlay.addEventListener('click', closeMobileMenu);

  // Gerar tabela mobile
  function generateMobileTable() {
    const table = document.querySelector('.ranking-table');
    const mobileView = document.querySelector('.table-mobile-view');

    if (!table || !mobileView) return;

    const rows = table.querySelectorAll('tbody tr');
    let html = '';

    rows.forEach(row => {
      const position = row.cells[0].textContent.trim();
      const avatar = row.querySelector('.player-avatar')?.outerHTML || '';
      const name = row.cells[1].querySelector('span')?.textContent.trim() || '';
      const points = row.cells[3]?.textContent.trim() || '0';
      const exact = row.cells[4]?.textContent.trim() || '0';
      const wins = row.cells[5]?.textContent.trim() || '0';

      html += `
        <div class="mobile-player-card">
          <div class="mobile-player-header">
            <span class="mobile-player-position">${position}</span>
            ${avatar}
            <div class="mobile-player-info">${name}</div>
          </div>
          <div class="mobile-player-stats">
            <div class="mobile-stat-item">
              <span class="mobile-stat-label">Pontos:</span>
              <span class="mobile-stat-value">${points}</span>
            </div>
            <div class="mobile-stat-item">
              <span class="mobile-stat-label">Placar Exato:</span>
              <span class="mobile-stat-value">${exact}</span>
            </div>
            <div class="mobile-stat-item">
              <span class="mobile-stat-label">Vitórias:</span>
              <span class="mobile-stat-value">${wins}</span>
            </div>
          </div>
        </div>
      `;
    });

    mobileView.innerHTML = html;
  }

  // Executar quando o DOM estiver pronto
  generateMobileTable();

  // Atualizar quando a janela for redimensionada
  window.addEventListener('resize', function() {
    if (window.innerWidth > 768) {
      document.querySelector('.table-mobile-view').innerHTML = '';
    } else {
      generateMobileTable();
    }
  });
});
