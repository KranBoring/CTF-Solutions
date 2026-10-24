const form = document.getElementById('upload-form');
const fileInput = document.getElementById('wasm-file');
const fileLabel = document.getElementById('file-label');
const dropzone = document.getElementById('dropzone');
const button = document.getElementById('submit-button');
const result = document.getElementById('result');
const resultIcon = document.getElementById('result-icon');
const resultTitle = document.getElementById('result-title');
const resultMessage = document.getElementById('result-message');
const flagNode = document.getElementById('flag');

function display(title, message, kind = 'pending', flag = '') {
  result.hidden = false;
  result.classList.toggle('error', kind === 'error');
  resultIcon.textContent = kind === 'success' ? '✓' : kind === 'error' ? '×' : '◌';
  resultTitle.textContent = title;
  resultMessage.textContent = message;
  flagNode.hidden = !flag;
  flagNode.textContent = flag;
}

function selectedFile() {
  const file = fileInput.files[0];
  fileLabel.textContent = file ? file.name : 'Choose a .wasm file';
}

fileInput.addEventListener('change', selectedFile);
for (const name of ['dragenter', 'dragover']) {
  dropzone.addEventListener(name, event => { event.preventDefault(); dropzone.classList.add('dragging'); });
}
for (const name of ['dragleave', 'drop']) {
  dropzone.addEventListener(name, event => { event.preventDefault(); dropzone.classList.remove('dragging'); });
}
dropzone.addEventListener('drop', event => {
  if (event.dataTransfer.files.length) {
    fileInput.files = event.dataTransfer.files;
    selectedFile();
  }
});

const delay = ms => new Promise(resolve => setTimeout(resolve, ms));

form.addEventListener('submit', async event => {
  event.preventDefault();
  if (!fileInput.files.length) return;
  button.disabled = true;
  display('Uploading module', 'Sending your WebAssembly file to the judge.');
  try {
    const body = new FormData();
    body.append('file', fileInput.files[0]);
    const submitted = await fetch('/api/jobs', { method: 'POST', body });
    const accepted = await submitted.json();
    if (!submitted.ok) throw new Error(accepted.error || 'Upload failed');
    let checks = 0;
    while (true) {
      await delay(1700);
      const response = await fetch(`/api/jobs/${encodeURIComponent(accepted.id)}`, { cache: 'no-store' });
      const data = await response.json();
      if (!response.ok) throw new Error(data.error || 'Result unavailable');
      if (data.status === 'queued') {
        display('Waiting for the judge', 'Your module is in the queue.');
      } else if (data.status === 'running') {
        checks += 1;
        display('Running WebAssembly', `Checking hash calls${'.'.repeat(1 + checks % 3)}`);
      } else if (data.status === 'won') {
        display('Collision found', `Accepted after ${Number(data.calls).toLocaleString()} hash calls.`, 'success', data.flag);
        break;
      } else if (data.status === 'no_collision') {
        display('No collision found', `The module finished after ${Number(data.calls).toLocaleString()} hash calls.`, 'error');
        break;
      } else {
        display('Submission did not complete', data.message || 'The judge stopped execution.', 'error');
        break;
      }
    }
  } catch (error) {
    display('Submission error', error.message || 'Please retry.', 'error');
  } finally {
    button.disabled = false;
  }
});
