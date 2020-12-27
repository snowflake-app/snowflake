export function setupModals() {
    document.querySelectorAll('button[data-toggle-modal]').forEach(button => {
        const target = document.querySelector(button.dataset.toggleModal)
        button.addEventListener('click', evt => {
            evt.preventDefault()
            target.classList.toggle("is-active")
        })
    });

    document.querySelectorAll('.modal').forEach(modal => {
        const closeBtn = modal.querySelector('.modal-close')

        if (closeBtn) {
            closeBtn.addEventListener('click', () => {
                modal.classList.remove("is-active");
            });
        }


        const background = modal.querySelector('.modal-background')

        if (background) {
            background.addEventListener('keydown', evt => {
                if (evt.key === "Escape" || evt.key === "Esc") {
                    modal.classList.remove("is-active")
                }
            })
        }
    });
}
