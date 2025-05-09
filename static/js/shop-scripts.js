function sendToWhatsApp(produtoNome, produtoPreco, produtoImagemUrl, telefoneLoja = null) {
    const numeroDestino = telefoneLoja;
    const mensagem = `
      Olá, gostaria de comprar o produto:

      *${produtoNome}*
      *Preço*: R$ ${produtoPreco}

      🔗 *Imagem do Produto*: ${window.location.origin}${produtoImagemUrl}
    `;

    const url = `https://wa.me/${numeroDestino}?text=${encodeURIComponent(mensagem)}`;
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
