function checkStatus() {
  const infoEl = document.getElementById('edge-info');
  infoEl.innerText = 'Connecting to edge network...';

  const userTime = new Date().toLocaleTimeString();
  const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;

  setTimeout(() => {
    infoEl.innerHTML = `
      <strong style="color: #38bdf8;">Connected to Amazon CloudFront Edge Node</strong><br>
      <small style="color: #94a3b8;">Client Time: ${userTime} | Timezone: ${timezone}</small>
    `;
  }, 350);
}
