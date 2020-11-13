export function setupNotifications() {
    document.querySelectorAll('.notification .delete').forEach((button) => {
        const notification = button.parentNode;

        button.addEventListener('click', () => {
            notification.parentNode.removeChild(notification);
        });
    });
}
