// ── Status filter (All / Upcoming / Expired / Active) ──
function filterCards(status, btn) {
  document.querySelectorAll('.filter-tab').forEach(t => t.classList.remove('active'));
  btn.classList.add('active');
  applyFilters();
}

// ── Category filter ──
function filterByCategory(cat, btn) {
  document.querySelectorAll('.cat-chip').forEach(c => c.classList.remove('active'));
  btn.classList.add('active');
  applyFilters();
}

// Combined filter: apply both active status tab + active category chip
function applyFilters() {
  const activeTab  = document.querySelector('.filter-tab.active');
  const activeChip = document.querySelector('.cat-chip.active');
  const status = activeTab  ? activeTab.textContent.trim().toLowerCase()  : 'all';
  const cat    = activeChip ? activeChip.textContent.trim() : 'All Categories';

  document.querySelectorAll('.sub-card').forEach(card => {
    const matchStatus = status === 'all' || card.dataset.status === status;
    const matchCat    = cat === 'All Categories' || card.dataset.category === cat;
    card.style.display = (matchStatus && matchCat) ? '' : 'none';
  });
}

// ── Cost conversion toggle ──
function showCost(id, mode, amount, btn) {
  const el = document.getElementById('cost-' + id);
  const suffix = mode === 'monthly' ? '/mo' : '/yr';
  el.innerHTML = '₹' + Math.round(amount) + '<span>' + suffix + '</span>';
  btn.closest('.cost-toggle').querySelectorAll('button').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
}