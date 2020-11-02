export function bindLaunchButton(launchButton) {
    const form = document.getElementById('one-on-one-form')

    form.querySelectorAll('button[data-action="close"]').forEach(button => {
        button.addEventListener('click', (e) => {
            e.preventDefault()
            form.classList.remove('is-active');
            form.reset()
        })
    })

    launchButton.addEventListener('click', () => {
        form.classList.add('is-active');
    })
}
