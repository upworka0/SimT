import {
    extractComponentTypeFromNodeName
} from "./../handler/newComponentHandler"
/*

  Take care of generating all required html eleement
  with the required components with them for HTML

*/
module.exports = class HtmlTagElementFactory {
    constructor() {
        this.typeListID = {
            transformer: "transformerTypeList",
            conductor: "conductorTypeList",
            logement: ""
        }
    }

    createTrElement() {
        return document.createElement('tr');
    }

    createTdElement() {
        return document.createElement('td');
    }

    createThElement() {
        return document.createElement('th');
    }

    createTheadElement() {
        return document.createElement("thead");
    }

    createTbodyElement() {
        return document.createElement("tbody");
    }

    createAppendRowButton() {
        /*
          create an append button

          @PURPOSE : Create a new row which represents a new
          component inside the table

        */

        var appendButton = this._createButtonElement();
        $(appendButton).text("+");
        appendButton.setAttribute("id", "appendRowButton");
        return appendButton;
    }

    createRemoveRowButton() {
        /*
          create a remove button

          @PURPOSE : Remove a row which removes the
          component as well.

        */
        var removeRowButton = this._createButtonElement();
        $(removeRowButton).text("-");
        removeRowButton.setAttribute("id", "removeRowButton");
        return removeRowButton;
    }

    createPredecessorSelectTag(componentList) {
        var selectTag = this._createSelectElement();
        selectTag = this._buildingPredecessorOptions(selectTag, componentList);
        selectTag.setAttribute("id", "appendPredecessor");
        return selectTag;
    }

    createTypeSelectTag(componentID, componentDetails) {
        /*
          Description : Create a select dom element
          for the tble.
          @ARG : componentID -> String i.e T1
        */
        // var typeRegex = /([T]{1}[0-9]{1,3}|[A]{1}[0-9]{1,3}|[C]{1}[0-9]{1,3}|[N]{1}[0-9]{1,3})/;
        var selectTag = this._createSelectElement();
        var valueType = extractComponentTypeFromNodeName(componentID);
        switch (true) {
            case valueType == 0:
                //TODO Generate Transformer ID
                selectTag.setAttribute("id", this.typeListID.transformer);
                // ** DEPRECATED **
                // $(selectTag).change(function(event){
                //     let parent = $(this).parent().attr("id");
                //     console.log(typeRegex.exec(parent));
                //     //TODO Extract ID from the self object
                //     // componentDetails.getTransformerDetails(self, function()){
                //     //
                //     // }
                // });
                break;
            case valueType == 1:
                //TODO Generate Client ID
                selectTag.setAttribute("id", this.typeListID.logement);
                // ** DEPRECATED **
                // $(selectTag).change(function(event){
                //   console.log(self);
                //   let parent = $(this).parent();
                //   console.log(parent);
                //   //TODO Extract ID from the self object
                //   // componentDetails.getLodgingDetails(self, function(){
                //   //
                //   // });
                // });
                break;
            case valueType == 2:
                //TODO Generate Arc ID
                selectTag.setAttribute("class", this.typeListID.conductor);
                // ** DEPRECATED **
                // $(selectTag).change(function(event){
                //   let parent = $(this).parent().attr("id");
                //   console.log(typeRegex.exec(parent));
                //   //TODO Extract ID from the self object
                //   // componentDetails.getConductorDetails(self, function(){
                //   //
                //   // })
                // });
                break;
            case valueType == 3:
                /*
                  Node select  tag
                */
                selectTag.setAttribute("disabled", true);
                break;
            default:
                //TODO
                break;
        }

        return selectTag;
    }

    createNewElementOptionChoices() {
        /*

          Build a select tag with all the client possible choices

        */
        var selectElement = this._createSelectElement();
        var conductorElementOption = this._createOptionElement();
        var chargeElementOption = this._createOptionElement();
        var nodeElementOption = this._createOptionElement();
        $(conductorElementOption).text("Arc");
        $(chargeElementOption).text("Client");
        $(nodeElementOption).text("Noeud");
        selectElement.appendChild(conductorElementOption);
        selectElement.appendChild(chargeElementOption);
        selectElement.appendChild(nodeElementOption);
        selectElement.setAttribute("id", "appendNode");
        return selectElement;
    }

    createTypeSelect() {
        optionElement = this._createOptionElement();
        optionElement.setAttribute("id", "");
        return optionElement;
    }

    createHabitableAreaInput(dom) {
        var areaInput = this._createInputElement()
        areaInput.setAttribute("id", "area_" + dom);
        areaInput.setAttribute("type", "number");
        return areaInput;
    }

    createNumberOfHousingInput(dom) {
        var housingInput = this._createInputElement();
        housingInput.setAttribute("id", "housings_" + dom);
        housingInput.setAttribute("type", "number");
        return housingInput;
    }

    createLongueurInput(dom) {
        var longueurInput = this._createInputElement();
        longueurInput.setAttribute("id", "arc_longueur_" + dom);
        longueurInput.setAttribute("type", "number");
        return longueurInput;
    }

    createNombreEtageInput(dom) {
        var nbrEtage = this._createInputElement();
        nbrEtage.setAttribute("id", "etage_" + dom);
        nbrEtage.setAttribute("type", "number");
        return nbrEtage;
    }

    _buildingPredecessorOptions(selectDOM, componentList) {
        for (let i = 0; i < componentList.length; i++) {
            let componentType = extractComponentTypeFromNodeName(componentList[i].nom_du_noeud);
            var optionTag = this._createOptionElement();
            switch (true) {
                case componentType == 2: // Arc
                case componentType == 3: // Node
                    //Create option for Select Tag.
                    optionTag.innerHTML = componentList[i].nom_du_noeud;
                    optionTag.setAttribute("value", componentList[i].nom_du_noeud);
                    selectDOM.appendChild(optionTag);
                    break;
            }
        }
        return selectDOM;
    }

    _createInputElement() {
        return document.createElement("input");
    }

    _createButtonElement() {
        return document.createElement('button');
    }
    _createSelectElement() {
        var selectElement = document.createElement('select');
        return selectElement;
    }

    _createOptionElement() {
        var optionElement = document.createElement('option');
        return optionElement;
    }
}