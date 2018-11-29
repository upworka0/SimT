var selectTool = true;
var moveTool = false;
var createLine = false;
var createTransfo = false;
var createClient = false;

var selectionButton = document.getElementById("selectionButton");
// var moveButton = document.getElementById("moveButton");
var conductorButton = document.getElementById("conductorButton");
// var transformerButton = document.getElementById("tranformerButton");
var clientButton = document.getElementById("clientButton");
var resetButton = document.getElementById("resetButton");

//Reset the button that are selected in the toolbar pane
function resetButtonSelected() {
    conductorButton.className = "button";
    selectionButton.className = "button";
    // transformerButton.className = "";
    clientButton.className = "button";
    // moveButton.className = "";
}

//Reset booleans that keeps track of which element to create
//Used in events that creates new elements
function resetSelectorState() {
    selectTool = false;
    // moveTool = false;
    createLine = false;
    createTransfo = false;
    createClient = false;
}

//Change the element parameter to show to the user that it has been selected
//Toolbox pane buttons changes color
function selectButton(element) {
    element.className = "button button-selected";
}

//Function to set Conductor as the element to create when clicking (toolbar or context menu)
function selectConductor() {
    resetSelectorState();
    createLine = true;
    resetButtonSelected();
    selectButton(conductorButton);
}

//Function to set Transformer as the element to create when clicking (toolbar or context menu)
function selectTranformer() {
    resetSelectorState();
    createTransfo = true;
    resetButtonSelected();
    selectButton(transformerButton);
}

//Function to set Client as the element to create when clicking (toolbar or context menu)
function selectClient() {
    resetSelectorState();
    createClient = true;
    resetButtonSelected();
    selectButton(clientButton);
}

//Function to set Select Tool as active (toolbar or context menu (soon))
function selectSelectTool() {
    resetSelectorState();
    selectTool = true;
    resetButtonSelected();
    selectButton(selectionButton);
}



export {
    selectTool,
    moveTool,
    createLine,
    createTransfo,
    createClient,
    selectClient,
    selectTranformer,
    selectConductor,
    selectSelectTool
}