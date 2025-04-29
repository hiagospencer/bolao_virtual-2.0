document.addEventListener('DOMContentLoaded', function() {
  // Elementos do DOM
  const cartSidebar = document.getElementById('cartSidebar');
  const toggleCartBtn = document.getElementById('toggleCart');
  const closeCartBtn = document.getElementById('closeCart');
  const cartItemsContainer = document.querySelector('.cart-items');
  const cartTotal = document.querySelector('.total-price');
  const checkoutBtn = document.querySelector('.btn-checkout');
  const cartCount = document.querySelector('.cart-count');

  // Carrinho de compras
  let cart = [];

  // Abrir/fechar carrinho
  toggleCartBtn.addEventListener('click', function() {
    cartSidebar.classList.add('open');
  });

  closeCartBtn.addEventListener('click', function() {
    cartSidebar.classList.remove('open');
  });

  // Adicionar item ao carrinho
  document.querySelectorAll('.btn-add-to-cart').forEach(button => {
    button.addEventListener('click', function() {
      const itemElement = this.closest('.shop-item');
      const item = {
        id: itemElement.dataset.id || Date.now().toString(),
        name: itemElement.querySelector('h3').textContent,
        price: parseFloat(itemElement.querySelector('.price').textContent.replace('R$ ', '').replace(',', '.')),
        image: itemElement.querySelector('.item-image').innerHTML,
        quantity: 1
      };

      addToCart(item);
      updateCartUI();
      cartSidebar.classList.add('open');
    });
  });

  // Função para adicionar item ao carrinho
  function addToCart(item) {
    const existingItem = cart.find(cartItem => cartItem.id === item.id);

    if (existingItem) {
      existingItem.quantity += 1;
    } else {
      cart.push(item);
    }
  }

  // Atualizar a interface do carrinho
  function updateCartUI() {
    // Limpar carrinho
    cartItemsContainer.innerHTML = '';

    if (cart.length === 0) {
      cartItemsContainer.innerHTML = `
        <div class="empty-cart">
          <i class="fas fa-shopping-basket"></i>
          <p>Seu carrinho está vazio</p>
        </div>
      `;
      checkoutBtn.disabled = true;
    } else {
      let total = 0;

      cart.forEach(item => {
        total += item.price * item.quantity;

        const cartItemElement = document.createElement('div');
        cartItemElement.className = 'cart-item';
        cartItemElement.innerHTML = `
          <div class="cart-item-image">${item.image}</div>
          <div class="cart-item-details">
            <h4>${item.name}</h4>
            <div class="cart-item-price">R$ ${item.price.toFixed(2).replace('.', ',')}</div>
            <div class="cart-item-quantity">
              <button class="btn-quantity minus" data-id="${item.id}">-</button>
              <span>${item.quantity}</span>
              <button class="btn-quantity plus" data-id="${item.id}">+</button>
            </div>
          </div>
          <button class="btn-remove-item" data-id="${item.id}">
            <i class="fas fa-trash"></i>
          </button>
        `;

        cartItemsContainer.appendChild(cartItemElement);
      });

      // Atualizar total
      cartTotal.textContent = `R$ ${total.toFixed(2).replace('.', ',')}`;
      checkoutBtn.disabled = false;
    }

    // Atualizar contador
    const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
    cartCount.textContent = totalItems;
  }

  // Delegar eventos para quantidade e remoção
  cartItemsContainer.addEventListener('click', function(e) {
    const target = e.target.closest('.btn-quantity') || e.target.closest('.btn-remove-item');

    if (!target) return;

    const itemId = target.dataset.id;
    const itemIndex = cart.findIndex(item => item.id === itemId);

    if (target.classList.contains('minus')) {
      if (cart[itemIndex].quantity > 1) {
        cart[itemIndex].quantity -= 1;
      } else {
        cart.splice(itemIndex, 1);
      }
    } else if (target.classList.contains('plus')) {
      cart[itemIndex].quantity += 1;
    } else if (target.classList.contains('btn-remove-item')) {
      cart.splice(itemIndex, 1);
    }

    updateCartUI();
  });

  // Finalizar compra
  checkoutBtn.addEventListener('click', function() {
    alert('Compra finalizada com sucesso! Total: ' + cartTotal.textContent);
    cart = [];
    updateCartUI();
    cartSidebar.classList.remove('open');
  });

  // Filtros da loja (simulação)
  document.getElementById('category-filter').addEventListener('change', function() {
    const category = this.value;

    document.querySelectorAll('.shop-item').forEach(item => {
      if (category === 'all' || item.dataset.category === category) {
        item.style.display = 'block';
      } else {
        item.style.display = 'none';
      }
    });
  });

  // Ordenação (simulação)
  document.getElementById('sort-by').addEventListener('change', function() {
    const sortBy = this.value;
    const container = document.querySelector('.shop-grid');
    const items = Array.from(document.querySelectorAll('.shop-item'));

    items.sort((a, b) => {
      const priceA = parseFloat(a.querySelector('.price').textContent.replace('R$ ', '').replace(',', '.'));
      const priceB = parseFloat(b.querySelector('.price').textContent.replace('R$ ', '').replace(',', '.'));

      if (sortBy === 'price-asc') return priceA - priceB;
      if (sortBy === 'price-desc') return priceB - priceA;
      return 0; // Ordem padrão para outros filtros
    });

    // Reordenar os itens
    items.forEach(item => container.appendChild(item));
  });
});
