var Konva = require('konva');


/*
  @DESCRIPTION : Create object from an image, it can be a client or a transformer
  @PARAM : x : Number -> usually 50 in a Konva.group
  @PARAM : y : Number -> usually 0 in a Konva.group
  @PARAM : width : Number -> usually 100
  @PARAM : height : Number -> usually 150,
  @PARAM : completeId : Number i.e C1
  @RETURN : konvaImage : Konva Object
*/
function getNewImage(x, y, width, height, image, completeId) {
    var konvaImage = new Konva.Image({
        x: x,
        y: y,
        image: image,
        width: width,
        height: height,
        id: completeId
    });

    return konvaImage;
}
/*
  @PARAM : horizontalLine : Number
  @PARAM : verticalLine : Number
  @PARAM : color : string
  @PARAM : id : Number
  @RETURN : Konva.Line({}) : Konva object
*/
function getNewLine(x, y, horizontalLine, verticalLine, color, completeId) {
    var line = new Konva.Line({
        x: x,
        y: y,
        points: [0, 0, 0, 0, 0, 0, horizontalLine, verticalLine],
        stroke: color,
        strokeWidth: 8,
        tension: 1.5,
        id: completeId
    });
    return line;
}
/*
  @PARAM : x : Number
  @PARAM : y : Number
  @PARAM : radius : Number
  @PARAM : strokeWidth : Number
  @PARAM : fill : string -> black, blue, green ... etc
  @PARAM : strokeColor : string -> black, blue, green .. etc
  @PARAM : nodeId : Number -> 1, 2 , 3, 4 ...  etc
  @RETURN : node : konva object -> Konva.Circle
*/
function getNewNode(x, y, radius, strokeWidth, fill, strokeColor, nodeId) {
    var node = new Konva.Circle({
        x: x,
        y: y,
        radius: radius,
        fill: fill,
        stroke: strokeColor,
        strokeWidth: strokeWidth,
        id: nodeId
    });
    return node;
}

/*
  @PARAM : x : Number -> usually horizontalWidth / 2 for Conductors
  @PARAM : y : Number -> usually verticalHeight / 2 for Conductors
  @PARAM : text : string i.e A2
  @PARAM : completeId : string i.e A2_text
  @RETURN : idText : Konva Object
*/
function getNewText(x, y, text, completeId) {
    var idText = new Konva.Text({
        x: x,
        y: y,
        text: text,
        fontSize: 30,
        fontFamily: 'Calibri',
        fill: 'black',
        id: completeId
    });
    return idText;
}

/*
  @PARAM : x : number -> usually ((firstCoordinates.x / zoomLevel) + currentLayerPositionX)
  @PARAM : y : number -> usually ((firstCoordinates.y / zoomLevel) + currentLayerPositionY)
  @PARAM : completeId : String -> i.e A1_Group (ID went through generateGroupIdString)
  @RETURN : group : Konva.Group object
*/
function getNewGroup(x, y, completeId) {
    var group = new Konva.Group({
        id: completeId,
        x: x,
        y: y
    });
    return group;
}

export {
    getNewLine,
    getNewText,
    getNewImage,
    getNewNode,
    getNewGroup
}