document.addEventListener('DOMContentLoaded', () => {
  const noteField = document.getElementById('note-field');

  if (noteField) {
    const sendContainer = document.querySelector('.send-container')
    noteField.addEventListener('focus', () => {
      sendContainer.style.height = 'auto';
    })
  }

  const launchButton = document.getElementById('launch-one-on-one-form');
   if (launchButton) {
    const form = document.getElementById('one-on-one-form')

    form.querySelectorAll('button[data-action="close"]').forEach(button => {
        button.addEventListener('click', (e) => {
            e.preventDefault()
            console.log("Closing form")
            form.classList.remove('is-active');
            form.reset()
        })
    })

    launchButton.addEventListener('click', () => {
      form.classList.add('is-active');
    })
  }
});
