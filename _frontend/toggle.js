export function setupToggles() {
    document.querySelectorAll('button[data-toggle]').forEach(button => {
        const target = document.querySelector(button.dataset.toggle)
        button.addEventListener('click', evt => {
            evt.preventDefault()
            target.classList.toggle("hide")
        })
    });
}
