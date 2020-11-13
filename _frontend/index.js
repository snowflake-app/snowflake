import "./styles/index.scss";

import "regenerator-runtime/runtime";

import {setupToggles} from "./toggle";
import {setupAutocomplete} from "./mentions";
import {bindLaunchButton} from "./one-on-one";
import {setupNotifications} from "./notifications";


document.addEventListener('DOMContentLoaded', async () => {
    setupToggles();
    const noteField = document.getElementById('note-field');

    if (noteField) {
        const sendContainer = document.querySelector('.send-container')
        noteField.addEventListener('focus', () => {
            sendContainer.style.height = 'auto';
        })
    }

    const launchButton = document.getElementById('launch-one-on-one-form');
    if (launchButton) {
        bindLaunchButton(launchButton)
    }

    setupAutocomplete();
    setupNotifications();
});
