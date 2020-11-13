export function searchUsers(text) {
    return fetch("/api/users/_autocomplete?q=" + encodeURIComponent(text))
        .then(r => r.json())
}
