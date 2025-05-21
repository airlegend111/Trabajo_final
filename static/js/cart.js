// Add to cart functionality
document.addEventListener('DOMContentLoaded', function() {
    // Get elements
    const addToCartModal = document.getElementById('addToCartModal');
    const modal = new bootstrap.Modal(addToCartModal);
    const addToCartForm = document.getElementById('add-to-cart-form');
    const cartCountElement = document.getElementById('cart-count');
    const confirmToast = new bootstrap.Toast(document.getElementById('cartToast'));

    // Quantity controls
    const quantityInput = document.getElementById('pizza-quantity');
    const decreaseBtn = document.getElementById('decrease-quantity');
    const increaseBtn = document.getElementById('increase-quantity');
    const modalSubtotal = document.getElementById('modal-subtotal');

    let currentPizzaPrice = 0;
    let currentPizzaId = 0;

    // Add click handlers to all "Add to Cart" buttons
    document.querySelectorAll('.add-to-cart-btn').forEach(button => {
        button.addEventListener('click', function() {
            const pizzaCard = this.closest('.pizza-card');
            currentPizzaId = pizzaCard.dataset.id;
            currentPizzaPrice = parseFloat(pizzaCard.dataset.price);

            // Populate modal with pizza details
            document.getElementById('modal-pizza-image').src = pizzaCard.dataset.image;
            document.getElementById('modal-pizza-name').textContent = pizzaCard.dataset.name;
            document.getElementById('modal-pizza-description').textContent = pizzaCard.dataset.description;
            document.getElementById('modal-pizza-size').textContent = pizzaCard.dataset.size;
            document.getElementById('modal-pizza-price').textContent = currentPizzaPrice.toFixed(2);
            
            // Reset quantity to 1
            quantityInput.value = 1;
            updateSubtotal();

            modal.show();
        });
    });

    // Quantity control handlers
    decreaseBtn.addEventListener('click', function() {
        const currentValue = parseInt(quantityInput.value);
        if (currentValue > 1) {
            quantityInput.value = currentValue - 1;
            updateSubtotal();
        }
    });

    increaseBtn.addEventListener('click', function() {
        const currentValue = parseInt(quantityInput.value);
        if (currentValue < 10) {
            quantityInput.value = currentValue + 1;
            updateSubtotal();
        }
    });

    quantityInput.addEventListener('change', function() {
        let value = parseInt(this.value);
        if (value < 1) {
            value = 1;
        } else if (value > 10) {
            value = 10;
        }
        this.value = value;
        updateSubtotal();
    });

    function updateSubtotal() {
        const quantity = parseInt(quantityInput.value);
        const subtotal = (currentPizzaPrice * quantity).toFixed(2);
        modalSubtotal.textContent = subtotal;
    }

    // Form submission handler
    addToCartForm.addEventListener('submit', function(e) {
        e.preventDefault();

        fetch('/products/cart/add/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            body: JSON.stringify({
                pizza_id: currentPizzaId,
                quantity: parseInt(quantityInput.value)
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                // Update cart count
                if (cartCountElement) {
                    cartCountElement.textContent = data.cart_count;
                }

                // Close modal and show success toast
                modal.hide();
                confirmToast.show();
            } else {
                alert(data.message || 'Error al añadir al carrito');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error al añadir al carrito');
        });
    });
});
