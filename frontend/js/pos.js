/**
 * POS (Point of Sale) & Order Management Module
 */

const POS = (() => {
  let categories = [];
  let menuItems = [];
  let cart = [];
  let activeCategoryId = "all";
  let searchQuery = "";

  async function init() {
    await loadCategories();
    await loadMenuItems();
    await loadTableOptions();
    await loadCustomerOptions();
    renderCategories();
    renderMenuItems();
    renderCart();
  }

  async function loadCategories() {
    try {
      categories = await API.menu.getCategories();
    } catch (e) {
      console.warn("Could not load categories:", e);
      categories = [];
    }
  }

  async function loadMenuItems() {
    try {
      menuItems = await API.menu.getItems();
    } catch (e) {
      console.warn("Could not load menu items:", e);
      menuItems = [];
    }
  }

  async function loadTableOptions() {
    const tableSelect = document.getElementById("pos-table-select");
    if (!tableSelect) return;
    try {
      const tables = await API.tables.getAll();
      tableSelect.innerHTML = `<option value="">-- Select Table --</option>` +
        tables.map(t => `<option value="${t.id || t._id}">Table ${t.table_number} (${t.location || 'Main'} - Cap: ${t.capacity})</option>`).join("");
    } catch (e) {
      console.warn("Could not load tables:", e);
    }
  }

  async function loadCustomerOptions() {
    const customerSelect = document.getElementById("pos-customer-select");
    if (!customerSelect) return;
    try {
      const customers = await API.customers.getAll();
      customerSelect.innerHTML = `<option value="">Walk-in Guest</option>` +
        customers.map(c => `<option value="${c.id || c._id}">${c.name} (${c.phone})</option>`).join("");
    } catch (e) {
      console.warn("Could not load customers:", e);
    }
  }

  function renderCategories() {
    const container = document.getElementById("pos-category-tabs");
    if (!container) return;

    let html = `<button class="category-tab-btn ${activeCategoryId === 'all' ? 'active' : ''}" onclick="POS.filterCategory('all')">All Items (${menuItems.length})</button>`;
    
    categories.forEach(cat => {
      const catId = cat.id || cat._id;
      const count = menuItems.filter(i => (i.category_id === catId || (i.category_id && i.category_id.$oid === catId))).length;
      html += `<button class="category-tab-btn ${activeCategoryId === catId ? 'active' : ''}" onclick="POS.filterCategory('${catId}')">${cat.name} (${count})</button>`;
    });

    container.innerHTML = html;
  }

  function filterCategory(catId) {
    activeCategoryId = catId;
    renderCategories();
    renderMenuItems();
  }

  function search(query) {
    searchQuery = query.toLowerCase().trim();
    renderMenuItems();
  }

  function renderMenuItems() {
    const container = document.getElementById("pos-items-grid");
    if (!container) return;

    let filtered = menuItems;
    if (activeCategoryId !== "all") {
      filtered = filtered.filter(item => {
        const cId = item.category_id?.id || item.category_id?._id || item.category_id;
        return cId === activeCategoryId;
      });
    }

    if (searchQuery) {
      filtered = filtered.filter(item =>
        item.name.toLowerCase().includes(searchQuery) ||
        (item.description && item.description.toLowerCase().includes(searchQuery))
      );
    }

    if (filtered.length === 0) {
      container.innerHTML = `
        <div style="grid-column: 1 / -1; text-align: center; padding: 3rem; color: var(--text-dim);">
          <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🍽️</div>
          <p>No dishes found matching your selection.</p>
        </div>`;
      return;
    }

    container.innerHTML = filtered.map(item => {
      const id = item.id || item._id;
      const price = Number(item.price?.$numberDecimal || item.price || 0).toFixed(2);
      const isVeg = item.is_vegetarian;

      return `
        <div class="menu-card" onclick="POS.addToCart('${id}')">
          <div class="menu-card-top">
            <span class="menu-card-badge">${isVeg ? '🌱 Veg' : '🥩 Non-Veg'}</span>
            ${item.preparation_time ? `<span style="font-size: 0.7rem; color: var(--text-dim);">⏱️ ${item.preparation_time}m</span>` : ''}
          </div>
          <div>
            <div class="menu-card-name">${escapeHtml(item.name)}</div>
            <div class="menu-card-desc">${escapeHtml(item.description || 'Freshly prepared specialty dish.')}</div>
          </div>
          <div class="menu-card-bottom">
            <span class="menu-card-price">$${price}</span>
            <button class="menu-card-add-btn" title="Add to Order">+</button>
          </div>
        </div>
      `;
    }).join("");
  }

  function addToCart(itemId) {
    const item = menuItems.find(i => (i.id || i._id) === itemId);
    if (!item) return;

    const existing = cart.find(c => c.itemId === itemId);
    const price = Number(item.price?.$numberDecimal || item.price || 0);

    if (existing) {
      existing.quantity += 1;
    } else {
      cart.push({
        itemId,
        name: item.name,
        price,
        quantity: 1,
        instructions: ""
      });
    }

    renderCart();
    App.showToast(`Added "${item.name}" to cart`, "info");
  }

  function updateQty(itemId, delta) {
    const item = cart.find(c => c.itemId === itemId);
    if (!item) return;

    item.quantity += delta;
    if (item.quantity <= 0) {
      cart = cart.filter(c => c.itemId !== itemId);
    }
    renderCart();
  }

  function clearCart() {
    cart = [];
    renderCart();
  }

  function renderCart() {
    const container = document.getElementById("pos-cart-items");
    const countBadge = document.getElementById("pos-cart-count");
    const subtotalEl = document.getElementById("pos-cart-subtotal");
    const taxEl = document.getElementById("pos-cart-tax");
    const totalEl = document.getElementById("pos-cart-total");

    const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
    if (countBadge) countBadge.textContent = totalItems;

    if (!container) return;

    if (cart.length === 0) {
      container.innerHTML = `
        <div class="cart-empty">
          <div style="font-size: 2.5rem; opacity: 0.4;">🛒</div>
          <p style="font-weight: 500;">Your ticket is currently empty.</p>
          <span style="font-size: 0.75rem;">Click menu items to add them here</span>
        </div>`;
      if (subtotalEl) subtotalEl.textContent = "$0.00";
      if (taxEl) taxEl.textContent = "$0.00";
      if (totalEl) totalEl.textContent = "$0.00";
      return;
    }

    let subtotal = 0;

    container.innerHTML = cart.map(item => {
      const lineTotal = item.price * item.quantity;
      subtotal += lineTotal;

      return `
        <div class="cart-item-row">
          <div class="cart-item-details">
            <div class="cart-item-name">${escapeHtml(item.name)}</div>
            <div class="cart-item-unit-price">$${item.price.toFixed(2)} ea</div>
          </div>
          <div class="cart-item-qty-controls">
            <button class="qty-btn" onclick="POS.updateQty('${item.itemId}', -1)">-</button>
            <span class="qty-display">${item.quantity}</span>
            <button class="qty-btn" onclick="POS.updateQty('${item.itemId}', 1)">+</button>
          </div>
          <div class="cart-item-total">$${lineTotal.toFixed(2)}</div>
        </div>
      `;
    }).join("");

    const tax = subtotal * 0.05; // 5% standard tax
    const grandTotal = subtotal + tax;

    if (subtotalEl) subtotalEl.textContent = `$${subtotal.toFixed(2)}`;
    if (taxEl) taxEl.textContent = `$${tax.toFixed(2)}`;
    if (totalEl) totalEl.textContent = `$${grandTotal.toFixed(2)}`;
  }

  async function placeOrder(sendToKitchen = false) {
    if (cart.length === 0) {
      App.showToast("Your order is empty. Please add items first.", "warning");
      return;
    }

    const tableId = document.getElementById("pos-table-select")?.value || null;
    const customerId = document.getElementById("pos-customer-select")?.value || null;
    const orderType = document.getElementById("pos-type-select")?.value || "DINE_IN";
    const user = API.getCurrentUser();

    try {
      App.showLoader(true);

      // 1. Create Order
      const orderPayload = {
        customer_id: customerId || undefined,
        table_id: tableId || undefined,
        order_type: orderType,
        created_by: user?.email || user?.name || "pos_staff"
      };

      const newOrder = await API.orders.create(orderPayload);
      const orderId = newOrder.id || newOrder._id;

      // 2. Add Each Cart Item to the Order
      for (const item of cart) {
        await API.orders.addItem(orderId, {
          menu_item_id: item.itemId,
          quantity: item.quantity,
          special_instructions: item.instructions || undefined
        });
      }

      // 3. Recalculate Order Subtotal & Total
      await API.orders.recalculate(orderId);

      // 4. Update status to CONFIRMED
      await API.orders.updateStatus(orderId, "CONFIRMED");

      // 5. If Send to Kitchen is requested:
      if (sendToKitchen) {
        await API.kitchen.createTicket(orderId, "NORMAL");
        App.showToast(`Order #${newOrder.order_number || orderId.slice(-6)} placed & sent to Kitchen KDS!`, "success");
      } else {
        App.showToast(`Order #${newOrder.order_number || orderId.slice(-6)} placed successfully!`, "success");
      }

      // If a table was occupied, mark table as OCCUPIED
      if (tableId) {
        await API.tables.updateStatus(tableId, "OCCUPIED").catch(() => {});
      }

      clearCart();
      await loadTableOptions();
      await OrdersList.refresh();
      if (window.KitchenDisplay) KitchenDisplay.refresh();
      if (window.TablesView) TablesView.refresh();

    } catch (err) {
      App.showToast(`Order placement failed: ${err.message}`, "error");
    } finally {
      App.showLoader(false);
    }
  }

  function escapeHtml(text) {
    if (!text) return "";
    return String(text).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  }

  return {
    init,
    filterCategory,
    search,
    addToCart,
    updateQty,
    clearCart,
    placeOrder,
    refresh: init
  };
})();
