import HtmlTagElementFactory from "../factory/htmlTagElementFactory";
var $ = require('jQuery');

function handleDomChangeFromAppendRow(componentObject, predecessor) {
    var htmlFactory = new HtmlTagElementFactory();
    var tdNode = $("#appendNode").parent();
    var tdPredecessor = $("#appendPredecessor").parent();
    $("#appendRowButton").text("-");
    $("#appendRowButton").prop("id", "removeRowButton");
    $("#appendPredecessor").remove();
    $("#appendNode").remove();
    if (componentObject.attrs.id.includes("C")) {
        $("#appendHabitable").empty();
        $("#appendNbrLogement").empty();
        $("#appendNbrEtage").empty();
        let habitableInput = htmlFactory.createHabitableAreaInput(componentObject.attrs.id);
        let numberOfHousingInput = htmlFactory.createNumberOfHousingInput(componentObject.attrs.id);
        let numberOfFloorInput = htmlFactory.createNombreEtageInput(componentObject.attrs.id);
        $("#appendHabitable").append(habitableInput);
        $("#appendNbrLogement").append(numberOfHousingInput);
        $("#appendNbrEtage").append(numberOfFloorInput);
    } else if (componentObject.attrs.id.includes("A")) {
        $("#appendLongueur").empty();
        let longueurInput = htmlFactory.createLongueurInput(componentObject.attrs.id);
        $("#appendLongueur").append(longueurInput);
    }

    $("#appendHabitable").attr("id", "habitable_" + componentObject.attrs.id);
    $("#appendNbrLogement").attr("id", "number_housing_" + componentObject.attrs.id);
    $("#appendLongueur").attr("id", "longueur_" + componentObject.attrs.id);
    $("#appendNbrEtage").attr("id", "nombre_etage_" + componentObject.attrs.id);

    tdNode[0].innerHTML = componentObject.attrs.id;
    tdPredecessor[0].innerHTML = predecessor.attrs.id;
}

export {
    handleDomChangeFromAppendRow
}