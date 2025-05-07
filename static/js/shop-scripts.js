const sendToWhatSapp = (produtoNome, produtoPreco, produtoImagemUrl) => {
    const errorMensagem = document.getElementById("errorMensagem");

    const numeroDestino = "+558481548139";
    const mensagem = `
      Olá, gostaria de comprar o produto:

      *${produtoNome}*
      Preço: R$ ${produtoPreco}

      🔗 *Imagem do Produto*: ${produtoImagemUrl}
    `;

    const url = `https://wa.me/${numeroDestino}?text=${encodeURIComponent(mensagem)}`;

    window.open(url, "_blank").focus();

};
