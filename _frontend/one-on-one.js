import AutoComplete from "@tarekraafat/autocomplete.js";
import {searchUsers} from "./api";
import errorHandler from "./error-handler";

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

function renderUser({name, username, avatar}) {
    return `
        <div class="user is-flex p-1 dropdown-item">
            <div class="avatar is-flex">
                <span class="image is-24x24 mx-1">
                    <img alt="${name}" class="is-rounded" src="${avatar}">
                </span>
            </div>
            <div class="user-info is-flex-grow-1">
                <div class="has-text-weight-bold">${name}</div>
                <div class="help">${username}</div>
            </div>
        </div>
    `;
}

export function setupUserAutocomplete() {
    const searchField = document.querySelector('.one-on-ones #user-search')
    if (searchField) {
        const resultList = document.querySelector('.user-autocomplete-container')
        searchField.addEventListener('focus', () => {
            resultList.classList.add('is-active')
        })
        searchField.addEventListener('blur', () => {
            resultList.classList.remove('is-active')
        })

        const userField = document.querySelector('.user-list')
        new AutoComplete({
            data: {
                src: async () => {
                    const query = searchField.value;
                    return await searchUsers(query).catch(errorHandler)
                },
                key: ["name"],
                cache: false
            },
            selector: '#user-search',
            threshold: 3,
            debounce: 300,
            searchEngine: "strict",
            resultsList: {
                render: true,
                container: source => {
                    source.setAttribute("id", "autoComplete_list");
                    source.setAttribute("class", "dropdown-content");
                },
                destination: document.querySelector(".user-autocomplete-container .dropdown-menu"),
                position: "beforeend",
                element: "div"
            },
            resultItem: {
                content: (data, source) => {
                    console.log(data)
                    source.innerHTML = renderUser(data.value);
                },
                element: "div"
            },
            onSelection: feedback => {
                console.log(feedback);
                const user = feedback.selection.value;
                searchField.value = "";
                userField.innerHTML = renderUser(user)
                resultList.classList.remove('is-active')

                document.getElementById('user').value = user.username;
            }
        });
    }
}
