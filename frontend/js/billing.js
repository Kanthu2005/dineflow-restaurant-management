/**
 * Billing, Invoicing & Payments Module
 */

const BillingView = (() => {
  let invoices = [];
  let filterStatus = "all";

  async function init() {
    await refresh();
  }

  async function refresh() {
    try {
      invoices = await API.billing.getInvoices();
      renderInvoices();
    } catch (e) {
      console.warn("Could not load invoices:", e);
      invoices = [];
      renderInvoices();
    }
  }

  function setFilter(status) {
    filterStatus = status;
    renderInvoices();
  }

  function renderInvoices() {
    const tableBody = document.getElementById("invoices-table-body");
    const countBadge = document.getElementById("invoices-total-count");
    if (!tableBody) return;

    let filtered = invoices;
    if (filterStatus !== "all") {
      filtered = filtered.filter(i => i.status === filterStatus);
    }

    if (countBadge) countBadge.textContent = `${filtered.length} Invoices`;

    if (filtered.length === 0) {
      tableBody.innerHTML = `
        <tr>
          <td colspan="7" style="text-align: center; padding: 3rem; color: var(--text-dim);">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">🧾</div>
            No invoices recorded yet.
          </td>
        </tr>`;
      return;
    }

    tableBody.innerHTML = filtered.map(inv => {
      const invId = inv.id || inv._id;
      const invNum = inv.invoice_number || `INV-${invId.slice(-6)}`;
      const orderNum = inv.order_number || (inv.order_id ? `#${inv.order_id.slice(-6)}` : '-');
      const total = Number(inv.total_amount?.$numberDecimal || inv.total_amount || 0).toFixed(2);
      const subtotal = Number(inv.subtotal?.$numberDecimal || inv.subtotal || 0).toFixed(2);
      const dateStr = inv.generated_at ? new Date(inv.generated_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) : '-';
      const statusBadge = getInvoiceBadge(inv.status);

      return `
        <tr>
          <td style="font-weight: 700; color: var(--accent-primary);">${invNum}</td>
          <td style="font-weight: 600;">${orderNum}</td>
          <td>$${subtotal}</td>
          <td style="font-weight: 700; font-size: 0.95rem;">$${total}</td>
          <td>${statusBadge}</td>
          <td style="font-size: 0.78rem; color: var(--text-dim);">${dateStr}</td>
          <td>
            <div style="display: flex; gap: 0.4rem;">
              <button class="btn btn-secondary btn-sm" onclick="BillingView.viewReceipt('${invId}')">Receipt</button>
              ${inv.status !== 'PAID' ? `
                <button class="btn btn-primary btn-sm" onclick="BillingView.openPaymentModal('${invId}', ${total})">Pay</button>
              ` : `
                <span class="badge badge-green" style="align-self: center;">Settled</span>
              `}
            </div>
          </td>
        </tr>
      `;
    }).join("");
  }

  function getInvoiceBadge(status) {
    switch (status) {
      case "PAID": return '<span class="badge badge-green">Paid</span>';
      case "PARTIALLY_PAID": return '<span class="badge badge-amber">Partially Paid</span>';
      case "UNPAID": return '<span class="badge badge-red">Unpaid</span>';
      default: return `<span class="badge badge-muted">${status || 'Unknown'}</span>`;
    }
  }

  function openPaymentModal(invoiceId, totalAmount) {
    const invInput = document.getElementById("pay-invoice-id");
    const amountInput = document.getElementById("pay-amount-input");
    if (invInput) invInput.value = invoiceId;
    if (amountInput) amountInput.value = totalAmount;

    App.openModal("payment-modal");
  }

  async function submitPayment() {
    const invoiceId = document.getElementById("pay-invoice-id")?.value;
    const amount = Number(document.getElementById("pay-amount-input")?.value || 0);
    const method = document.getElementById("pay-method-select")?.value || "CASH";
    const ref = document.getElementById("pay-ref-input")?.value?.trim() || null;
    const user = API.getCurrentUser();

    if (!invoiceId || amount <= 0) {
      App.showToast("Enter a valid payment amount", "warning");
      return;
    }

    try {
      App.showLoader(true);
      await API.billing.createPayment({
        invoice_id: invoiceId,
        amount: amount,
        payment_method: method,
        transaction_reference: ref || `TXN-${Date.now().toString().slice(-6)}`,
        recorded_by: user?.email || user?.name || "cashier_staff"
      });

      App.showToast("Payment recorded successfully!", "success");
      App.closeModal("payment-modal");
      await refresh();
      if (window.OrdersList) OrdersList.refresh();
      if (window.Dashboard) Dashboard.refresh();
    } catch (e) {
      App.showToast(`Payment failed: ${e.message}`, "error");
    } finally {
      App.showLoader(false);
    }
  }

  async function viewReceipt(invoiceId) {
    try {
      App.showLoader(true);
      const inv = await API.billing.getInvoice(invoiceId);
      const order = inv.order_id ? await API.orders.getOne(inv.order_id).catch(() => null) : null;
      const items = inv.order_id ? await API.orders.getItems(inv.order_id).catch(() => []) : [];

      const receiptContent = document.getElementById("receipt-modal-content");
      if (!receiptContent) return;

      const subtotal = Number(inv.subtotal?.$numberDecimal || inv.subtotal || 0).toFixed(2);
      const tax = Number(inv.tax_amount?.$numberDecimal || inv.tax_amount || 0).toFixed(2);
      const discount = Number(inv.discount_amount?.$numberDecimal || inv.discount_amount || 0).toFixed(2);
      const total = Number(inv.total_amount?.$numberDecimal || inv.total_amount || 0).toFixed(2);

      let itemsHtml = items.map(item => {
        const itemTotal = Number(item.item_total?.$numberDecimal || item.item_total || 0).toFixed(2);
        return `
          <div style="display: flex; justify-content: space-between; margin-bottom: 0.35rem;">
            <span>${item.quantity}× ${item.item_name_snapshot}</span>
            <span>$${itemTotal}</span>
          </div>
        `;
      }).join("");

      if (items.length === 0) {
        itemsHtml = `<div style="text-align: center; color: #6b7280;">General dining service</div>`;
      }

      receiptContent.innerHTML = `
        <div class="thermal-receipt">
          <div class="receipt-header">
            <div class="receipt-title">DINEFLOW RESTAURANT</div>
            <div style="font-size: 0.75rem; color: #4b5563;">Culinary Arts & Fine Dining</div>
            <div style="font-size: 0.72rem; color: #6b7280; margin-top: 0.25rem;">Tel: +1 (555) 346-3356 • GST #98234-A</div>
          </div>

          <div style="font-size: 0.75rem; margin-bottom: 0.5rem; display: flex; justify-content: space-between;">
            <span>Invoice: <strong>${inv.invoice_number || invoiceId}</strong></span>
            <span>Date: ${new Date(inv.generated_at || Date.now()).toLocaleDateString()}</span>
          </div>
          ${order ? `
            <div style="font-size: 0.75rem; margin-bottom: 0.5rem; display: flex; justify-content: space-between;">
              <span>Order: ${order.order_number || order.id}</span>
              <span>Type: ${order.order_type}</span>
            </div>
          ` : ''}

          <div class="receipt-divider"></div>

          <div style="margin: 0.75rem 0;">
            ${itemsHtml}
          </div>

          <div class="receipt-divider"></div>

          <div style="display: flex; justify-content: space-between; margin-bottom: 0.2rem;">
            <span>Subtotal:</span>
            <span>$${subtotal}</span>
          </div>
          <div style="display: flex; justify-content: space-between; margin-bottom: 0.2rem;">
            <span>Tax (5%):</span>
            <span>$${tax}</span>
          </div>
          ${discount > 0 ? `
            <div style="display: flex; justify-content: space-between; color: #059669; margin-bottom: 0.2rem;">
              <span>Discount:</span>
              <span>-$${discount}</span>
            </div>
          ` : ''}
          <div class="receipt-divider"></div>
          <div style="display: flex; justify-content: space-between; font-size: 1.1rem; font-weight: 800; margin-top: 0.35rem;">
            <span>TOTAL DUE:</span>
            <span>$${total}</span>
          </div>

          <div style="text-align: center; margin-top: 1.25rem; font-size: 0.75rem; color: #4b5563;">
            <p style="font-weight: 700; margin-bottom: 0.25rem;">STATUS: ${inv.status}</p>
            <p>Thank you for dining with us!</p>
            <p style="font-size: 0.65rem; margin-top: 0.25rem;">Powered by DineFlow System</p>
          </div>
        </div>
      `;

      App.openModal("receipt-modal");
    } catch (e) {
      App.showToast(`Error rendering receipt: ${e.message}`, "error");
    } finally {
      App.showLoader(false);
    }
  }

  function printReceipt() {
    window.print();
  }

  return {
    init,
    refresh,
    setFilter,
    openPaymentModal,
    submitPayment,
    viewReceipt,
    printReceipt
  };
})();
