export function setupAlerts() {
    document.querySelectorAll('.alert .delete').forEach((button) => {
        const notification = button.parentNode;

        button.addEventListener('click', () => {
            notification.parentNode.removeChild(notification);
        });
    });
}
