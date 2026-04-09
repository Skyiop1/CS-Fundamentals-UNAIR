// assets/js/main.js

// Copy hash to clipboard
function copyToClipboard(text) {
  navigator.clipboard.writeText(text).then(() => {
    showToast('Hash disalin!', 'success');
  }).catch(err => {
    console.error('Copy failed', err);
    showToast('Gagal menyalin hash', 'error');
  });
}

// Toast notification
function showToast(message, type = 'info') {
  let container = document.querySelector('.toast-container');
  if (!container) {
    container = document.createElement('div');
    container.className = 'toast-container';
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  
  // Icon based on type
  let iconHtml = '';
  if (type === 'success') {
    iconHtml = '<i data-lucide="check-circle" class="text-xs" style="color: var(--color-verified)"></i>';
  } else if (type === 'error') {
    iconHtml = '<i data-lucide="x-circle" class="text-xs" style="color: var(--color-rejected)"></i>';
  } else {
    iconHtml = '<i data-lucide="info" class="text-xs" style="color: var(--color-primary)"></i>';
  }

  toast.innerHTML = `${iconHtml} <span>${message}</span>`;
  container.appendChild(toast);
  
  // Initialize lucide icons for the newly added toast
  if (typeof lucide !== 'undefined') {
    lucide.createIcons({ root: toast });
  }

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateY(10px) translateX(100%)';
    toast.style.transition = 'all 0.3s ease';
    setTimeout(() => toast.remove(), 300);
  }, 3000);
}

// Tab switcher (generic)
function initTabs() {
  document.querySelectorAll('[data-tab]').forEach(tab => {
    tab.addEventListener('click', (e) => {
      const targetPanelId = tab.dataset.tab;
      
      // Find parent container grouping tabs to only toggle sibling tabs
      const container = tab.closest('.tabs-container') || document;
      
      const tabs = container.querySelectorAll('[data-tab]');
      const panels = container.querySelectorAll('.tab-panel');
      
      tabs.forEach(t => t.classList.remove('active'));
      panels.forEach(p => p.classList.add('hidden'));
      
      tab.classList.add('active');
      const targetPanel = container.querySelector(`#${targetPanelId}`);
      if (targetPanel) {
        targetPanel.classList.remove('hidden');
      }
    });
  });
}

// Format IDR
function formatIDRLocale(amount) {
  return new Intl.NumberFormat('id-ID', { style: 'currency', currency: 'IDR', minimumFractionDigits: 0 }).format(amount);
}

document.addEventListener('DOMContentLoaded', () => {
  initTabs();
  // Init lucide icons
  if (typeof lucide !== 'undefined') {
    lucide.createIcons();
  }
});
