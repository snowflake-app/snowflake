export function setupToggles() {
    document.querySelectorAll('*[data-toggle]').forEach(button => {
        const target = document.querySelector(button.dataset.toggle)
        const toggleClass = button.dataset.toggleClass || "hide"
        button.addEventListener('click', evt => {
            evt.preventDefault()
            target.classList.toggle(toggleClass)
        })
    });
}
