document.addEventListener('DOMContentLoaded', () => {
  const noteField = document.getElementById('note-field');

  if (noteField) {
    const sendContainer = document.querySelector('.send-container')
    noteField.addEventListener('focus', () => {
      sendContainer.style.height = 'auto';
    })
  }
});
