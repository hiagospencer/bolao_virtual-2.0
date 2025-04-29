// auth-control.js
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

  // Atualiza o header conforme o estado de autenticação
  function updateAuthUI() {
    if (isAuthenticated) {
      // Usuário logado - mostra menu do usuário
      loginBtn.style.display = "none";
      registerBtn.style.display = "none";
      loggedUser.style.display = "block";

      // Carrega dados do usuário (substitua pelos dados reais)
      const userData = getUserData(); // Implemente conforme seu backend
      if (userData) {
        userAvatar.src = userData.avatar || "https://via.placeholder.com/30";
        usernameDisplay.textContent = userData.username || "Usuário";
      }

      // Mostra dropdown completo para palpites
      if (palpitesDropdown) {
        palpitesDropdown.style.display = "block";
      }
    } else {
      // Usuário não logado - mostra botões de login/cadastro
      loginBtn.style.display = "block";
      registerBtn.style.display = "block";
      loggedUser.style.display = "none";

      // Esconde dropdown de palpites
      if (palpitesDropdown) {
        palpitesDropdown.style.display = "none";
      }
    }
  }

  // Função de logout
  if (logoutBtn) {
    logoutBtn.addEventListener("click", function (e) {
      e.preventDefault();
      logoutUser(); // Implemente esta função conforme seu backend
      window.location.href = "/"; // Redireciona para home após logout
    });
  }

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

  function logoutUser() {
    // Implemente a lógica real de logout
    localStorage.removeItem("isAuthenticated");
    localStorage.removeItem("userData");
  }

  // Inicializa a UI
  updateAuthUI();
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

// Máscara para WhatsApp
// document
//   .getElementById("register-whatsapp")
//   .addEventListener("input", function (e) {
//     let value = e.target.value.replace(/\D/g, "");
//     if (value.length > 11) value = value.substring(0, 11);

//     if (value.length > 0) {
//       value = value.replace(/^(\d{0,2})(\d{0,5})(\d{0,4})/, "($1) $2-$3");
//     }

//     e.target.value = value;
//   });

// Verificador de força da senha
// document
//   .getElementById("register-whatsapp")
//   .addEventListener("input", function (e) {
//     const password = e.target.value;
//     const strengthBars = document.querySelectorAll(".strength-bar");
//     const strengthText = document.querySelector(".strength-text");

//     // Reset
//     strengthBars.forEach((bar) => (bar.style.backgroundColor = "#ddd"));
//     strengthText.textContent = "Força da senha";
//     strengthText.style.color = "#666";

//     if (password.length === 0) return;

//     let strength = 0;

//     // Verifica comprimento
//     if (password.length >= 8) strength++;
//     if (password.length >= 12) strength++;

//     // Verifica complexidade
//     if (/[A-Z]/.test(password)) strength++;
//     if (/[0-9]/.test(password)) strength++;
//     if (/[^A-Za-z0-9]/.test(password)) strength++;

//     // Atualiza visualização
//     if (strength > 0) {
//       strengthBars[0].style.backgroundColor = "#ff4d4d";
//       strengthText.textContent = "Fraca";
//       strengthText.style.color = "#ff4d4d";
//     }

//     if (strength >= 3) {
//       strengthBars[0].style.backgroundColor = "#ffa500";
//       strengthBars[1].style.backgroundColor = "#ffa500";
//       strengthText.textContent = "Média";
//       strengthText.style.color = "#ffa500";
//     }

//     if (strength >= 5) {
//       strengthBars[0].style.backgroundColor = "#4CAF50";
//       strengthBars[1].style.backgroundColor = "#4CAF50";
//       strengthBars[2].style.backgroundColor = "#4CAF50";
//       strengthText.textContent = "Forte";
//       strengthText.style.color = "#4CAF50";
//     }
//   });


  // Cria a visualização mobile da tabela
// function createMobileView() {
//   const table = document.querySelector('.ranking-table');
//   const mobileView = document.querySelector('.table-mobile-view');

//   if (!table || !mobileView) return;

//   const rows = table.querySelectorAll('tbody tr');
//   let mobileHTML = '';

//   rows.forEach((row, index) => {
//     const position = row.cells[0].textContent.trim();
//     const avatar = row.querySelector('.player-avatar')?.outerHTML || '';
//     const name = row.cells[1].textContent.trim();
//     const points = row.cells[3].textContent;
//     const exactScores = row.cells[4]?.textContent || '0';
//     const victories = row.cells[5]?.textContent || '0';

//     mobileHTML += `
//       <div class="mobile-player-card">
//         <div class="mobile-player-header">
//           <span class="mobile-player-position">${position}</span>
//           ${avatar}
//           <span>${name}</span>
//         </div>
//         <div class="mobile-player-stats">
//           <div class="mobile-stat-item">
//             <span class="mobile-stat-label">Pontos:</span>
//             <span>${points}</span>
//           </div>
//           <div class="mobile-stat-item">
//             <span class="mobile-stat-label">Placar Exato:</span>
//             <span>${exactScores}</span>
//           </div>
//           <div class="mobile-stat-item">
//             <span class="mobile-stat-label">Vitórias:</span>
//             <span>${victories}</span>
//           </div>
//           <div class="mobile-stat-item">
//             <span class="mobile-stat-label">Posição:</span>
//             <span>${index + 1}º</span>
//           </div>
//         </div>
//       </div>
//     `;
//   });

//   mobileView.innerHTML = mobileHTML;
//   console.log(table)
//   console.log(mobileView)
// }

// // Executa quando o DOM estiver carregado
// document.addEventListener('DOMContentLoaded', createMobileView);

// Controle do menu mobile
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
