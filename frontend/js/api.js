/**
 * DineFlow API Service Layer
 * Seamlessly connects UI with FastAPI backend endpoints.
 */

const API = (() => {
  // Determine default base URL
  const isSameOriginBackend = window.location.port === "8000" && window.location.pathname.startsWith("/app");
  const defaultBaseUrl = isSameOriginBackend ? "/api" : "http://localhost:8000/api";
  
  let baseUrl = localStorage.getItem("dineflow_api_url") || defaultBaseUrl;

  const getBaseUrl = () => baseUrl;
  const setBaseUrl = (url) => {
    baseUrl = url.replace(/\/+$/, "");
    localStorage.setItem("dineflow_api_url", baseUrl);
  };

  const getToken = () => localStorage.getItem("dineflow_token");
  const setToken = (token) => {
    if (token) localStorage.setItem("dineflow_token", token);
    else localStorage.removeItem("dineflow_token");
  };

  const getCurrentUser = () => {
    try {
      const u = localStorage.getItem("dineflow_user");
      return u ? JSON.parse(u) : null;
    } catch {
      return null;
    }
  };

  const setCurrentUser = (user) => {
    if (user) localStorage.setItem("dineflow_user", JSON.stringify(user));
    else localStorage.removeItem("dineflow_user");
  };

  // Core Request Helper
  async function request(endpoint, options = {}) {
    const url = `${baseUrl}${endpoint.startsWith("/") ? "" : "/"}${endpoint}`;
    const token = getToken();

    const headers = {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    };

    if (token) {
      headers["Authorization"] = `Bearer ${token}`;
    }

    const config = {
      ...options,
      headers,
    };

    if (options.body && typeof options.body === "object") {
      config.body = JSON.stringify(options.body);
    }

    try {
      const response = await fetch(url, config);
      const data = await response.json().catch(() => null);

      if (!response.ok) {
        const errorMsg = data?.detail || data?.message || data?.error || `Request failed with status ${response.status}`;
        const err = new Error(errorMsg);
        err.status = response.status;
        err.data = data;
        throw err;
      }

      return data;
    } catch (err) {
      if (err.name === "TypeError" && err.message.includes("fetch")) {
        err.message = `Cannot reach backend at ${baseUrl}. Ensure backend server is running.`;
      }
      throw err;
    }
  }

  return {
    getBaseUrl,
    setBaseUrl,
    getToken,
    setToken,
    getCurrentUser,
    setCurrentUser,

    // Health
    health: () => {
      const rootUrl = baseUrl.replace(/\/api\/?$/, "");
      return fetch(`${rootUrl}/health`).then((r) => r.json());
    },

    // Auth
    auth: {
      login: (email, password) =>
        request("/auth/login", {
          method: "POST",
          body: { email, password },
        }),
      register: (userData) =>
        request("/auth/register", {
          method: "POST",
          body: userData,
        }),
      me: () => request("/auth/me"),
    },

    // Users
    users: {
      getAll: () => request("/users"),
      create: (data) => request("/users", { method: "POST", body: data }),
      getOne: (id) => request(`/users/${id}`),
      update: (id, data) => request(`/users/${id}`, { method: "PUT", body: data }),
      delete: (id) => request(`/users/${id}`, { method: "DELETE" }),
    },

    // Customers
    customers: {
      getAll: () => request("/customers"),
      create: (data) => request("/customers", { method: "POST", body: data }),
      getOne: (id) => request(`/customers/${id}`),
    },

    // Menu
    menu: {
      getCategories: () => request("/menu/categories"),
      createCategory: (data) => request("/menu/categories", { method: "POST", body: data }),
      getItems: () => request("/menu/items"),
      getAvailableItems: () => request("/menu/items/available"),
      createItem: (data) => request("/menu/items", { method: "POST", body: data }),
      updateItem: (id, data) => request(`/menu/items/${id}`, { method: "PUT", body: data }),
    },

    // Tables
    tables: {
      getAll: () => request("/tables"),
      getAvailable: () => request("/tables/available"),
      create: (data) => request("/tables", { method: "POST", body: data }),
      updateStatus: (id, status) =>
        request(`/tables/${id}/status`, {
          method: "PATCH",
          body: { status },
        }),
    },

    // Reservations
    reservations: {
      getAll: () => request("/reservations"),
      create: (data) => request("/reservations", { method: "POST", body: data }),
      update: (id, data) => request(`/reservations/${id}`, { method: "PUT", body: data }),
    },

    // Orders
    orders: {
      getAll: () => request("/orders"),
      getOne: (id) => request(`/orders/${id}`),
      create: (data) => request("/orders", { method: "POST", body: data }),
      updateStatus: (id, status) =>
        request(`/orders/${id}/status`, {
          method: "PATCH",
          body: { status },
        }),
      updateDiscount: (id, data) =>
        request(`/orders/${id}/discount`, {
          method: "PATCH",
          body: data,
        }),
      addItem: (orderId, itemData) =>
        request(`/orders/${orderId}/items`, {
          method: "POST",
          body: itemData,
        }),
      getItems: (orderId) => request(`/orders/${orderId}/items`),
      recalculate: (orderId) => request(`/orders/${orderId}/recalculate`, { method: "POST" }),
    },

    // Kitchen
    kitchen: {
      getTickets: (status = null) => {
        const query = status ? `?status=${encodeURIComponent(status)}` : "";
        return request(`/kitchen/tickets${query}`);
      },
      createTicket: (orderId, priority = "NORMAL") =>
        request("/kitchen/tickets", {
          method: "POST",
          body: { order_id: orderId, priority },
        }),
      getTicket: (ticketId) => request(`/kitchen/tickets/${ticketId}`),
      updateStatus: (ticketId, status) =>
        request(`/kitchen/tickets/${ticketId}/status?status_value=${encodeURIComponent(status)}`, {
          method: "PATCH",
        }),
      assignStaff: (ticketId, userId, role = "CHEF") =>
        request(`/kitchen/tickets/${ticketId}/assign`, {
          method: "POST",
          body: { user_id: userId, role },
        }),
    },

    // Billing & Payments
    billing: {
      getInvoices: (status = null) => {
        const query = status ? `?status=${encodeURIComponent(status)}` : "";
        return request(`/invoices${query}`);
      },
      createInvoice: (orderId) =>
        request("/invoices", {
          method: "POST",
          body: { order_id: orderId },
        }),
      getInvoice: (id) => request(`/invoices/${id}`),
      getInvoiceByOrder: (orderId) => request(`/invoices/order/${orderId}`),
      createPayment: (data) =>
        request("/payments", {
          method: "POST",
          body: data,
        }),
      getPayments: () => request("/payments"),
      createRefund: (data) => request("/refunds", { method: "POST", body: data }),
    },

    // Inventory & Ingredients
    inventory: {
      getIngredients: () => request("/ingredients"),
      getActiveIngredients: () => request("/ingredients/active"),
      createIngredient: (data) => request("/ingredients", { method: "POST", body: data }),
      updateStock: (id, quantity) =>
        request(`/ingredients/${id}/stock`, {
          method: "POST",
          body: { quantity: Number(quantity) },
        }),
      getStockStatus: (id) => request(`/ingredients/${id}/stock-status`),
      getMovements: () => request("/stock-movements"),
      createMovement: (data) => request("/stock-movements", { method: "POST", body: data }),
    },

    // Feedback
    feedback: {
      getAll: () => request("/feedback"),
      getSummary: () => request("/feedback/summary"),
      create: (orderId, data) =>
        request(`/orders/${orderId}/feedback`, {
          method: "POST",
          body: data,
        }),
    },
  };
})();
