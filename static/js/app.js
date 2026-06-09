/* TutorSync — app.js
   Lucide icon init + shared UI helpers
*/

// ── Lucide Icons ─────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  if (window.lucide) {
    lucide.createIcons();
  }
});

// ── Sidebar collapse toggle ───────────────────────────────────
function initSidebar() {
  const sidebar = document.getElementById('ts-sidebar');
  const main    = document.getElementById('ts-main');
  const toggle  = document.getElementById('ts-sidebar-toggle');
  if (!sidebar || !toggle) return;

  const COLLAPSED_KEY = 'ts-sidebar-collapsed';
  const collapsed = localStorage.getItem(COLLAPSED_KEY) === 'true';
  if (collapsed) {
    sidebar.classList.add('collapsed');
    main && main.classList.add('sidebar-collapsed');
  }

  toggle.addEventListener('click', () => {
    sidebar.classList.toggle('collapsed');
    main && main.classList.toggle('sidebar-collapsed');
    localStorage.setItem(COLLAPSED_KEY, sidebar.classList.contains('collapsed'));
  });
}

// ── Notification dropdown ─────────────────────────────────────
function initNotifications() {
  const btn      = document.getElementById('ts-notif-btn');
  const dropdown = document.getElementById('ts-notif-dropdown');
  if (!btn || !dropdown) return;

  btn.addEventListener('click', (e) => {
    e.stopPropagation();
    dropdown.classList.toggle('hidden');
  });

  document.addEventListener('click', (e) => {
    if (!dropdown.contains(e.target) && e.target !== btn) {
      dropdown.classList.add('hidden');
    }
  });
}

// ── User menu dropdown ────────────────────────────────────────
function initUserMenu() {
  const btn  = document.getElementById('ts-user-menu-btn');
  const menu = document.getElementById('ts-user-menu');
  if (!btn || !menu) return;

  btn.addEventListener('click', (e) => {
    e.stopPropagation();
    menu.classList.toggle('hidden');
  });

  document.addEventListener('click', (e) => {
    if (!menu.contains(e.target) && e.target !== btn) {
      menu.classList.add('hidden');
    }
  });
}

// ── Flash messages auto-dismiss ───────────────────────────────
function initFlashMessages() {
  document.querySelectorAll('.ts-flash').forEach((el) => {
    const close = el.querySelector('.ts-flash-close');
    if (close) {
      close.addEventListener('click', () => el.remove());
    }
    setTimeout(() => el.classList.add('opacity-0', 'transition-opacity', 'duration-300'), 4000);
    setTimeout(() => el.remove(), 4300);
  });
}

// ── Confirm dialogs ────────────────────────────────────────────
function initConfirmButtons() {
  document.querySelectorAll('[data-confirm]').forEach((btn) => {
    btn.addEventListener('click', (e) => {
      const msg = btn.dataset.confirm || 'Are you sure?';
      if (!window.confirm(msg)) {
        e.preventDefault();
        e.stopPropagation();
      }
    });
  });
}

// ── Bulk-select checkboxes ─────────────────────────────────────
function initBulkSelect() {
  const selectAll = document.getElementById('ts-select-all');
  if (!selectAll) return;

  const rows = document.querySelectorAll('.ts-row-check');
  const bulkBar = document.getElementById('ts-bulk-bar');

  const updateBulkBar = () => {
    const checked = document.querySelectorAll('.ts-row-check:checked').length;
    if (bulkBar) {
      bulkBar.classList.toggle('hidden', checked === 0);
      const counter = bulkBar.querySelector('.bulk-count');
      if (counter) counter.textContent = checked;
    }
  };

  selectAll.addEventListener('change', () => {
    rows.forEach((r) => { r.checked = selectAll.checked; });
    updateBulkBar();
  });

  rows.forEach((r) => {
    r.addEventListener('change', () => {
      selectAll.indeterminate = [...rows].some((x) => x.checked) && ![...rows].every((x) => x.checked);
      selectAll.checked = [...rows].every((x) => x.checked);
      updateBulkBar();
    });
  });
}

// ── Init all ─────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  initSidebar();
  initNotifications();
  initUserMenu();
  initFlashMessages();
  initConfirmButtons();
  initBulkSelect();
});
