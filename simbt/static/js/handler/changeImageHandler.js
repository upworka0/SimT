import {
    getNewImage,
    getNew
} from '../factory/konvaElementFactory.js';
var $ = require('jQuery');
var Konva = require('konva');

const BASE_PATH = "/static/img";
const imagesPath = {
    selectedHouse: BASE_PATH + "/selectedHouse.svg",
    selectedConnectedHouse: BASE_PATH + "/selectedConnectedHouse.svg",
    selectedWarningHouse: BASE_PATH + "/selectedWarningHouse.svg",
    selectedErrorHouse: BASE_PATH + "/selectedErrorHouse.svg",
    house: BASE_PATH + "/house.svg",
    connectedHouse: BASE_PATH + "/connectedHouse.svg",
    warningHouse: BASE_PATH + "/warningHouse.svg",
    errorHouse: BASE_PATH + "/errorHouse.svg",
    selectedTransformateur: BASE_PATH + "/selectedTransformateur.svg",
    selectedConnectedTransformateur: BASE_PATH + "/selectedConnectedTransformateur.svg",
    selectedWarningTransformateur: BASE_PATH + "/selectedWarningTransformateur.svg",
    selectedErrorTransformateur: BASE_PATH + "/selectedErrorTransformateur.svg",
    transformateur: BASE_PATH + "/transformateur.svg",
    connectedTransformateur: BASE_PATH + "/connectedTransformateur.svg",
    warningTransformateur: BASE_PATH + "/warningTransformateur.svg",
    errorTransformateur: BASE_PATH + "/errorTransformateur.svg"
}

const componentState = {
    error: -2,
    warning: -1,
    notConnected: 0,
    connected: 1,
    missingValues: 2
};

var selectedNode = null;

class ChangeImageHandler {

    static resetSelection(component) {
        selectedNode = null
        ChangeImageHandler.selectComponent(component, false);
    }

    static selectComponent(component, isSelected) {
        if (selectedNode != null && component.attrs.id != selectedNode.attrs.id) {
            ChangeImageHandler.resetSelection(selectedNode);
        }
        var newImage = ChangeImageHandler.__generateNewImage(component);
        ChangeImageHandler.__fetchVisual(component, newImage, isSelected);
    }

    static connectComponent(component) {
        let isSelected = false;
        var newImage = ChangeImageHandler.__generateNewImage(component);
        ChangeImageHandler.__fetchVisual(component, newImage, isSelected, componentState.connected);
    }

    static warningComponent(component) {
        let isSelected = false;
        var newImage = ChangeImageHandler.__generateNewImage(component);
        ChangeImageHandler.__fetchVisual(component, newImage, isSelected, componentState.warning);
    }

    static errorComponent(component) {
        let isSelected = false;
        var newImage = ChangeImageHandler.__generateNewImage(component);
        ChangeImageHandler.__fetchVisual(component, newImage, isSelected, componentState.error);
    }

    static missingValues(component) {
        let isSelected = false;
        var newImage = ChangeImageHandler.__generateNewImage(component);
        ChangeImageHandler.__fetchVisual(component, newImage, isSelected, componentState.missingValues);
    }

    static __generateNewImage(component) {
        var newImage = new Image();
        newImage.onload = function() {
            component.image(newImage);
            component.getLayer().draw()
        }

        return newImage;
    }
    /*
        ARGS :
            component : konva object - The object that is selected on the user interface
            newImage : Image object that will hold the new image to display on the user interface
            isSelected : Boolean - Just keeps track if the component is selected or not
            componentState : Number - Keeps track of what state are we on; warning, error, connected, not connected, missing values

        componentState values:
           -2 - Error
           -1 - Warning
            0 - Not Connected
            1 - Connected
            2 - Missing Values
    */
    static __fetchVisual(component, newImage, isSelected, componentState) {
        if (!component.attrs.id.includes('A') && !component.attrs.id.includes('N')) {
            var value = component.attrs.image.attributes.src.nodeValue;
            if (component.attrs.id.includes("C")) {
                if (componentState == undefined) {
                    if (isSelected == true) {
                        newImage.src = ChangeImageHandler.__getSelectedClientImage(value);
                    } else {
                        newImage.src = ChangeImageHandler.__getClientImage(value);
                    }
                } else {
                    newImage.src = ChangeImageHandler.__getClientValueImage(componentState);
                }
            } else if (component.attrs.id.includes('T')) {
                if (componentState == undefined) {
                    if (isSelected == true) {
                        newImage.src = ChangeImageHandler.__getSelectedTransformateur(value);
                    } else {
                        newImage.src = ChangeImageHandler.__getTransformateur(value);
                    }
                } else {
                    newImage.src = ChangeImageHandler.__getTransformateurValueImage(componentState);
                }
            }
        } else if (component.attrs.id.includes('A')) {
            ChangeImageHandler.__selectConductor(component, isSelected);
        } else if (component.attrs.id.includes('N')) {
            ChangeImageHandler.__selectNode(component, isSelected);
        }
        selectedNode = component;
    }

    static __getClientValueImage(componentState) {
        switch (componentState) {
            case componentState.notConnected:
                return imagesPath.house;
            case componentState.connected:
                return imagesPath.connectedHouse;
            case componentState.error:
                return imagesPath.errorHouse;
            case componentState.warning:
                return imagesPath.warningHouse;
            case componentState.missingValues:
                //TODO Add missingValues house
                break;
        }
    }

    static __getTransformateurValueImage(componentState) {
        switch (componentState) {
            case componentState.notConnected:
                return imagesPath.transformateur;
            case componentState.connected:
                return imagesPath.connectedTransformateur;
            case componentState.warning:
                return imagesPath.warningTransformateur;
            case componentState.error:
                return imagesPath.errorHouse;
            case componentState.missingValues:
                //TODO Add missing values transformateur
                break;
        }
    }

    static __selectConductor(conducteur, isSelected) {
        selectedNode = conducteur;
        if (isSelected == true) {
            conducteur.shadowEnabled(true);
            conducteur.shadowColor("blue");
            conducteur.shadowBlur(10);
        } else {
            conducteur.shadowEnabled(false);
        }
        conducteur.getLayer().draw();
    }

    static __selectNode(node, isSelected) {
        selectedNode = node;
        if (isSelected == true) {
            node.shadowEnabled(true);
            node.shadowColor("blue");
            node.shadowBlur(10);
        } else {
            node.shadowEnabled(false);
        }
        node.getLayer().draw();
    }

    static __getSelectedTransformateur(value) {
        switch (true) {
            case value == imagesPath.transformateur:
                return imagesPath.selectedTransformateur;
            case value == imagesPath.connectedTransformateur:
                return imagesPath.selectedConnectedTransformateur;
            case value == imagesPath.warningTransformateur:
                return imagesPath.selectedWarningTransformateur;
            case value == imagesPath.errorTransformateur:
                return imagesPath.selectedErrorTransformateur;
        }
    }

    static __getTransformateur(value) {
        switch (true) {
            case value == imagesPath.selectedTransformateur:
                return imagesPath.transformateur;
            case value == imagesPath.selectedConnectedTransformateur:
                return imagesPath.connectedTransformateur;
            case value == imagesPath.selectedWarningTransformateur:
                return imagesPath.warningTransformateur;
            case value == imagesPath.selectedErrorTransformateur:
                return imagesPath.errorTransformateur;
        }
    }

    static __getSelectedClientImage(value) {
        switch (true) {
            case value == imagesPath.house:
                return imagesPath.selectedHouse;
            case value == imagesPath.connectedHouse:
                return imagesPath.selectedConnectedHouse;
            case value == imagesPath.warningHouse:
                return imagesPath.selectedWarningHouse;
            case value == imagesPath.errorHouse:
                return imagesPath.selectedErrorHouse;
        }
    }

    static __getClientImage(value) {
        switch (true) {
            case value == imagesPath.selectedHouse:
                return imagesPath.house;
            case value == imagesPath.selectedConnectedHouse:
                return imagesPath.connectedHouse;
            case value == imagesPath.selectedWarningHouse:
                return imagesPath.warningHouse;
            case value == imagesPath.selectedErrorHouse:
                return imagesPath.errorHouse;
        }
    }
}

export {
    ChangeImageHandler
}