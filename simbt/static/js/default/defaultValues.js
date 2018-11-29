import {
    componentIdHandler
} from "../handler/componentIdHandler";

class DefaultValues {
    constructor() {
        this.defaultRed = 'red';
        this.defaultBlue = 'blue';
        this.defaultGreen = 'green';
        this.defaultBlack = 'black';
        this.defaultGrey = 'grey';

        this.defaultRadius = 30;
        this.defaultFill = this.defaultRed; // Can be changed to any other colors
        this.defaultStrokeWidth = 2

        this.defaultTransfoWidth = 100;
        this.defaultTransfoHeight = 150;
    }

    /*
      @PARAM :  newId : Boolean default true
      @RETURN String : Transformer Id -> T1
    */
    generateTransformerIdString(newId = true) {
        return "T" + componentIdHandler.getTransformerId(newId);
    }

    /*
      @PARAM :  newId : Boolean default true
      @RETURN String : Client Id -> C1
    */
    generateClientIdString(newId = true) {
        return "C" + componentIdHandler.getClientId(newId);
    }

    /*
      @PARAM :  newId : Boolean default true
      @RETURN String : Conductor Id -> A1
    */
    generateConductorIdString(newId = true) {
        return "A" + componentIdHandler.getConductorId(newId);
    }

    /*
      @PARAM :  newId : Boolean default true
      @RETURN String : Node Id -> N1
    */
    generateNodeIdString(newId = true) {
        return "N" + componentIdHandler.getNodeId(newId);
    }

    /*
      @PARAM : componentId : String i.e A1
      @RETURN : String : -> A1_Group
    */
    generateGroupIdString(componentId) {
        return componentId + "_Group";
    }

    /*
      @PARAM :  newId : Boolean default false
      @RETURN String : Transfomer Konva component Id -> T1_text
    */
    generateTransformerText(newId = false) {
        return "T" + componentIdHandler.getTransformerId(newId) + "_text";
    }

    /*
      @PARAM :  newId : Boolean default false
      @RETURN String : Client Konva component Id -> C1_text
    */
    generateClientText(newId = false) {
        return "C" + componentIdHandler.getClientId(newId) + "_text";
    }

    /*
      @PARAM :  newId : Boolean default false
      @RETURN String : Conductor Text Id -> A1_text
    */
    generateConductorText(newId = false) {
        return "A" + componentIdHandler.getConductorId(newId) + "_text";
    }

    /*
      @PARAM :  newId : Boolean default false
      @RETURN String : Node Text Id -> N1_text
    */
    generateNodeText(newId = false) {
        return "N" + componentIdHandler.getNodeId(newId) + "_text";
    }

    /*
      @PARAM : value : Number from JSON
    */
    setNodeId(value) {
        componentIdHandler.setNodeId(value);
    }

    /*
      @PARAM : value : Number from JSON
    */
    setTransformerId(value) {
        componentIdHandler.setTransformerId(value);
    }

    /*
      @PARAM : value : Number from JSON
    */
    setClientId(value) {
        componentIdHandler.setClientId(value);
    }

    /*
      @PARAM : value : Number from JSON
    */
    setConductorId(value) {
        componentIdHandler.setConductorId(value);
    }
}

var defaultValues = new DefaultValues();

export {
    defaultValues
}