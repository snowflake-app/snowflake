import Tribute from "tributejs";
import errorHandler from "./error-handler";
import {searchUsers} from "./api";

export function setupAutocomplete() {
    document.querySelectorAll('*[data-has-mentions]')
        .forEach(element => {
            const tribute = new Tribute({
                collection: [{
                    lookup: 'username',
                    fillAttr: 'username',
                    autocompleteMode: true,
                    values: function (text, cb) {
                        searchUsers(text)
                            .then(cb)
                            .catch(errorHandler)
                    }
                }]
            });

            tribute.attach(element);
        });
}
