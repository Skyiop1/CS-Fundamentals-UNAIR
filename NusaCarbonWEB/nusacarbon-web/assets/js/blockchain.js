// assets/js/blockchain.js

// Truncate hash for display dynamically in vanilla JS 
// (though most times it should be truncated from PHP server-side)
function truncateHash(hash) {
  if (!hash || hash.length < 12) return hash;
  return hash.substring(0, 6) + '...' + hash.substring(hash.length - 4);
}

function mockGasFee() {
  const min = 0.003;
  const max = 0.008;
  return (Math.random() * (max - min) + min).toFixed(4);
}
