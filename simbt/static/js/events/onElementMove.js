var Konva = require('konva');

/**
 *  This function makes the require changes to make
 *  a conductor follow it successor when it is moved
 * 
 * @param {Konva Object} stage Object that represent the canva
 * @param {JSON Object} successeur Object from componentListManager
 * @param { Number } zoomLevel It is a global variable in canvas.js -> Keeps track of the zoomLevel
 * @param { ComponentListManager instance } componentListManager  Used to update data in the componentListModel
 * @param { function } callback It returns the updated successor using a callback 
 */
function onElementSuccessorFollowUp(stage, successeur, zoomLevel, componentListManager, currentLayerPositionX, currentLayerPositionY, callback) {
    let mousePosition = stage.getPointerPosition();
    var followingComponent = stage.find("#" + successeur.nom_du_noeud);
    let points = followingComponent[0].points();
    followingComponent[0].parent.x(mousePosition.x);
    followingComponent[0].parent.y(mousePosition.y);
    console.log(currentLayerPositionX);
    console.log(currentLayerPositionY);
    let verticalHeight = ((((successeur.tipConductorPosition.x - mousePosition.x) + currentLayerPositionX) / zoomLevel));
    let horizontalWidth = ((((successeur.tipConductorPosition.y - mousePosition.y) + currentLayerPositionY) / zoomLevel));

    points = [0, 0, 0, 0, verticalHeight, horizontalWidth];
    followingComponent[0].points(points);
    successeur.firstCoordinates = mousePosition;
    componentListManager.updateComponentData(successeur);
    callback(followingComponent);
}

/**
 *  This function makes the require changes to make
 *  a conductor follow it predecessor when it is moved
 * 
 * @param {Konva Object} stage Object that represent the canva
 * @param {JSON Object} predecesseur Object from componentListManager
 * @param { Number } zoomLevel It is a global variable in canvas.js -> Keeps track of the zoomLevel
 * @param { ComponentListManager instance } componentListManager  Used to update data in the componentListModel
 * @param { function } callback It returns the updated successor using a callback 
 */
function onElementPredecessorFollowUp(stage, predecesseur, zoomLevel, componentListManager, currentLayerPositionX, currentLayerPositionY, callback) {
    let mousePosition = stage.getPointerPosition();
    var followingComponent = stage.find("#" + predecesseur.nom_du_noeud);
    let points = followingComponent[0].points();
    let verticalHeight = (((mousePosition.x - predecesseur.firstCoordinates.x) + currentLayerPositionX) / zoomLevel) * 0.9;
    let horizontalWidth = (((mousePosition.y - predecesseur.firstCoordinates.y) + currentLayerPositionY) / zoomLevel) * 0.9;

    points = [0, 0, 0, 0, verticalHeight, horizontalWidth];
    followingComponent[0].points(points);
    predecesseur.tipConductorPosition = mousePosition;
    componentListManager.updateComponentData(predecesseur);
    callback(followingComponent);
}

/**
 *  Takes both successor and predecessor.
 *  Should be used on a node to make the conductor
 *  around it, follow up!
 * 
 * @param {Konva Object} stage Object that represent the canva
 * @param {JSON Object} successeur Object from componentListManager
 * @param {JSON Object} predecesseur Object from componentListManager
 * @param { Number } zoomLevel It is a global variable in canvas.js -> Keeps track of the zoomLevel
 * @param { ComponentListManager instance } componentListManager  Used to update data in the componentListModel
 */
function onElementPredecessorAndSuccessorFollowUp(stage, successeur, predecesseur, zoomLevel, componentListManager) {
    let mousePosition = stage.getPointerPosition();
    onElementPredecessorFollowUp(stage, predecesseur, zoomLevel, componentListManager, function(followingComponent) {
        followingComponent[0].getLayer().draw();
    });

    onElementSuccessorFollowUp(stage, successeur, zoomLevel, componentListManager, function(followingComponent) {
        followingComponent[0].getLayer().draw();
    });
}

export {
    onElementPredecessorFollowUp,
    onElementSuccessorFollowUp,
    onElementPredecessorAndSuccessorFollowUp
};