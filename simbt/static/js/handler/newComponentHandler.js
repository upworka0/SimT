var $ = require('jQuery');


function extractComponentTypeFromNodeName(nodeName) {
    /*
      Transformer -> 0
      Client -> 1
      Arc (conductor) -> 2
      Node (Noeud) -> 3
    */
    if (nodeName.includes('T')) {
        return 0;
    } else if (nodeName.includes('C')) {
        return 1
    } else if (nodeName.includes("A")) {
        return 2;
    } else if (nodeName.includes('N')) {
        return 3;
    }

}
/*
  0 -> Tranformateur
  1 -> Logement
  2 -> Conducteur
  3 -> Node
*/
function handleNewComponent(newComponent, predecessor) {
    /*
      Function that adds any of the components
      into the componentListBuffer
    */
    var component = {}
    var componentType = extractComponentTypeFromNodeName(newComponent.attrs.id) // Change newComponent attr ID

    switch (true) {
        case componentType == 0: // Transformateur
            component = {
                nom_du_noeud: newComponent.attrs.id,
                successeur: "None",
                predecesseur: predecessor == undefined ? "None" : predecessor.attrs.id,
                type_de_transformateur: "",
                position_x: 0, //newComponent.parent.attrs.x == undefined ? 0 : newComponent.parent.attrs.x,
                position_y: 0 //newComponent.parent.attrs.y == undefined ? 0 : newComponent.parent.attrs.y
            };
            break;
        case componentType == 1: // Logement
            component = {
                nom_du_noeud: newComponent.attrs.id,
                successeur: "None",
                predecesseur: predecessor == undefined ? "None" : predecessor.attrs.id,
                type_de_logement: "",
                type_de_chauffage: "",
                logement_code_saison: "",
                surface_habitable: "",
                nombre_etage: 1,
                nombre_de_logement: "",
                position_x: 0, //newComponent.parent.attrs.x == undefined ? 0 : newComponent.parent.attrs.x,
                position_y: 0 //newComponent.parent.attrs.y == undefined ? 0 : newComponent.parent.attrs.y
            };
            break;
        case componentType == 2: // Conducteur
            component = {
                nom_du_noeud: newComponent.attrs.id,
                successeur: "None",
                predecesseur: predecessor == undefined ? "None" : predecessor.attrs.id,
                type_de_conducteur: "",
                longueur: 0,
                position_x: 0, //newComponent.parent.attrs.x == undefined ? 0 : newComponent.parent.attrs.x,
                position_y: 0 //newComponent.parent.attrs.y == undefined ? 0 : newComponent.parent.attrs.y
            };
            break;
        case componentType == 3: // Node
            component = {
                nom_du_noeud: newComponent.attrs.id,
                successeur: "None",
                predecesseur: predecessor == undefined ? "None" : predecessor.attrs.id,
                position_x: 0, //newComponent.parent.attrs.x == undefined ? 0 : newComponent.parent.attrs.x,
                position_y: 0 //newComponent.parent.attrs.y == undefined ? 0 : newComponent.parent.attrs.y
            };
        default:
            //TODO Houston we have a problem!
            break;
    }

    return component
}

function addFollower(componentList) {
    var component = "";
    for (let i = 0; i < componentList.length; i++) {
        var component = componentList.filter(function(component) {
            if (component.predecesseur == componentList[i].nom_du_noeud) {
                return component;
            }
        });
        componentList[i].successeur = component[0] == undefined ? "None" : component[0].nom_du_noeud;
    }
    return componentList;
}

export {
    extractComponentTypeFromNodeName,
    handleNewComponent,
    addFollower
};