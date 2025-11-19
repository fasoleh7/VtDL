const backendBase = "https://YOUR_BACKEND_DOMAIN";

document.getElementById('downloadBtn').addEventListener('click', async () => {
  const url = document.getElementById('url').value.trim();
  const status = document.getElementById('status');
  if (!url) { status.innerText = "Masukkan URL."; return; }

  status.innerText = "Meminta server...";
  try {
    const resp = await fetch(backendBase + '/download', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url })
    });

    if (!resp.ok) {
      const err = await resp.json().catch(()=>({error:"server error"}));
      status.innerText = "Gagal: " + err.error;
      return;
    }

    const blob = await resp.blob();
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = "tiktok.mp4";
    a.click();
    status.innerText = "Selesai.";
  } catch (e) {
    status.innerText = "Error: " + e.message;
  }
});
