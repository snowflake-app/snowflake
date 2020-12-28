export function setupModals() {
    function showModal(modal) {
        modal.classList.add("is-active");
        modal.dispatchEvent(new Event('open'));
    }

    function closeModal(modal) {
        modal.classList.remove("is-active");
        modal.dispatchEvent(new Event('close'));
    }

    document.querySelectorAll('button[data-toggle-modal]').forEach(button => {
        const modal = document.querySelector(button.dataset.toggleModal)
        button.addEventListener('click', evt => {
            evt.preventDefault()

            if (modal.classList.contains("is-active")) {
                closeModal(modal)
            } else {
                showModal(modal);
            }
        })

        modal.addEventListener('close', () => {
            button.focus();
        })

    });

    document.querySelectorAll('.modal').forEach(modal => {
        const closeBtn = modal.querySelector('.modal-close')

        if (closeBtn) {
            closeBtn.addEventListener('click', () => {
                closeModal(modal);
            });
        }
    });

    document.addEventListener('keyup', e => {
        if (e.key === 'Escape' || e.key === 'Esc') {
            document.querySelectorAll('.modal.is-active').forEach(closeModal);
        }
    });
}
