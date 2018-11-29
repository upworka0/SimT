import {
    ComponentManager
} from "./ComponentManager";
import * as canvajs from "./canvas";
var $ = require('jQuery');

const tableDOM = ".table";
const tableBodyDOM = "#network";

$(document).ready(function() {
    if (document.getElementById("network") != null) {
        console.log("Nope");
        var csrf_token = $('.box input[type="hidden"]').val();
        var manager = new ComponentManager(csrf_token, tableDOM, tableBodyDOM);
        manager.initBaseEvents();
    } else {
        canvajs.initCanvaJS();
    }
});