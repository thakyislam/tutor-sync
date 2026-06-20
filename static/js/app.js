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
  const mobileBtn = document.getElementById('ts-mobile-menu');
  const overlay = document.getElementById('ts-sidebar-overlay');
  if (!sidebar) return;

  const isMobile = () => window.innerWidth <= 640;

  const closeMobile = () => {
    sidebar.classList.remove('mobile-open');
    overlay && overlay.classList.remove('visible');
  };

  if (toggle) {
    toggle.addEventListener('click', () => {
      if (isMobile()) {
        closeMobile();
      } else {
        sidebar.classList.toggle('collapsed');
        main && main.classList.toggle('sidebar-collapsed');
      }
    });
  }

  if (mobileBtn) {
    mobileBtn.addEventListener('click', () => {
      sidebar.classList.add('mobile-open');
      overlay && overlay.classList.add('visible');
    });
  }

  if (overlay) {
    overlay.addEventListener('click', closeMobile);
  }

  sidebar.querySelectorAll('.ts-nav-item').forEach((link) => {
    link.addEventListener('click', () => {
      if (isMobile()) closeMobile();
    });
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
