document.addEventListener('DOMContentLoaded', () => {
  const uploadForm = document.getElementById('upload-form');
  if (!uploadForm) return;

  uploadForm.addEventListener('submit', (event) => {
    event.preventDefault();
    const title = document.getElementById('title')?.value || 'Untitled project';
    const message = document.getElementById('message');

    if (message) {
      message.textContent = `Project "${title}" was submitted successfully.`;
    }

    uploadForm.reset();
  });
});
