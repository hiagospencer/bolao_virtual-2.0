function sendToWhatsApp(produtoNome, produtoPreco, produtoImagemUrl, telefoneLoja = null) {
    const numeroDestino = telefoneLoja;

    const mensagem = `
      Olá, estou vindo diretamente do site Bolão Virtual e gostaria de comprar o produto:

      *${produtoNome}*
      *Preço*: R$ ${produtoPreco}

      🔗 *Imagem do Produto*: ${produtoImagemUrl}
    `;
    // ${window.location.origin}

    const url = `https://wa.me/+55${numeroDestino}?text=${encodeURIComponent(mensagem)}`;
    window.open(url, "_blank").focus();
}

// Opcional: Adicione efeitos de hover nos itens
document.addEventListener('DOMContentLoaded', function() {
    const items = document.querySelectorAll('.shop-item');

    items.forEach(item => {
        item.addEventListener('click', function(e) {
            // Evita abrir o WhatsApp se clicar em qualquer lugar do item
            if (!e.target.classList.contains('btn-add-to-cart')) {
                this.classList.toggle('item-expanded');
            }
        });
    });
});

// Atualiza o cabeçalho e cores ao mudar a loja
document.body.addEventListener('htmx:afterSwap', function(evt) {
    if (evt.detail.target.id === 'products-container') {
        updateLojaHeader();
    }
});

function updateLojaHeader() {
    const lojaSelect = document.getElementById('loja-filter');
    const selectedLojaId = lojaSelect.value;
    const lojaHeader = document.getElementById('loja-info-header');

    if (selectedLojaId === 'all') {
        // Reset para visualização de todas as lojas
        document.body.style.removeProperty('--loja-bg-color');
        document.body.style.removeProperty('--loja-secondary-color');
        return;
    }

    // Busca as cores da loja via AJAX (opcional)
    fetch(`/api/lojas/${selectedLojaId}/`)
        .then(response => response.json())
        .then(loja => {
            // Aplica as cores como variáveis CSS
            document.body.style.setProperty('--loja-bg-color', loja.cor_primaria);
            document.body.style.setProperty('--loja-secondary-color', loja.cor_secundaria);

            // Atualiza o cabeçalho
            lojaHeader.innerHTML = `
                <div class="loja-header-content" style="background-color: ${loja.cor_primaria}; color: ${loja.cor_texto};">
                    <div class="loja-logo">
                        ${loja.logo ? `<img src="${loja.logo}" alt="${loja.nome}">` : ''}
                    </div>
                    <div class="loja-details">
                        <h2>Produtos da ${loja.nome}</h2>
                        <p>${loja.descricao || 'Confira nossos produtos exclusivos'}</p>
                    </div>
                </div>
            `;
        })
        .catch(error => {
            console.error('Erro ao carregar dados da loja:', error);
        });
}

// Inicializa ao carregar a página
document.addEventListener('DOMContentLoaded', function() {
    updateLojaHeader();
});
