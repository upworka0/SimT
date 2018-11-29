import {
    ComponentListModel
} from "../model/componentListModel.js";
var $ = require('jQuery');

class ComponentListManager {
    /**
     * @class ComponentListManager
     * @param {JSON Object} componentType it is like an enum for the different possible component that can be added, it is mostly used in appendNewComponents function
     */
    constructor(componentType) {
        this.componentType = componentType;
    }

    /**
     *  Retrieve the list of component 
     *  stored in ComponentListModel
     * 
     * @requires ComponentListModel
     */
    getComponentList() {
        return ComponentListModel.getComponentList();
    }

    /**
     *  Save a new array to
     *  the ComponentListModel
     * 
     * @requires ComponentListModel
     * @param {Array} value 
     */
    setComponentList(value) {
        ComponentListModel.setComponentList(value);
    }
    /**
     * This function retrieve the list of components
     * stored in the componentListModel then removes it.
     * Afterward, it sets the new array to the componentListModel
     * 
     * @requires componentList from getComponentList method in this object
     * @param {JSON Object} component JSON object with a stucture defined in appendNewComponents in this file
     */
    removeComponent(component) {
        let i = ComponentListModel.getComponentList().indexOf(component);
        let componentList = ComponentListModel.getComponentList();
        componentList.splice(i, 1);
        ComponentListModel.setComponentList(componentList);
    }
    /**
     * This function returns the successor of
     * a particular component. The component is
     * represented as a json object and we find 
     * the predecessor using the name of the node
     * and the successor attribute from the object
     * in componentList array
     * 
     * @requires componentList from getComponentList method in this object
     * @param {JSON Object} component JSON object with a stucture defined in appendNewComponents in this file
     * @returns {JSON Object} successor  
     */
    getSuccesseur(component) {
        var successeur = ComponentListModel.getComponentList().filter(function(object) {
            if (object.nom_du_noeud == component.successeur) {
                return object;
            }
        });
        return successeur;
    }

    /**
     * This function returns the predecessor of
     * a particular component. The component is
     * represented as a json object and we find 
     * the predecessor using the name of the node
     * and the predecessor attribute from the object
     * in componentList array
     * 
     * @requires componentList from getComponentList method in this object
     * @param {JSON Object} component JSON object with a stucture defined in appendNewComponents in this file
     * @returns {JSON Object} predecesseur  
     */
    getPredecesseur(component) {
        var predecesseur = this.getComponentList().filter(function(object) {
            if (object.nom_du_noeud == component.predecesseur) {
                return object;
            }
        });
        return predecesseur;
    }
    /**
     * This function return an array
     * of components that has a relation
     * to the componentId: i.e componentID == T1
     * so all the conductor related to T1 will be
     * in the array
     * 
     * @requires componentList from getComponentList method in this object
     * @param {String} componentId should be a client or transformer ID
     * @returns {Array} relationships is a an array of components from componentListManager
     */
    getComponentFirstLevelRelationship(componentId) {
        console.log(this.getComponentList());
        return this.getComponentList().filter((object) => componentId == object.successeur || componentId == object.predecesseur);
    }

    /**
        Not currently in use - 2018-04-03

        fetch component using its id.

        @requires ComponentListModel -> Array of json objects (components)
        @param {componentId} -> String i.e "C1" (Client  1)
        @returns {JSON object} component[0]
    */
    fetchComponent(componentId) {
        let list = this.getComponentList()
        let component = list.filter((value) => value.nom_du_noeud == componentId);
        return component[0];
    }

    /**
     *  This function refresh the component using its Id,
     *  when it is found, it will change the predecessor
     *  with the new one 
     *  
     * @requires componentList from getComponentList method in this object
     * @param {String} componentId also called nom_du_noeud
     * @param {String} predecesseurId the predecessor of the componentId
     */
    updateComponentPredecesseur(componentId, predecesseurId) {
        let list = this.getComponentList();
        for (let i = 0; i < list.length; i++) {
            if (predecesseurId == list[i].nom_du_noeud) {
                list[i].predecesseur = componentId;
                if (list[i].successeur == componentId) {
                    list[i].successeur = "";
                }
                break;
            }
        }
        this.setComponentList(list);
    }

    /**
     *  This function refresh the component using its Id,
     *  when it is found, it will change the successor
     *  with the new one 
     *  
     * @requires componentList from getComponentList method in this object
     * @param {String} componentId also called nom_du_noeud
     * @param {String} succeeseurId the predecessor of the componentId
     */
    updateComponentSuccesseur(componentId, successeurId) {
        let list = this.getComponentList();
        for (let i = 0; i < list.length; i++) {
            if (successeurId == list[i].nom_du_noeud) {
                list[i].successeur = componentId;
                if (list[i].predecesseur == componentId) {
                    list[i].predecesseur = "";
                }
                break;
            }
        }
        this.setComponentList(list);
    }

    /**
     *  This function takes care of changing the alias
     *  given from the user in the user interface
     *  
     * @requires componentList from getComponentList method in this object
     * @param {String} componentId also called nom_du_noeud
     * @param {String} componentAlias this would be a name a user would have given to the component
     */
    updateComponentAlias(componentId, componentAlias) {
        let list = ComponentListModel.getComponentList();
        list.forEach(function(element) {
            if (element.nom_du_noeud == componentId) {
                element.noeud_alias = componentAlias;
            }
        });
        ComponentListModel.setComponentList(list);
    }

    /**
     *  This function handles the last part of loading
     *  the data stored in the database to the front-end
     * 
     * @requires componentList from getComponentList method in this object
     * @param {JSON Object - Konva DOM object} component is an object generated by Konva.JS 
     */
    updateComponentImage(component) {
        let list = this.getComponentList();
        for (let i = 0; i < list.length; i++) {
            if (!component.attrs.id.includes("A") && !component.attrs.id.includes("N")) {
                if (list[i].nom_du_noeud == component.attrs.id) {
                    list[i].image = component.attrs.image.attributes.src.nodeValue;
                    return list;
                }
            }
        }
    }

    /**
     * This function takes in a complete object that was altered
     * and will update a component that has the same "nom_du_noeud",
     * also known as the componentId.
     * 
     * Afterwards the Array will be used to update the current array 
     *  
     * @requires componentList from getComponentList method in this object
     * @param {JSON Object} component JSON object with a stucture defined in appendNewComponents in this file
     */
    updateComponentData(component) {
        if (component.nom_du_noeud == undefined) return;
        let list = this.getComponentList();
        for (let i = 0; i < list.length; i++) {
            if (list[i].nom_du_noeud == component.nom_du_noeud) {
                list[i] = component;
                break;
            }
        }
        this.setComponentList(list);
    }

    /**
     *  This function is built to handle different situations which explains
     *  why it has many default values. It is built to handle a new Client, Transformer
     *  Node or conductor. In all those different case, you may not have a component that 
     *  is selected or need to the position of the tip of a conductor or its first coordinates.
     * 
     *  Any time you want to add a new component to the user interface, it must go through here
     *  to keep track of the new components that are added.
     * 
     * 
     * @requires componentType JSON Object that uses the following structure { transfromateur: 0, logement: 1, conducteur:2, noeud: 3}. It acts as a enum
     * @requires __handlePredAndSuc Function that make sure the predecessor and the successor are in place  when creating a new object for the componentList
     * @requires componentList from getComponentList method in this object
     * @param {JSON Object - Konva Object} component 
     * @param { Number } type This represents the type that of the component that we have to handle. Each component has its own attributes 
     * @param {JSON Object - Konva Object} firstSelected a DOM/KOnva object that represents the first object selected (UI), by default undefined
     * @param {JSON Object - Konva Object} secondSelected a DOM/Konva object that represents the second object selected (UI), by default undefined
     * @param {JSON Object} tipConductorPosition an object using this format {x: { Number }, y: { Number }} 
     * @param {JSON Object} conductorFirstConductors an object using this format {x: { Number }, y: { Number }}. Those are conductor positions
     */
    appendNewComponents(component, type, firstSelected = undefined, secondSelected = undefined, tipConductorPosition = undefined, conductorFirstConductors = undefined) {
        let list = this.getComponentList();
        var object = this.__handlePredAndSuc(firstSelected, secondSelected, component);
        switch (true) {
            case type == this.componentType.tranformateur:
                list.push({
                    nom_du_noeud: component.attrs.id,
                    noeud_alias: "",
                    successeur: object == undefined ? "None" : object.successeur,
                    predecesseur: object == undefined ? "None" : object.predecesseur,
                    type_de_transformateur: "",
                    position_x: component.parent.attrs.x,
                    position_y: component.parent.attrs.y,
                    image: component.attrs.image.attributes.src.nodeValue
                })
                break;
            case type == this.componentType.logement:
                list.push({
                    nom_du_noeud: component.attrs.id,
                    noeud_alias: "",
                    successeur: object == undefined ? "None" : object.successeur,
                    predecesseur: object == undefined ? "None" : object.predecesseur,
                    type_de_logement: "",
                    type_de_chauffage: "",
                    logement_code_saison: "",
                    surface_habitable: "",
                    nombre_etage: "",
                    nombre_de_logement: "",
                    position_x: component.parent.attrs.x,
                    position_y: component.parent.attrs.y,
                    image: component.attrs.image.attributes.src.nodeValue
                });
                break;
            case type == this.componentType.conducteur:
                list.push({
                    nom_du_noeud: component.attrs.id,
                    noeud_alias: "",
                    successeur: object == undefined ? "None" : object.successeur,
                    predecesseur: object == undefined ? "None" : object.predecesseur,
                    type_de_conducteur: "",
                    longueur: 0,
                    position_x: component.parent.attrs.x,
                    position_y: component.parent.attrs.y,
                    tipConductorPosition: tipConductorPosition, // Initial element should be undefined
                    firstCoordinates: conductorFirstConductors // Initial element should be undefined
                });
                break;
            case type == this.componentType.noeud:
                list.push({
                    nom_du_noeud: component.attrs.id,
                    noeud_alias: "",
                    successeur: object == undefined ? "None" : object.successeur,
                    predecesseur: object == undefined ? "None" : object.predecesseur,
                    position_x: component.attrs.x,
                    position_y: component.attrs.y
                });
            default:
                //TODO Houston we have a problem!
                break;
        }
        this.setComponentList(list);
    }

    /**
     *  @private 
     *  @private @description  
     *      In this case, private method doesn't really exists.
     *      Although, I have kept an OOP (Object Oriented Programming)
     *      structure, so functions that uses __ in fron of their name
     *      are meant to be used only inside this class.
     * 
     *  @function @description
     *      This methods make sure that the object that we are adding
     *      to the list has its successor and predecessor.
     * 
     * @requires __updatePredAndSucc Update the componentListModel
     * @param {JSON Object - Konva Object} firstSelected 
     * @param {JSON Object - Konva Object} secondSelected 
     * @param {JSON Object - Konva Object} component 
     * @returns {JSON Object} successeurPredObject It has the following structure { successeur : "C1", predecesseur : "T1" }  
     */
    __handlePredAndSuc(firstSelected, secondSelected, component) {
        if (firstSelected == undefined && secondSelected == undefined) return undefined; //Nothing to do here, bye!
        var successeurPredObject = {};

        let firstSelectedId = firstSelected.attrs == undefined ? firstSelected.nom_du_noeud : firstSelected.attrs.id;
        let secondSelectedId = secondSelected.attrs == undefined ? secondSelected.nom_du_noeud : secondSelected.attrs.id;

        if (firstSelectedId.includes('C') || secondSelectedId.includes('C')) {
            successeurPredObject = firstSelected.attrs.id.includes("C") == true ? {
                successeur: firstSelectedId,
                predecesseur: secondSelectedId
            } : {
                successeur: secondSelectedId,
                predecesseur: firstSelectedId
            };
        } else {
            var replaceChar = firstSelectedId.includes('N') ? "N" : "A";
            successeurPredObject = Number(firstSelectedId.replace(replaceChar, "")) > Number(secondSelectedId.replace(replaceChar, "")) ? {
                successeur: firstSelectedId,
                predecesseur: secondSelectedId
            } : {
                successeur: secondSelectedId,
                predecesseur: firstSelectedId
            }

        }
        this.__updatePredAndSucc(successeurPredObject, component);
        return successeurPredObject;
    }

    /**
     * 
     *  @private 
     *  @private @description  
     *      In this case, private method doesn't really exists.
     *      Although, I have kept an OOP (Object Oriented Programming)
     *      structure, so functions that uses __ in fron of their name
     *      are meant to be used only inside this class.
     *  
     * @function @description
     *      This function update the successor and the successor 
     *      to have the component as their successor or predecessor.
     *      It helps keep track of everyone inside the array.
     * 
     * @requires componentList from getComponentList method in this object
     * @param {JSON Object} successeurPredObject It has the following structure { successeur : "C1", predecesseur : "T1" }   
     * @param {JSON Objet - Konva Object} component 
     */
    __updatePredAndSucc(successeurPredObject, component) {
        var list = ComponentListModel.getComponentList();
        var premierElement = list.filter(function(object) {
            if (object.nom_du_noeud == successeurPredObject.successeur) {
                return object;
            }
        });

        var secondElement = list.filter(function(object) {
            if (object.nom_du_noeud == successeurPredObject.predecesseur) {
                return object;
            }
        });

        premierElement[0].predecesseur = component.attrs.id;
        secondElement[0].successeur = component.attrs.id

        for (let i = 0; i < list.length; i++) {
            if (premierElement[0].nom_du_noeud == list[i].nom_du_noeud) {
                list[i] = premierElement[0];
            }

            if (secondElement[0].nom_du_noeud == list[i].nom_du_noeud) {
                list[i] = secondElement[0];
            }
        }
        ComponentListModel.setComponentList(list);
    }

}

export {
    ComponentListManager
}