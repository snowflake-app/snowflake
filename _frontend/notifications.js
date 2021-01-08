export async function setupNotifications() {
    const notificationCounterContainer = document.querySelector('#notification-button .tagged')

    if (notificationCounterContainer) {
        const notificationCount = await fetch("/api/notifications/_count").then(r => r.json());

        if (notificationCount > 0) {
            const counter = document.createElement('span')
            counter.className = "tag is-small-tag is-primary is-rounded"
            counter.innerText = notificationCount
            notificationCounterContainer.appendChild(counter)
        }
    }
}
