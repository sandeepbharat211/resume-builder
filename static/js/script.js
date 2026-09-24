// Auto close alerts after 4s
setTimeout(() => {
  document.querySelectorAll('.alert').forEach(a => {
    try { bootstrap.Alert.getOrCreateInstance(a).close(); } catch(e) {}
  });
}, 4000);
