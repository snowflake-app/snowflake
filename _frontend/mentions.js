import Tribute from "tributejs";
import errorHandler from "./error-handler";

export function setupAutocomplete() {
    document.querySelectorAll('*[data-has-mentions]')
        .forEach(element => {
            const tribute = new Tribute({
                collection: [{
                    lookup: 'username',
                    fillAttr: 'username',
                    autocompleteMode: true,
                    values: function (text, cb) {
                        fetch("/api/users/_autocomplete?q=" + encodeURIComponent(text))
                            .then(r => r.json())
                            .then(cb)
                            .catch(errorHandler)
                    }
                }]
            });

            tribute.attach(element);
        });
}
