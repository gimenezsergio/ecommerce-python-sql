// URL base de nuestro servidor Backend en Python Flask con Base de Datos SQL
const BASE_URL = 'http://localhost:5000/api';

function buildQueryParams(options = {}) {
    const params = new URLSearchParams();
    if (options.sort && (options.sort === 'asc' || options.sort === 'desc')) {
        params.append('sort', options.sort);
    }
    if (options.limit && !isNaN(options.limit) && Number(options.limit) > 0) {
        params.append('limit', options.limit);
    }
    const queryString = params.toString();
    return queryString ? `?${queryString}` : '';
}

export async function fetchProducts(options = {}) {
    try {
        const query = buildQueryParams(options);
        const response = await fetch(`${BASE_URL}/products${query}`);
        if (!response.ok) {
            throw new Error(`Error HTTP: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('Fallo en la obtención de productos:', error);
        throw error;
    }
}

export async function fetchProductsByCategory(category, options = {}) {
    try {
        const query = buildQueryParams(options);
        const response = await fetch(`${BASE_URL}/products/category/${encodeURIComponent(category)}${query}`);
        if (!response.ok) {
            throw new Error(`Error HTTP Categoría: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error(`Fallo en la obtención de productos para categoría ${category}:`, error);
        throw error;
    }
}

export async function fetchCategories() {
    try {
        const response = await fetch(`${BASE_URL}/products/categories`);
        if (!response.ok) {
            throw new Error(`Error HTTP Categorías: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('Fallo en la obtención de categorías:', error);
        throw error;
    }
}

export async function fetchProductDetail(productId) {
    try {
        const response = await fetch(`${BASE_URL}/products/${productId}`);
        if (!response.ok) {
            throw new Error(`Error HTTP Detalle: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('Fallo en la obtención de detalle del producto:', error);
        throw error;
    }
}

export async function fetchUserProfile(userId) {
    try {
        const response = await fetch(`${BASE_URL}/users/${userId}`);
        if (!response.ok) {
            throw new Error(`Error HTTP Perfil: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('Fallo en la obtención del perfil de usuario:', error);
        throw error;
    }
}

export async function createCartOrder(cartItems, userId = 1) {
    try {
        if (!Array.isArray(cartItems) || cartItems.length === 0) {
            throw new Error('El carrito no puede estar vacío');
        }

        const formattedProducts = cartItems.map(item => ({
            productId: Number(item.id),
            quantity: Number(item.quantity) || 1
        }));

        const currentDate = new Date().toISOString().split('T')[0];

        const payload = {
            userId: Number(userId),
            date: currentDate,
            products: formattedProducts
        };

        const response = await fetch(`${BASE_URL}/carts`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            throw new Error(`Error HTTP al crear la orden de compra: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error('Fallo en la creación de la orden de compra:', error);
        throw error;
    }
}
