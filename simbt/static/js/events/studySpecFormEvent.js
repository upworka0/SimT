var $ = require("jQuery");

function addEventToForm(form, callback) {
    $(form).submit(function(event) {
        console.log(event);
        event.preventDefault();
        let nodeName = $("#elementName").text();
        nodeName = nodeName.substring(nodeName.indexOf(":") + 1, nodeName.length).trim()
        let alias = $("#" + $(this).attr('id').replace("_form", "_alias")).val();
        callback(nodeName, alias);
    });
}

export {
    addEventToForm
};