import ComponentsDetails from "./ComponentsDetails";
import TableHandler from "./handler/tableHandler";
import ComponentFactory from "./model/component";
import changeTypeByVoltage from "./events/voltageSelectedEvent";
import {
    handleNewComponent,
    addFollower
} from "./handler/newComponentHandler";
import {
    cloneChauffagModelToNewComponent,
    cloneLogementModelToNewComponent
} from "./handler/selectTagCloneHandler";
import {
    buildDependencyTree
} from "./handler/dependencyTreeHandler";
import HtmlTagElementFactory from "./factory/htmlTagElementFactory";
import {
    onTypeChangeEvent
} from "./events/onChangeType";
var $ = require('jQuery');

var voltageDOM = ""
var componentList = [];
var tableHandler = "";
var componentFactory = new ComponentFactory();
var csrfToken = "";
const voltageSelectedDOM = "#voltageSelection";

function handleNewRowType(component) {
    let htmlFactory = new HtmlTagElementFactory();
    $("#appendChangeType").empty();
    $("#appendChauffage").empty();

    if (component.attrs.id.includes("C")) {
        cloneLogementModelToNewComponent();
        cloneChauffagModelToNewComponent();
    } else if (component.attrs.id.includes("A")) {
        //TODO Deal with the conductor
        let selectTag = htmlFactory.createTypeSelectTag(component.attrs.id);
        changeTypeByVoltage(csrfToken, voltageSelectedDOM);
        $("#appendChangeType").append(selectTag);
    } else if (component.attrs.id.includes("N")) {
        //For now do nothing with a node component
    }

    document.getElementById("appendChangeType").setAttribute("id", "type_" + component.attrs.id);
    document.getElementById("appendChauffage").setAttribute("id", "type_chauffage_" + component.attrs.id);

    $("#type_" + component.attrs.id).change(function(event) {
        componentList = onTypeChangeEvent(this, componentList);
    });

    $("#type_chauffage_" + component.attrs.id).change(function(event) {
        componentList = onTypeChangeEvent(this, componentList);
    });

    $("#habitable_" + component.attrs.id).change(function(event) {
        componentList = onTypeChangeEvent(this, componentList);
    });

    $("#housings_" + component.attrs.id).change(function(event) {
        componentList = onTypeChangeEvent(this, componentList);
    });

    $("#longueur_" + component.attrs.id).change(function(event) {
        componentList = onTypeChangeEvent(this, componentList);
    })
}

function handleNewRow(component, predecessor) {
    // callback come from tableHandler addNewRow > _appendButtonClickEvent functions
    // Does what _addComponentToList does, but I can't call here since I am not
    // inside the class but inside a callback!
    componentList.push(
        handleNewComponent(component, predecessor, componentList)
    );

    componentList = addFollower(componentList);
    handleNewRowType(component);

    tableHandler.addNewRow(componentList, function(component, predecessor) {
        handleNewRow(component, predecessor);
    });
}

function calculateEvent(csrfToken) {
    $("#calculate_network").click(function(event) {
        console.log(componentList);
        $.ajax({
            url: "get_compute_network",
            type: "POST",
            data: JSON.stringify(componentList),
            headers: {
                "X-CSRFToken": csrfToken,
                "Application-Type": "application/json"
            },
            success: function(computed_values) {
                console.log(computed_values.data);
                document.getElementById("log").innerHTML = computed_values.data;
            },
            error: function(error) {
                alert("Erreur");
            }
        })
    });
}

class ComponentManager {
    constructor(csrfToken, tableDOM, tableBodyDOM) {
        csrfToken = csrfToken;
        this.detailsQuery = new ComponentsDetails(csrfToken);
        tableHandler = new TableHandler(tableDOM, tableBodyDOM);
        this._addInitialElements();
        calculateEvent(csrfToken);
    }

    _addInitialElements() {
        var transformer = componentFactory.buildNewTransformer();
        var conductor = componentFactory.buildNewConductor();
        var node = componentFactory.buildNewNode();
        tableHandler.addComponentToTable(transformer, undefined, this.detailsQuery, function(typeDom, longueurInput) {
            $(typeDom).change(function(event) {
                componentList = onTypeChangeEvent(this, componentList);
            });
            //Not going to use longueurInput since it is not needed for tranformers
        });
        tableHandler.addComponentToTable(conductor, transformer, this.detailsQuery, function(typeDom, longueurInput) {
            $(typeDom).change(function(event) {
                componentList = onTypeChangeEvent(this, componentList);
            });

            $(longueurInput).change(function(event) {
                componentList = onTypeChangeEvent(this, componentList);
            });
        });
        tableHandler.addComponentToTable(node, conductor, this.detailsQuery, function(typeDom, longueurInput) {
            $(typeDom).change(function(event) {
                componentList = onTypeChangeEvent(this, componentList);
            });
            //Not going to use longueurInput since it is not needed for nodes
        });
        this._addComponentToList(transformer, undefined);
        this._addComponentToList(conductor, transformer);
        this._addComponentToList(node, conductor);
        tableHandler.addNewRow(componentList, function(component, predecessor) {
            handleNewRow(component, predecessor);
        });

        $("#showDepency").click(function(event) {
            buildDependencyTree(componentList);
        })
    }

    _addComponentToList(component, predecessor) {
        componentList.push(
            handleNewComponent(component, predecessor, componentList)
        );
        componentList = addFollower(componentList);
    }

    initBaseEvents() {
        changeTypeByVoltage(csrfToken, voltageSelectedDOM);
        $('#voltageSelection').change(function(event) {
            changeTypeByVoltage(csrfToken, voltageSelectedDOM);
        });
    }

}



export {
    ComponentManager,
    componentFactory
}