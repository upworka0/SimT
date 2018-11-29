import {
    selectTool,
    moveTool,
    createLine,
    createTransfo,
    createClient,
} from "./toolboxHandler/toolbox";
import {
    selectConductor,
    selectTranformer,
    selectClient,
    selectSelectTool,
} from "./toolboxHandler/toolbox";
import {
    displayConductorSpecificationDetails,
    displayHeatingSpecificationDetails,
    displayLodgingSpecificationDetails,
    displayTransformerSpecificationDetails,
} from './specificationHandler/specifications';
import {
    getNewImage,
    getNewLine,
    getNewText,
    getNewNode,
    getNewGroup,
} from './factory/konvaElementFactory';
import {
    onElementPredecessorAndSuccessorFollowUp,
    onElementSuccessorFollowUp,
    onElementPredecessorFollowUp,
} from './events/onElementMove'
import {
    defaultValues
} from './default/defaultValues';
import {
    konvaComponentEvents
} from './events/konvaComponentsEvents.js';
import {
    ComponentListManager
} from './manager/componentListManager';
import {
    ChangeImageHandler
} from './handler/changeImageHandler.js';
import {
    addEventToForm
} from './events/studySpecFormEvent';
import {
    DataTableHandler
} from './handler/dataTableHandler.js';
import {
    isObject
} from "util";
require('./events/accordionEvents.js');

var Konva = require('konva');
var $ = require('jQuery');

/*             Global Konva                     */
var stage = null;
var layer = new Konva.Layer();


const componentType = {
    transformateur: 0,
    logement: 1,
    conducteur: 2,
    noeud: 3,
};

const componentListManager = new ComponentListManager(componentType);

/*             Global Konva                      */

/*                Global DOM                          */

var navigation = document.getElementById("navigation");
var toolboxPane = document.getElementById("toolboxPane");
var specificationPane = document.getElementById("specificationPane");

var transformerSpecs = document.getElementById("transformerSpecs");
var clientSpecs = document.getElementById("clientSpecs");
var conductorSpecs = document.getElementById("conductorSpecs");
var nodeSpecs = document.getElementById("nodeSpecs");

var transformerSpecsForm = document.getElementById("transformer_form");
var conductorSpecsForm = document.getElementById("conductor_form");
var clientSpecsForm = document.getElementById("client_form");
var nodeSpecsForm = document.getElementById("node_form");

var elementName = document.getElementById("elementName");

var stageParent = document.getElementById("stage-parent");
var containerDOM = document.getElementById("container");


var zoomInButton = document.getElementById("zoomInButton");
var zoomOutButton = document.getElementById("zoomOutButton");
var zoomStatus = document.getElementById("zoomStatus");

var message = document.getElementById("message");
var positionInfo = document.getElementById("positionInfo");
var componentListDOM = document.getElementById("component-list"); // January 5 2018 -> Related to table, maybe implemented later


/*                  Global DOM                          */


var menuDisplayed = false;
// Menu box DOM
var menuBox = null; // context menu (right click menu)

/*         Zoom Variable           */

var zoomLevel = 1;
var zoomStep = 0.10;
var zoomInLimit = 3;

/*         Zoom Variable           */

/*         Conductor Variable           */

var firstSelectedNode = null; // Keep track of first node selected
var secondSelectedNode = null; // keep track of second node selected

var elementSelected = null;

// const maxWidth = 1400;
// const maxHeight = 800;

// Delta X and Delta Y
var currentLayerPositionX = 0;
var currentLayerPositionY = 0;

var originalLayerPositionX = 0;
var originalLayerPositionY = 0;

// Start drag X and Y.
// Ending drag is in event below
var layerStartDrag;

var stageBoundPositionX;
var stageBoundPositionY;

// var specificationTransformatorModal = document.getElementById("specification-transformateur-modal");
// var specificationClientModal = document.getElementById("specification-client-modal");
// var specificationConductorModal = document.getElementById("specification-conductor-modal");

var elementMoved = false;
var currentPosition = {
    x: 0,
    y: 0
};
var draggedComponentOriginalPosition = {
    x: 0,
    y: 0
};

var lineFirstPoint = true;
var isLineOnElement = false;

var firstCoordinates = null;

var positionTable = 0; // position in array for table at the bottom

/**
 * This function is a callback 
 * for the specification form.
 * 
 * This callback is used for the
 * alias part of the some specification
 * form  
 * 
 * @requires componentListManager 
 * @param {String} componentId 
 * @param {String} alias 
 */
function eventFormCallback(componentId, alias) {
    componentListManager.updateComponentAlias(componentId, alias);
}

/**
 *  This function takes in a konva group that
 *  holds a node object and returns this node 
 *  
 * @param {JSON Object - Konva Object} nodeGroup 
 * @returns {Konva object} node object
 */
function extractNodeObjectFromNodeGroup(nodeGroup) {
    // Search for the component in group
    for (var i = 0; i < nodeGroup.children.length; i++) {
        if (nodeGroup.children[i].className == "Circle") {
            return nodeGroup.children[i];
        }
    }
}

/**
 *  This function add the event mousedown to
 *  a Konva object
 * 
 *  This event sets the canva attribute draggable
 *  to FALSE then set the parent draggable attribute of the 
 *  argument component to TRUE to the component is the only
 *  one to move
 * 
 *  
 * @param {JSON Object - Konva Object} component 
 */
function onMouseDownComponentEvent(component) {
    component.addEventListener("mousedown", function(event) {
        elementMoved = true; // Global variable - Fix Bug related to moving component that changed the user position in the canvas
        stage.draggable(false);
        component.parent.draggable(true); // Uses the draggable attribte in the parent object since the component is in a group
        draggedComponentOriginalPosition = {
            x: component.parent.attrs.x,
            y: component.parent.attrs.y
        };
    });
}

/**
 *  This function add the event mouseup to
 *  a Konva Object. 
 * 
 *  This event makes sure that the predecessor
 *  or successor (usually a comductor) follows
 *  the component that moved
 * 
 * @param {JSON Object - Konva Object} component it usually represent a node - Transformer - Client
 */
function onMouseUpComponentEvent(component) {
    component.addEventListener("mouseup", function(event) {
        stage.draggable(true); // You can now navigate in the canva
        component.parent.draggable(false); // You cannot move the component anymore -> You will on mousedown event
        var firstLeveRelationShip = componentListManager.getComponentFirstLevelRelationship(component.attrs.id);
        console.log(firstLeveRelationShip);

        firstLeveRelationShip.forEach((value) => {
            if (value.predecesseur === component.attrs.id) {
                onElementPredecessorFollowUp(stage, value, zoomLevel, componentListManager, currentLayerPositionX, currentLayerPositionY,
                    (followingComponent) => {
                        followingComponent[0].getLayer().draw();
                    }
                );
            } else if (value.successeur === component.attrs.id) {
                onElementSuccessorFollowUp(stage, value, zoomLevel, componentListManager, currentLayerPositionX, currentLayerPositionY,
                    (followingComponent) => {
                        followingComponent[0].getLayer().draw();
                    }
                );
            }
        });
    });
}

/**
 *  This function add all the event required
 *  by a node
 * 
 *  click : Show Specification or add a conductor
 *  
 * @requires onMouseDownComponentEvent Allow the component to be moved instead of moving the canvas
 * @requires onMouseUpComponentEvent  Make sure the conductors follow the movement of the node
 * @requires hideAllSpecs Takes care of hiding the specification tab
 * @requires handleNodeSpecificationsTab Show the specification of the node ( Not much in this case )
 * @requires setSelectionNode Set Node as one of the selected component
 * @param {JSON Object - Konva Object} nodeGroup This is a Konva.Group - This is a populated group with a node
 */
function onClickNodeEvent(nodeGroup) {
    nodeGroup.addEventListener("click", function(event) {
        var node = extractNodeObjectFromNodeGroup(this);
        if (createLine == true) {
            isLineOnElement = true;
            setSelectionNode(node);
            message.innerHTML = "Noeud sélectionner";
        } else {
            // specificationConductorModal.style.display = "block";
            // document.getElementById("conductor-name").innerHTML = this.attrs.id;
            hideAllSpecs();
            handleNodeSpecificationsTab(this);
            ChangeImageHandler.selectComponent(this.children[0], true);
            nodeSpecs.style.display = "block";
            elementName.innerHTML = "Conducteur : " + node.attrs.id;
            // TODO: Set value to input type hidden
        }
    });
    var node = extractNodeObjectFromNodeGroup(nodeGroup);
    onMouseDownComponentEvent(node);
    onMouseUpComponentEvent(node);
}

/**
 *  This function add all the event required
 *  by a conductor
 * 
 *  click : Show Specification or add a conductor ( Split in half)
 *  
 * @requires onMouseDownComponentEvent Allow the component to be moved instead of moving the canvas
 * @requires onMouseUpComponentEvent  Make sure the conductors follow the movement of the node
 * @requires hideAllSpecs Takes care of hiding the specification tab
 * @requires handleConductorSpecificationsTab Show the specification of the node ( Not much in this case )
 * @requires setSelectionNode Set conductor as one of the selected component
 * @requires handleCondutorSplitting On creating a new line, this will split the original conductor in 2 ** For now it is not functionnal 10/05/2018**
 * @param {JSON Object - Konva object} conductor 
 */
function onClickConductorEvent(conductor) {
    conductor.addEventListener("click", function(event) {
        if (createLine == true) {
            isLineOnElement = true;
            message.innerHTML = "Conducteur sélectionner";
            setSelectionNode(this);
            //handleConductorSplitting(this);
        } else {
            // specificationConductorModal.style.display = "block";
            // document.getElementById("conductor-name").innerHTML = this.attrs.id;
            hideAllSpecs();
            conductorSpecs.style.display = "block";
            elementName.innerHTML = "Conducteur : " + this.attrs.id;
            // TODO: Set value to input type hidden
            handleConductorSpecificationTab(this);
            ChangeImageHandler.selectComponent(this, true);
            componentListManager.updateComponentImage(this);
        }
    });
}

/**
 *  This function add all the event required
 *  by a conductor
 * 
 *  click : Show Specification or add a conductor ( Split in half)
 *  
 * @requires onMouseDownComponentEvent Allow the component to be moved instead of moving the canvas
 * @requires onMouseUpComponentEvent  Make sure the conductors follow the movement of the node
 * @requires hideAllSpecs Takes care of hiding the specification tab
 * @requires handleTransformerSpecificationsTab Show the specification of the node ( Not much in this case )
 * @requires setSelectionNode Set conductor as one of the selected component
 * @param {JSON Object - Konva Object} transfo 
 */
function onClickTranformerEvent(transfo) {
    transfo.addEventListener("click", function(event) {
        if (createLine == true) {
            isLineOnElement = true;
            message.innerHTML = "Transformateur sélectionner";
            setSelectionNode(this);
        } else {
            // specificationTransformatorModal.style.display = "block";
            // document.getElementById("transfo-name").innerHTML = this.attrs.id;
            hideAllSpecs();
            transformerSpecs.style.display = "block";
            // showSelectedElement(this);
            elementName.innerHTML = "Tranformateur : " + this.attrs.id; // Writes Transformateur + its id to spec tab
            // TODO: Set value to input type hidden
            handleTransformerSpecificationTab(this)
            ChangeImageHandler.selectComponent(this, true);
            componentListManager.updateComponentImage(this);
        }
    });
    onMouseDownComponentEvent(transfo);
    onMouseUpComponentEvent(transfo);
}

/**
 *  This function add all the event required
 *  by a transformer
 * 
 *  click : Show Specification or add a conductor ( Split in half)
 *  
 * @requires onMouseDownComponentEvent Allow the component to be moved instead of moving the canvas
 * @requires onMouseUpComponentEvent  Make sure the conductors follow the movement of the node
 * @requires hideAllSpecs Takes care of hiding the specification tab
 * @requires handleLodgingSpecificationsTab Show the specification of the  ( Not much in this case )
 * @requires setSelectionNode Set conductor as one of the selected component
 * @param {JSON Object - Konva Object} client 
 */
function onClickClientEvent(client) {
    client.addEventListener("click", function(event) {
        if (createLine == true) {
            isLineOnElement = true;
            message.innerHTML = "Client sélectionner";
            setSelectionNode(this);
        } else {
            // specificationClientModal.style.display = "block";
            // document.getElementById("client-name").innerHTML = this.attrs.id;
            hideAllSpecs();
            clientSpecs.style.display = "block";
            elementName.innerHTML = "Client : " + this.attrs.id;
            // TODO: Set value to input type hidden
            handleLodgingSpecificationTab(this);
            ChangeImageHandler.selectComponent(this, true)
            componentListManager.updateComponentImage(this);
        }
    });

    onMouseDownComponentEvent(client);
    onMouseUpComponentEvent(client, stage);

}


/* Not implemented */
function handlePointerConstraint() {
    if (currentLayerPositionX >= maxWidth) {
        currentLayerPositionX = maxWidth;
    } else if (currentLayerPositionX <= (-(maxWidth))) {
        currentLayerPositionX = (-(maxWidth));
    }

    if (currentLayerPositionY >= maxHeight) {
        currentLayerPositionY = maxHeight;
    } else if (currentLayerPositionY <= (-(maxHeight))) {
        currentLayerPositionY = (-(maxHeight));
    }
}

/* ******************************************** */

function setPositionInfoToZero() {
    currentPosition.x = 0;
    currentPosition.y = 0;

    positionInfo.innerHTML = JSON.stringify(currentPosition);
}

// Not currently in use
function calculateDifference(value) {
    var scaledValue = value / zoomLevel;
    var diff = value - scaledValue;
    return diff;
}

/* Doesn't seem to be in use */
function boundPosition(pos, maxPosition) {
    var position;
    maxPosition += calculateDifference(maxPosition);

    if (pos >= 0) {
        position = pos >= maxPosition ? maxPosition : pos;
    } else {
        position = pos <= (-(maxPosition)) ? (-(maxPosition)) : pos;
    }
    return position;
}

/**
 *  Hide the specs menu on the side
 * 
 *  Uses the DOM to do so.
 */
function hideAllSpecs() {
    transformerSpecs.style.display = "none";
    clientSpecs.style.display = "none";
    conductorSpecs.style.display = "none";
    nodeSpecs.style.display = "none";
}


// Function to set Move Tool as active (toolbar or context menu (soon))
// function selectMoveTool(){
//     resetSelectorState();
//     moveTool = true;
//     resetButtonSelected();
//     selectButton(moveButton);
// }

/**
 *  Keep track of the component that were selected
 *  Used in the case that you want to connect a client 
 *  to a transformer
 * 
 * @param {JSON Object} self instance of a clicked object - i.e a transformer or a client 
 */
function setSelectionNode(self) {
    if (firstSelectedNode == null) { // First Node wasn't selected
        firstSelectedNode = self; // Assign the first node clicked on ( creating conductor mode )
    } else if (secondSelectedNode == null) { // Second Node wasn't selected
        secondSelectedNode = self; // Assign the second node clicked on ( creating conductor mode )
    }
}

/**
 *  This function does what it says, which is
 *  addind a new element. The element in this
 *  case is a conductor. It requires a lot more
 *  data than a usual element since it has a predecessor,
 *  a successor, a tip position, a first coordinates ( origin coordinates )
 *  
 * @param {JSON Object - Konva Object} conductorElement 
 * @param {JSON Object} tipConductorPosition 
 * @param {JSON Object} firstCoordinates 
 */
function addNewElement(conductorElement, tipConductorPosition, firstCoordinates) {
    if (firstSelectedNode != null && secondSelectedNode != null) {
        // Temporary tipConductorPosition and firstCoordinates
        componentListManager.appendNewComponents(conductorElement, componentType.conducteur, firstSelectedNode, secondSelectedNode, tipConductorPosition, firstCoordinates);

        firstSelectedNode = null; // Make it ready for another component
        secondSelectedNode = null; // Make it ready for another component
    }
}


/** 
    TODO: Remove this function and replace it with the actual function used in it

    Method that will take the a selected component and retrieve
    a component in the component list buffer and return it to
    the function that called it in the first place

    @requires componentListMananager
    @param selectedComponent
    @return  {ARRAY of size 1} -> Component selected with saved informations
*/
function filtercomponentListWithSelectedComponent(selectedComponent) {
    return componentListManager.fetchComponent(selectedComponent.attrs.id.replace('_Group', ''));
}

/** 
    Function which takes care of fetching the details
    on the transformer into the specification tab
    
    @param {JSON Object - Konva object}
*/
function handleTransformerSpecificationTab(transfo) {

    var transformer_object = filtercomponentListWithSelectedComponent(transfo);

    // TODO: if not found in buffer Query server to see if componenet exist

    $("#transformerTypeList").val(transformer_object.type_de_transformateur == "" ? "none" : transformer_object.type_de_transformateur);
    $("#transformer_alias").val(transformer_object.noeud_alias);

    if (transformer_object.type_de_transformateur != "") {
        displayTransformerSpecificationDetails(transformer_object, function(transformer) {
            // Do nothing
        });
    } else {
        $("#transformer_description").val("");
        $("#transformer_capacity").val("");
        $("#transformer_resistance").val("");
        $("#transformer_reactance").val("");
        $("#transformer_no_load_loss").val("");
        $("#transformer_overhead").prop("checked", "false");
    }

    $('#transformerTypeList').change(function(event) {
        displayTransformerSpecificationDetails(transformer_object, function(transformer_object) {
            let list = componentListManager.getComponentList();
            for (let i = 0; i < list.length; i++) {
                if (transformer_object.nom_du_noeud == list[i].nom_du_noeud) {
                    list[i] = transformer_object;
                }
            }
            componentListManager.setComponentList(list);
        });
    });
}

/**
 *  This function takes care of showing 
 *  the details of a node in the specification
 *  tab
 * 
 * @event onclick {onClickNodeEvent}
 * @param { JSON Object - Konva Object } node this usually a instance inside of the click event
 */
function handleNodeSpecificationsTab(node) {
    var nodeObject = filtercomponentListWithSelectedComponent(node);
    $("#node_alias").val(nodeObject.noeud_alias);
}

/**
 *  Function which takes care of fetching the details
 *  on the conductor into the specification tab
 * 
 * @event onclick {onClickConductorEvent}
 * @param {JSON Object - Konva Object} conductor this usually a instance inside of the click event 
 */
function handleConductorSpecificationTab(conductor) {
    // Might have to simply pass this object as argument instead of the array
    var conductor_object = filtercomponentListWithSelectedComponent(conductor);
    // TODO: if not found in buffer Query server to see if componenet exist
    $("#conductorTypeList").val(conductor_object.type_de_conducteur == "" ? "none" : conductor_object.type_de_conducteur);
    $("#conductor_length").val(conductor_object.longueur);
    // BUG unable to save alias to the componentList, so unable to show the data - ** Might be a browserify or bable bug **
    // $("#conductor_alias").val(conductor_object.noeud_alias);

    if (conductor_object.type_de_conducteur != "") {
        displayConductorSpecificationDetails(conductor_object, function(conductor) {
            // Do nothing
        });
    } else {
        $("#conductor_description").val("");
        $("#conductor_overhead").prop("checked", false);
        $("#conductor_resistance_per_km").val("");
        $("#conductor_resistance_variation_by_celcius").val("");
        $("#conductor_resistance_per_km_with_temperature").val("");
        $("#conductor_admissible_current").val("");
        $("#conductor_variation_temp_depending_current").val("");
        $("#conductor_variation_resistance_depending_current").val("");
        $("#conductor_reactance").val("");
        $("#conductor_winter_recovery").val("");
        $("#conductor_summer_schelude").val("");
        $("#conductor_client_pole").val("");
    }

    //This takes care of updating data in the componentList array
    $("#conductorTypeList").change(function(event) {
        displayConductorSpecificationDetails(conductor_object, function(conductor_object) {
            let list = componentListManager.getComponentList();
            list.forEach((conductor, index, array) => {
                if (conductor_object.nom_du_noeud == conductor.nom_du_noeud) {
                    array[index] = conductor_object;
                }
            });
            componentListManager.setComponentList(list);
        });
    })
}

/**
 * Function which takes care of fetching the details
 * on the specification of a lodging into the specification tab
 * 
 * @event onclick {onClickClientEvent}
 * @param {JSON Object - Konva Object} lodging (Got carried away at first lodging == client) this usually a instance inside of the click event 
 */
function handleLodgingSpecificationTab(lodging) {
    var lodging_object = componentListManager.fetchComponent(lodging.attrs.id);

    $("#heatingTypeList").val(lodging_object.type_de_chauffage == "" ? "none" : lodging_object.type_de_chauffage);
    $("#lodgingTypeList").val(lodging_object.type_de_logement == "" ? "none" : lodging_object.type_de_logement);

    $("#habitable_area").val(lodging_object.surface_habitable);
    $("#number_of_floors").val(lodging_object.nombre_etage);
    $("#number_of_lodgings").val(lodging_object.nombre_de_logement);
    $("#client_alias").val(lodging_object.noeud_alias);

    if (lodging_object.type_de_chauffage != "") {
        displayHeatingSpecificationDetails(lodging_object, function(heating) {
            // Do nothing
        });
    } else {
        $("#heating_description").val("");
    }

    if (lodging_object.type_de_logement != "") {
        displayLodgingSpecificationDetails(lodging_object, function(lodging) {
            // Do nothing
        });
    } else {
        $("#lodging_description").val("");
    }

    //This takes care of updating data in the componentList array
    $("#lodgingTypeList").change(function(event) {
        displayLodgingSpecificationDetails(lodging_object, function(lodging_object) {
            let list = componentListManager.getComponentList();
            list.forEach((value, index, array) => {
                if (value.nom_du_noeud == lodging_object.nom_du_noeud) {
                    array[index] = lodging_object;
                }
            });
            componentListManager.setComponentList(list);
        });
    });

    //This takes care of updating data in the componentList array
    $("#heatingTypeList").change(function(event) {
        // TODO: Display changes
        displayHeatingSpecificationDetails(lodging_object, function(lodging_object) {
            let list = componentListManager.getComponentList();
            for (let i = 0; i < list.length; i++) {
                if (list[i].nom_du_noeud == lodging_object.nom_du_noeud) {
                    list[i] = lodging_object;
                }
            }
            componentListManager.setComponentList(list);
        })
    });
}

/**
 *  This function takes care of 
 *  splitting a conductor and 
 *  create a node in the middle of the split.
 *  At the same time, we end up with having 2 
 *  conductor with their own successor and predecessor
 * @author It doesn't work in the current state, so the function commented out of the click event of a conductor
 * @event onclick {onClickConductorEvent}
 * @param {JSON Object - Konva Object} self conductor instance from the click event
 */
function handleConductorSplitting(self) {
    var pos = stage.getPointerPosition();

    let conductorGroup = stage.find("#" + self.attrs.id + "_Group");
    conductorGroup.destroy();
    let conductorPoints = self.attrs.points;
    let verticalHeight = conductorPoints[7];
    let horizontalWidth = conductorPoints[6];

    var conductorObject = componentListManager.getComponentList().filter(function(object) {
        if (self.attrs.id == object.nom_du_noeud) {
            return object;
        }
    });

    var predecessorObject = componentListManager.getComponentList().filter(function(object) {
        if (conductorObject[0].predecesseur == object.nom_du_noeud) {
            return object;
        }
    });

    var successorObject = componentListManager.getComponentList().filter(function(object) {
        if (conductorObject[0].successeur == object.nom_du_noeud) {
            return object;
        }
    });

    var verticalUpperLine = ((pos.y - conductorObject[0].firstCoordinates.y) / zoomLevel) * 0.9;
    var horizontalUpperLine = ((pos.x - conductorObject[0].firstCoordinates.x) / zoomLevel) * 0.9;

    var verticalLowerLine = ((pos.y - conductorObject[0].tipConductorPosition.y) / zoomLevel) * 0.9;
    var horizontalLowerLine = ((pos.x - conductorObject[0].tipConductorPosition.x) / zoomLevel) * 0.9;

    var upperLine = getNewLine(0, 0, horizontalUpperLine, verticalUpperLine, defaultValues.defaultGreen,
        defaultValues.generateConductorIdString(true));

    var upperLineGroup = getNewGroup(((conductorObject[0].position_x / zoomLevel) + currentLayerPositionX),
        ((conductorObject[0].position_y / zoomLevel) + currentLayerPositionY),
        defaultValues.generateGroupIdString(defaultValues.generateConductorIdString(false)));

    var node = getNewNode(0, 0, defaultValues.defaultRadius,
        defaultValues.defaultStrokeWidth, defaultValues.defaultFill, defaultValues.defaultBlack,
        defaultValues.generateNodeIdString());

    var nodeText = getNewText(-20, -15, defaultValues.generateNodeIdString(false), defaultValues.generateNodeText());
    var nodeGroup = getNewGroup(pos.x, pos.y, defaultValues.generateNodeIdString(false));

    var lowerLine = getNewLine(0, 0, horizontalLowerLine, verticalLowerLine, defaultValues.defaultBlue,
        defaultValues.generateConductorIdString(true));

    var lowerLineGroup = getNewGroup(((nodeGroup.attrs.x / zoomLevel) + currentLayerPositionX),
        ((nodeGroup.attrs.y / zoomLevel) + currentLayerPositionY),
        defaultValues.generateGroupIdString(defaultValues.generateConductorIdString(false)));

    $("#" + self.attrs.id).unbind("click");
    stage.find("#" + self.attrs.id).destroy();
    let originalConductor = componentListManager.fetchComponent(self.attrs.id);

    nodeGroup.add(node);
    nodeGroup.add(nodeText);
    lowerLineGroup.add(lowerLine);
    upperLineGroup.add(upperLine);


    // conductorGroup[0].add(lowerLineGroup);
    // conductorGroup[0].add(nodeGroup);
    layer.add(upperLineGroup);
    layer.add(lowerLineGroup);
    layer.add(nodeGroup);
    layer.draw();



    var originalConductorPred = componentListManager.getPredecesseur(conductorObject[0]);
    var originalConductorSucc = componentListManager.getSuccesseur(conductorObject[0]);


    let nodePosition = {
        attrs: {
            x: nodeGroup.attrs.x,
            y: nodeGroup.attrs.y
        }
    };
    let predecessorPosition = {
        attrs: {
            x: originalConductorPred[0].position_x,
            y: originalConductorPred[0].position_y
        }
    };
    let successorPosition = {
        attrs: {
            x: originalConductorSucc[0].position_x,
            y: originalConductorSucc[0].position_y
        }
    };


    componentListManager.appendNewComponents(node, componentType.noeud);
    componentListManager.appendNewComponents(upperLine, componentType.conducteur, originalConductorPred[0], nodeGroup, predecessorPosition, nodePosition);
    componentListManager.appendNewComponents(lowerLine, componentType.conducteur, nodeGroup, originalConductorSucc[0], successorPosition, nodePosition);

    componentListManager.removeComponent(conductorObject[0]);
    //componentListManager.updateComponentPredecesseur(lowerLine.attrs.id, originalConductorSucc[0].nom_du_noeud);
    //originalConductorPred[0].nom_du_noeud);

    if (firstSelectedNode.attrs.id == conductorObject[0].nom_du_noeud) {
        firstSelectedNode = node;
    } else {
        secondSelectedNode = node;
    }

    onClickConductorEvent(upperLine);
    onClickConductorEvent(lowerLine);
}

/**
 *  This function generate a new node 
 * @event on click KonvaJS Content - Can be found in the last lines of the page
 */
function generateNode() {
    var node = getNewNode(0, 0, defaultValues.defaultRadius,
        defaultValues.defaultStrokeWidth, defaultValues.defaultFill,
        defaultValues.defaultBlack, defaultValues.generateNodeIdString());

    var idNodeText = getNewText(-15, -15, defaultValues.generateNodeIdString(false),
        defaultValues.generateNodeText());
    var pos = stage.getPointerPosition();

    var nodeGroup = new Konva.Group({
        x: ((pos.x + currentLayerPositionX) / zoomLevel),
        y: ((pos.y + currentLayerPositionY) / zoomLevel),
        id: node.attrs.id + "_Group",
    });

    nodeGroup.add(node);
    nodeGroup.add(idNodeText);

    componentListManager.appendNewComponents(node, componentType.noeud);

    setSelectionNode(node);
    onClickNodeEvent(nodeGroup);

    layer.add(nodeGroup);
    stage.add(layer);
}

/**
 *  This function takes care of 
 *  generating 
 *  
 * @event containerDOM on click
 * @param {Click event} event
 */
function generateTranformer(event) {
    var transfoImage = new Image();
    var pos = stage.getPointerPosition();

    transfoImage.onload = function() {
        var transfo = getNewImage(50, 0,
            defaultValues.defaultTransfoWidth, defaultValues.defaultTransfoHeight,
            transfoImage, defaultValues.generateTransformerIdString());

        var idText = getNewText(0, 0, defaultValues.generateTransformerIdString(false),
            defaultValues.generateTransformerText());

        var transfoGroup = new Konva.Group({
            x: event == undefined ? (containerDOM.clientWidth / 2) : ((pos.x + currentLayerPositionX) / zoomLevel) - (this.width / 2.5),
            y: event == undefined ? containerDOM.clientHeight * 0.15 : ((pos.y + currentLayerPositionY) / zoomLevel) - (this.height / 4),
        });


        transfoGroup.add(transfo);
        transfoGroup.add(idText);

        componentListManager.appendNewComponents(transfo, componentType.tranformateur);

        layer.add(transfoGroup);

        stage.add(layer);

        onClickTranformerEvent(transfo);
    };
    transfoImage.src = "/static/img/transformateur.svg";
}

// function to create a client  on the canvas
function generateClient(event) {
    var clientImage = new Image();
    var pos = stage.getPointerPosition();

    clientImage.onload = function() {
        var client = getNewImage(50, 0, 100, 150, clientImage,
            defaultValues.generateClientIdString());

        var idText = getNewText(0, 0, defaultValues.generateClientIdString(false),
            defaultValues.generateClientText());

        let x = event == undefined ? (containerDOM.clientWidth / 2) : ((pos.x / zoomLevel) + currentLayerPositionX) - (this.width / 3);
        let y = event == undefined ? containerDOM.clientHeight * 0.15 : ((pos.y / zoomLevel) + currentLayerPositionY) - (this.height / 4);
        var clientGroup = getNewGroup(x, y, defaultValues.generateGroupIdString(defaultValues.generateClientIdString(false)));

        console.log(clientGroup);

        console.log({
            PositionX: currentLayerPositionX,
            PositionY: currentLayerPositionY,
        });


        clientGroup.add(client);
        clientGroup.add(idText);

        layer.add(clientGroup);

        stage.add(layer);

        componentListManager.appendNewComponents(client, componentType.logement);
        // where new client can be controlled
        onClickClientEvent(client);
    };

    clientImage.src = "/static/img/house.svg";
}

// Function to create a conductor on the canvas
function generateConductor() {
    var pos = stage.getPointerPosition();
    if (isLineOnElement == true) { // make sure an element is selected
        if (lineFirstPoint == true) { // make sure this is the first time something is selected
            firstCoordinates = pos; // Getting the first coordinates so I can create line later
            lineFirstPoint = false; // Once this will be over, we'll be ready for the next node

            // Executed if second point when Selecting a transfo or client then a the conductor
            if (firstSelectedNode == null) { // No node selected ?
                setSelectionNode(pos); // Let's assign our first node
            }
        } else {
            console.log(secondSelectedNode);
            var verticalHeight = ((pos.y - (firstCoordinates.y)) / zoomLevel) * 0.9;
            var horizontalWidth = ((pos.x - (firstCoordinates.x)) / zoomLevel) * 0.9;
            var line = getNewLine(0, 0, horizontalWidth, verticalHeight, defaultValues.defaultGrey,
                defaultValues.generateConductorIdString());

            var conductorGroup = getNewGroup(((firstCoordinates.x / zoomLevel) + currentLayerPositionX),
                ((firstCoordinates.y / zoomLevel) + currentLayerPositionY),
                defaultValues.generateGroupIdString(defaultValues.generateConductorIdString(false)));

            conductorGroup.add(line);

            layer.add(conductorGroup);

            stage.add(layer);

            lineFirstPoint = true;
            message.innerHTML = "Lien complété";

            // Where new conductor can be controlled
            onClickConductorEvent(line);

            addNewElement(line, pos, firstCoordinates);

            conductorGroup.moveToBottom();
            layer.draw();
        }
        isLineOnElement = false;
    }
}

function loadSave() {
    componentListManager.setComponentList($('#data').val() == "None" ? [] : jQuery.parseJSON($("#data").val().replace(/'/g, "\"")));
    return $("#visual").val();
}

function drawImageBack(nom_du_noeud, image) {
    var node = stage.find("#" + nom_du_noeud);
    var newImage = new Image()
    newImage.onload = function(event) {
        node.image(newImage);
        node.getLayer().draw();
    }
    newImage.src = image;
}

function completeLoading() {
    let list = componentListManager.getComponentList()
    for (let i = 0; i < list.length; i++) {
        let nomNoeud = list[i].nom_du_noeud;
        if (nomNoeud.includes('C') || nomNoeud.includes('T')) {
            setTimeout(function() {
                drawImageBack(nomNoeud, list[i].image);
            }, 1000);
        }

        if (nomNoeud.includes('C')) {
            var client = stage.find("#" + nomNoeud);
            onClickClientEvent(client[0]);
            defaultValues.setClientId(nomNoeud.replace('C', ''));
        } else if (nomNoeud.includes('T')) {
            var transfo = stage.find("#" + nomNoeud);
            onClickTranformerEvent(transfo[0]);
            defaultValues.setTransformerId(nomNoeud.replace('T', ''));
        } else if (nomNoeud.includes('A')) {
            var conducteur = stage.find("#" + nomNoeud);
            onClickConductorEvent(conducteur[0]);
            defaultValues.setConductorId(nomNoeud.replace("A", ''));
        } else if (nomNoeud.includes('N')) {
            var noeud = stage.find('#' + nomNoeud + "_Group");
            onClickNodeEvent(noeud[0]);
            defaultValues.setNodeId(nomNoeud.replace("N", ''));
        }
    }
}

// Used to be window.load = function(){}
function initCanvaJS() {
    setPositionInfoToZero();

    var width = (window.innerWidth) - (specificationPane.clientWidth + toolboxPane.clientWidth + 90);
    var height = (window.innerHeight - navigation.clientHeight);

    var loadedValues = loadSave();
    if (loadedValues == "None") {
        stage = new Konva.Stage({
            container: "container",
            width: width,
            height: height,
            draggable: true,
        });
        generateTranformer();
    } else {
        stage = Konva.Node.create(loadedValues, "container");
        completeLoading();
    }


    containerDOM.addEventListener("click", function(event) {
        var isDraggable = document.getElementById("drag");
        var isCreating = document.getElementById("create");

        if (createLine == true) {
            generateConductor(event);
        } else if (createTransfo == true) {
            generateTranformer(event);
        } else if (createClient == true) {
            generateClient(event);
        }
    });


    window.addEventListener("contextmenu", function(event) {
        var left = event.x;
        var top = event.y;

        menuBox = window.document.querySelector(".menu");
        menuBox.style.left = left + "px";
        menuBox.style.top = top + "px";
        menuBox.style.display = "block";

        event.preventDefault();

        menuDisplayed = true;
    }, false);

    window.addEventListener("click", function() {
        if (menuDisplayed == true) {
            menuBox.style.display = "none";
        }
    });

    // Zoom in button
    zoomInButton.addEventListener("click", function() {
        if (zoomLevel == 1) {
            originalLayerPositionX = currentLayerPositionX;
            originalLayerPositionY = currentLayerPositionY;
        }

        if (zoomLevel <= zoomInLimit) {
            zoomLevel += zoomStep;

            stage.scale({
                x: zoomLevel,
                y: zoomLevel,
            });


            currentLayerPositionX = originalLayerPositionX / zoomLevel;
            currentLayerPositionY = originalLayerPositionY / zoomLevel;

            // Debug position code
            // var node = new Konva.Circle({
            //     x : currentLayerPositionX,
            //     y : currentLayerPositionY,
            //     radius : 30,
            //     fill : 'red',
            //     stroke: 'black',
            //     strokeWidth : 2,
            //     id : "N" + nodeIdNumber
            // });

            // layer.add(node);
            // layer.draw();

            var status = parseInt(zoomLevel * 100); // Make sure that status is an integer

            zoomStatus.innerHTML = status + "%";
        }

        if (zoomLevel == 1) {
            currentLayerPositionX = originalLayerPositionX;
            currentLayerPositionY = originalLayerPositionY;
        }
        //
        stage.draw();
    });

    // Deal with the events when clicking the zoom in button
    zoomOutButton.addEventListener("click", function() {
        if (zoomLevel == 1) {
            originalLayerPositionX = currentLayerPositionX;
            originalLayerPositionY = currentLayerPositionY;
        }

        if (zoomLevel > zoomStep) {
            zoomLevel -= zoomStep;
            stage.scale({
                x: zoomLevel,
                y: zoomLevel,
            });

            currentLayerPositionX = (originalLayerPositionX / zoomLevel);
            currentLayerPositionY = (originalLayerPositionY / zoomLevel);

            // Debug Position Code
            // console.log({X : currentLayerPositionX, Y : currentLayerPositionY});
            // var node = new Konva.Circle({
            //     x : currentLayerPositionX,
            //     y : currentLayerPositionY,
            //     radius : 30,
            //     fill : 'red',
            //     stroke: 'black',
            //     strokeWidth : 2,
            //     id : "N" + nodeIdNumber
            // });

            // layer.add(node);
            // layer.draw();


            var status = parseInt(zoomLevel * 100); // Make sure that status is an integer

            zoomStatus.innerHTML = status + "%";
        }

        if (zoomLevel == 1) {
            currentLayerPositionX = originalLayerPositionX;
            currentLayerPositionY = originalLayerPositionY;
        }

        stage.draw();
    });

    var conductorContextMenu = document.getElementById("conductor"); // Button when right click (conductor)
    var transfoContextMenu = document.getElementById("transfo"); // Button when right click (transfo)
    var clientContextMenu = document.getElementById("client"); // Buttonwhen right click (client)

    conductorContextMenu.addEventListener("click", function() {
        if (menuDisplayed == true) {
            selectConductor();
        }
    });

    // transfoContextMenu.addEventListener("click", function(){
    //     if(menuDisplayed == true){
    //         selectTranformer();
    //     }
    // });

    clientContextMenu.addEventListener("click", function() {
        if (menuDisplayed == true) {
            selectClient();
        }
    });

    // transformerButton.addEventListener("click", function(){
    //     selectTranformer();
    // });

    clientButton.addEventListener("click", function() {
        selectClient();
    })

    conductorButton.addEventListener("click", function() {
        selectConductor();
    });

    selectionButton.addEventListener("click", function() {
        selectSelectTool();
    });

    stage.addEventListener("dragstart", function() {
        layerStartDrag = stage.getPointerPosition();
    });

    stage.addEventListener("dragmove", function() {
        // var pos = stage.getPointerPosition();
        // currentPosition.x += ( - (pos.x - layerStartDrag.x) );
        // currentPosition.y += ( - (pos.y - layerStartDrag.y) );
        // positionInfo.innerHTML = JSON.stringify(currentPosition);
    });

    stage.addEventListener("dragend", function() {
        if (elementMoved == false) {
            var layerEndDrag = stage.getPointerPosition();

            var distanceX = (layerEndDrag.x - layerStartDrag.x);
            var distanceY = (layerEndDrag.y - layerStartDrag.y);

            currentLayerPositionX += (-distanceX) / zoomLevel; // brings you position of current origin
            currentLayerPositionY += (-distanceY) / zoomLevel; // brings you position of current origin

            if (zoomLevel != 1) {
                originalLayerPositionX += (-distanceX);
                originalLayerPositionY += (-distanceY);
            }
            currentPosition.x = currentLayerPositionX;
            currentPosition.y = currentLayerPositionY;
            positionInfo.innerHTML = JSON.stringify(currentPosition);
            // handlePointerConstraint();
        }
        elementMoved = false;
    });

    containerDOM.addEventListener("scroll", function(event) {
        event.preventDefault();

        console.log(event);
    });

    resetButton.addEventListener("click", function() {
        stage.x(0);
        stage.y(0);

        currentLayerPositionX = 0;
        currentLayerPositionY = 0;

        originalLayerPositionX = 0;
        originalLayerPositionY = 0;

        setPositionInfoToZero();

        stage.draw();
    });

    $('.konvajs-content').bind("click", function(event) {
        if (isLineOnElement == false && firstSelectedNode != null && createLine == true) {
            generateNode();
            isLineOnElement = true;
        }
    });

    // TODO: : Look for a way to make the canvas resize correctly
    function fitStageIntoParentContainer() {
        var parentContainer = document.querySelector("#stage-parent");

        var containerWidth = parentContainer.offsetWidth;

        var scale = containerWidth / width;

        var width = (window.clientWidth - toolboxPane.clientWidth) - specificationPane.clientWidth;
        var height = (window.clientHeight - navigation.clientHeight) - specificationPane.clientHeight;

        stage.width(width);
        stage.height(height);
        stage.draw();
    }

    // window.addEventListener("resize", fitStageIntoParentContainer);

    /*
          *****************************************************************

              Code that  the changes in type for all components

          *****************************************************************
      */

    addEventToForm(transformerSpecsForm, eventFormCallback);
    addEventToForm(nodeSpecsForm, eventFormCallback);
    addEventToForm(clientSpecsForm, eventFormCallback);

    /*
          @BUG: Unable to fetch componentListManager.on update
      */
    // addEventToForm(conductorSpecsForm, eventFormCallback)

    // TODO: Remove this from the interface -> It should be taken care when a user create
    // a study

    $('#save_network').on("click", function(event) {
        var saveValue = {
            "data": componentListManager.getComponentList(),
            "visual": stage.toJSON(),
        };
        var csrfToken = $('.voltageBox input[type="hidden"]').val();
        $.ajax({
            url: "save/" + $('#study_id').val(),
            type: "POST",
            data: JSON.stringify(saveValue),
            headers: {
                "X-CSRFToken": csrfToken,
                "Application-Type": "application/json",
            },
            success: function(response) {
                console.log(response);
                alert("Sauvegarde réussie");
            },
        })
    });

    /*
        Component caracteristic changes
      */
    $("#conductor_length").change(function(event) {
        var elementChanged = $("#elementName").html();
        elementChanged = elementChanged.replace("Conducteur :", "");
        elementChanged = elementChanged.trim();
        let list = componentListManager.getComponentList()
        for (let i = 0; i < list.length; i++) {
            if (list[i].nom_du_noeud == elementChanged) {
                list[i].longueur = parseInt(event.target.value);
            }
        }
        componentListManager.setComponentList(list);
    });

    function extractNodeFromHTML(htmlString) {
        htmlString = htmlString.replace("Client :", "");
        htmlString = htmlString.trim();
        return htmlString;
    }

    $("#habitable_area").change(function(event) {
        var elementChanged = extractNodeFromHTML($("#elementName").html());
        let list = componentListManager.getComponentList();
        list.forEach((value, index, array) => {
            if (value.nom_du_noeud == elementChanged) {
                array[index].surface_habitable = parseInt(event.target.value);
            }
        });
        componentListManager.setComponentList(list);
    });

    $("#number_of_floors").change(function(event) {
        var elementChanged = extractNodeFromHTML($("#elementName").html());
        let list = componentListManager.getComponentList();
        for (let i = 0; i < list.length; i++) {
            if (list[i].nom_du_noeud == elementChanged) {
                list[i].nombre_etage = parseInt(event.target.value);
            }
        }
        componentListManager.setComponentList(list);
    });

    $("#number_of_lodgings").change(function(event) {
        var elementChanged = extractNodeFromHTML($("#elementName").html());
        let list = componentListManager.getComponentList();
        for (let i = 0; i < list.length; i++) {
            if (list[i].nom_du_noeud == elementChanged) {
                list[i].nombre_de_logement = parseInt(event.target.value);
            }
        }
        componentListManager.setComponentList(list);
    });

    /*
        Computing handling part of the code
      */

    $("#calculate_network").click(function(event) {
        var csrf_token = $('.voltageBox input[type="hidden"]').val();
        var etude_id = $('.etude_id').text();
        console.log(etude_id);
        $.ajax({
            url: "get_compute_network/" + etude_id,
            type: "POST",
            data: JSON.stringify(componentListManager.getComponentList()),
            headers: {
                "X-CSRFToken": csrf_token,
                "Application-Type": "application/json",
            },
            success: function(computed_values) {
                var jsonData = JSON.parse(computed_values.data)
                const transfoDataTable = new DataTableHandler("#transformer_data");
                const conductorTableHandler = new DataTableHandler("#conductor_data");
                const clientTableHandler = new DataTableHandler("#client_data");
                const nodeTableHandler = new DataTableHandler("#node_data");
                console.log(jsonData);
                jsonData.forEach(function(data) {
                    switch (true) {
                        case data.model.includes("transformateur"):
                            transfoDataTable.addDataRow(data.fields);
                            break
                        case data.model.includes("conducteur"):
                            conductorTableHandler.addDataRow(data.fields);
                            break;
                        case data.model.includes("noeud"):
                            nodeTableHandler.addDataRow(data.fields);
                            break;
                        case data.model.includes("logement"):
                            clientTableHandler.addDataRow(data.fields);
                            break;
                    }
                })
            },
            error: function(error) {
                alert("Erreur - Vérifier que vous n'avez rien oublié");
            },
        })
    });
}


export {
    initCanvaJS,
    handleConductorSplitting,
    setSelectionNode,
    handleConductorSpecificationTab,
    hideAllSpecs,
    componentType,
    componentListManager
};