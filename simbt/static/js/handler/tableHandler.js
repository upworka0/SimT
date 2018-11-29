import HtmlTagElementFactory from "./../factory/htmlTagElementFactory";
import {
    handleDomChangeFromAppendRow
} from "./../events/addNewRowEvent";
import {
    componentFactory
} from "./../ComponentManager";

var $ = require('jQuery');

module.exports = class TableHandler {
    /*
      Handle every change to the table
    */
    constructor(tableDOM, bodyDOM) {
        this.htmlTagFactory = new HtmlTagElementFactory();
        this.tableDOM = tableDOM;
        this.bodyDOM = bodyDOM;
        this.unavailable = "----";
    }

    _buildDOMStructuredJSON() {
        /*
          @RETURN build a json object
          of the new element used in the table
        */
        var dom = {
            newTr: this.htmlTagFactory.createTrElement(),
            actionButton: this.htmlTagFactory.createTdElement(),
            nomNoeud: this.htmlTagFactory.createTdElement(),
            suiveur: this.htmlTagFactory.createTdElement(),
            predecesseur: this.htmlTagFactory.createTdElement(),
            type: this.htmlTagFactory.createTdElement(),
            typeChauffage: this.htmlTagFactory.createTdElement(),
            typeLogement: this.htmlTagFactory.createTdElement(),
            surfaceHabitable: this.htmlTagFactory.createTdElement(),
            nbrLogement: this.htmlTagFactory.createTdElement(),
            nbrEtage: this.htmlTagFactory.createTdElement(),
            longueur: this.htmlTagFactory.createTdElement()
        };
        return dom;
    }

    _updateDomTr(dom) {
        /*
          Update the values contained in the tr element
        */
        var tr = dom.newTr;
        $(tr).empty();
        tr.appendChild(dom.actionButton);
        tr.appendChild(dom.nomNoeud);
        tr.appendChild(dom.suiveur);
        tr.appendChild(dom.predecesseur);
        tr.appendChild(dom.type);
        tr.appendChild(dom.typeChauffage);
        tr.appendChild(dom.typeLogement);
        tr.appendChild(dom.surfaceHabitable);
        tr.appendChild(dom.nbrLogement);
        tr.appendChild(dom.nbrEtage);
        tr.appendChild(dom.longueur);
        dom.newTr = tr;
        return dom;
    }

    addNewRow(componentList, callback) {
        /*
          Add new row (blank row)
        */
        var domValues = this._buildDOMStructuredJSON();
        var appendButton = this.htmlTagFactory.createAppendRowButton();
        this._appendButtonClickEvent(appendButton, function(component, pred) {
            callback(component, pred);
        });
        domValues.actionButton.appendChild(appendButton);
        domValues.nomNoeud.appendChild(this.htmlTagFactory.createNewElementOptionChoices());
        domValues.suiveur.innerHTML = this.unavailable; //TODO Add Select to a client ( NOTHING if it is a client)
        domValues.predecesseur.appendChild(this.htmlTagFactory.createPredecessorSelectTag(componentList)); //TODO Add Select to a node ()
        domValues.type.innerHTML = this.unavailable; //TODO
        domValues.type.setAttribute("id", "appendChangeType");
        domValues.typeChauffage.innerHTML = this.unavailable;
        domValues.typeChauffage.setAttribute("id", "appendChauffage");
        domValues.typeLogement.innerHTML = this.unavailable;
        domValues.surfaceHabitable.innerHTML = this.unavailable;
        domValues.surfaceHabitable.setAttribute("id", "appendHabitable");
        domValues.nbrLogement.innerHTML = this.unavailable;
        domValues.nbrLogement.setAttribute("id", "appendNbrLogement");
        domValues.nbrEtage.innerHTML = this.unavailable;
        domValues.nbrEtage.setAttribute("id", "appendNbrEtage");
        domValues.longueur.innerHTML = this.unavailable;
        domValues.longueur.setAttribute("id", "appendLongueur");
        domValues = this._updateDomTr(domValues);
        $(this.bodyDOM).append(domValues.newTr);
    }

    addComponentToTable(component, predecessorComponent, detailsQuery, callback) {
        //TODO Have access to its predecessor (Should all information about it.)
        //TODO
        var domValues = this._buildDOMStructuredJSON();
        domValues.actionButton.appendChild(this.htmlTagFactory.createRemoveRowButton());
        domValues.nomNoeud.innerHTML = component.attrs.id;
        domValues.nomNoeud.setAttribute("id", "node_" + component.attrs.id);
        domValues.suiveur.innerHTML = this.unavailable;
        domValues.suiveur.setAttribute("id", "suiveur_" + component.attrs.id); //Add an id to make it simplier to modify the predecessor
        domValues.predecesseur.innerHTML = predecessorComponent == undefined ? this.unavailable : predecessorComponent.attrs.id; //TODO Put in place predecessor
        domValues.predecesseur.setAttribute("id", "predecesseur_" + component.attrs.id);
        domValues.type.appendChild(this.htmlTagFactory.createTypeSelectTag(component.attrs.id, detailsQuery));
        domValues.type.setAttribute("id", "type_" + component.attrs.id);
        domValues.typeChauffage.innerHTML = this.unavailable; //TODO Create a option select
        domValues.typeChauffage.setAttribute("id", "chauffage_" + component.attrs.id);
        domValues.typeLogement.innerHTML = this.unavailable; // TODO Create a option select
        domValues.typeLogement.setAttribute("id", "logement_" + component.attrs.id);
        domValues.surfaceHabitable.innerHTML = this.unavailable; //TODO Create input for surfaceHabitablenumber
        domValues.surfaceHabitable.setAttribute("id", "habitable_" + component.attrs.id);
        domValues.nbrEtage.innerHTML = this.unavailable;
        domValues.nbrEtage.setAttribute("id", "nombre_etage_" + component.attrs.id);
        domValues.nbrLogement.innerHTML = this.unavailable;
        domValues.nbrLogement.setAttribute("id", "number_housing_" + component.attrs.id);
        if (component.attrs.id.includes("A")) {
            domValues.longueur.appendChild(this.htmlTagFactory.createLongueurInput(component.attrs.id));
            domValues.longueur.setAttribute("id", "longueur_" + component.attrs.id);
        } else {
            domValues.longueur.innerHTML = this.unavailable;
        }
        this._findFollower(component.attrs.id, predecessorComponent);
        domValues = this._updateDomTr(domValues);
        $(this.bodyDOM).append(domValues.newTr);
        callback(domValues.type, domValues.longueur);
    }

    _findFollower(currentComponentId, predecessor) {
        if (predecessor != undefined) {
            $("#suiveur_" + predecessor.attrs.id).text(currentComponentId);
        }
    }
    _appendButtonClickEvent(appendButton, callback) {
        $(appendButton).click(function(event) {
            var nomNoeud = $("#appendNode").val();
            var predecesseur = $("#appendPredecessor").val();
            var component = componentFactory.buildComponentFromString(nomNoeud); // Build Object that ressemble the one from Konva
            predecesseur = {
                attrs: {
                    id: predecesseur
                }
            };
            handleDomChangeFromAppendRow(component, predecesseur);
            callback(component, predecesseur);
        })
    }
}