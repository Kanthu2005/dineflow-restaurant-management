/**
 * Menu Administration Module (Categories & Dishes)
 */

const MenuMgmt = (() => {
  let categories = [];
  let items = [];

  async function init() {
    await refresh();
  }

  async function refresh() {
    await loadCategories();
    await loadItems();
    render();
  }

  async function loadCategories() {
    try {
      categories = await API.menu.getCategories();
    } catch (e) {
      console.warn("Could not load categories:", e);
      categories = [];
    }
  }

  async function loadItems() {
    try {
      items = await API.menu.getItems();
    } catch (e) {
      console.warn("Could not load items:", e);
      items = [];
    }
  }

  function render() {
    renderItemsTable();
    renderCategoriesTable();
  }

  function renderItemsTable() {
    const tableBody = document.getElementById("menu-items-table-body");
    const countBadge = document.getElementById("menu-items-count-badge");
    if (!tableBody) return;

    if (countBadge) countBadge.textContent = `${items.length} Dishes`;

    if (items.length === 0) {
      tableBody.innerHTML = `
        <tr>
          <td colspan="7" style="text-align: center; padding: 3rem; color: var(--text-dim);">
            No menu items found.
          </td>
        </tr>`;
      return;
    }

    tableBody.innerHTML = items.map(item => {
      const id = item.id || item._id;
      const price = Number(item.price?.$numberDecimal || item.price || 0).toFixed(2);
      const isAvailable = item.is_available !== false;
      const isVeg = item.is_vegetarian;

      return `
        <tr>
          <td style="font-weight: 700;">${item.name}</td>
          <td><span class="badge ${isVeg ? 'badge-green' : 'badge-amber'}">${isVeg ? 'Vegetarian' : 'Non-Veg'}</span></td>
          <td style="font-weight: 700; color: var(--accent-primary);">$${price}</td>
          <td>${item.preparation_time || 15} mins</td>
          <td>
            <span class="badge ${isAvailable ? 'badge-green' : 'badge-red'}">
              ${isAvailable ? 'Available' : 'Sold Out'}
            </span>
          </td>
          <td>
            <button class="btn btn-secondary btn-sm" onclick="MenuMgmt.toggleAvailability('${id}', ${isAvailable})">
              ${isAvailable ? 'Mark Sold Out' : 'Mark Available'}
            </button>
          </td>
        </tr>
      `;
    }).join("");
  }

  function renderCategoriesTable() {
    const tableBody = document.getElementById("menu-cat-table-body");
    if (!tableBody) return;

    tableBody.innerHTML = categories.map(cat => {
      const id = cat.id || cat._id;
      return `
        <tr>
          <td style="font-weight: 700;">${cat.name}</td>
          <td style="color: var(--text-dim);">${cat.description || '-'}</td>
        </tr>
      `;
    }).join("");
  }

  function openAddItemModal() {
    // Populate categories select
    const select = document.getElementById("dish-category-select");
    if (select) {
      select.innerHTML = categories.map(c => `
        <option value="${c.id || c._id}">${c.name}</option>
      `).join("");
    }
    App.openModal("add-dish-modal");
  }

  async function submitAddItem() {
    const name = document.getElementById("dish-name-input")?.value?.trim();
    const categoryId = document.getElementById("dish-category-select")?.value;
    const price = Number(document.getElementById("dish-price-input")?.value || 0);
    const prepTime = parseInt(document.getElementById("dish-prep-input")?.value || 15, 10);
    const isVeg = document.getElementById("dish-veg-input")?.checked || false;
    const desc = document.getElementById("dish-desc-input")?.value?.trim() || "";

    if (!name || !categoryId || price <= 0) {
      App.showToast("Dish name, category, and price are required", "warning");
      return;
    }

    try {
      App.showLoader(true);
      await API.menu.createItem({
        name,
        category_id: categoryId,
        price,
        preparation_time: prepTime,
        is_vegetarian: isVeg,
        is_available: true,
        description: desc
      });

      App.showToast(`Dish "${name}" added to menu!`, "success");
      App.closeModal("add-dish-modal");
      await refresh();
      if (window.POS) POS.refresh();
    } catch (e) {
      App.showToast(`Error adding dish: ${e.message}`, "error");
    } finally {
      App.showLoader(false);
    }
  }

  function openAddCategoryModal() {
    App.openModal("add-category-modal");
  }

  async function submitAddCategory() {
    const name = document.getElementById("cat-name-input")?.value?.trim();
    const desc = document.getElementById("cat-desc-input")?.value?.trim() || "";

    if (!name) {
      App.showToast("Category name is required", "warning");
      return;
    }

    try {
      App.showLoader(true);
      await API.menu.createCategory({ name, description: desc });
      App.showToast(`Category "${name}" created!`, "success");
      App.closeModal("add-category-modal");
      await refresh();
      if (window.POS) POS.refresh();
    } catch (e) {
      App.showToast(`Error creating category: ${e.message}`, "error");
    } finally {
      App.showLoader(false);
    }
  }

  async function toggleAvailability(itemId, current) {
    try {
      App.showLoader(true);
      await API.menu.updateItem(itemId, { is_available: !current });
      App.showToast("Dish availability updated", "success");
      await refresh();
      if (window.POS) POS.refresh();
    } catch (e) {
      App.showToast(`Error: ${e.message}`, "error");
    } finally {
      App.showLoader(false);
    }
  }

  return {
    init,
    refresh,
    openAddItemModal,
    submitAddItem,
    openAddCategoryModal,
    submitAddCategory,
    toggleAvailability
  };
})();
