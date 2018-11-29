var transformerId = 0;
var conductorId = 0;
var clientId = 0;
var nodeId = 0;

class ComponentIdHandler {
    constructor() {}

    setNodeId(value) {
        nodeId = Number(Number(value)) + 1;
    }
    setTransformerId(value) {
        transformerId = Number(value) + 1
    }

    setConductorId(value) {
        conductorId = Number(value) + 1;
    }

    setClientId(value) {
        clientId = Number(value) + 1;
    }

    getTransformerId(newId = true) {
        if (newId) {
            transformerId++;
        }
        return transformerId;
    }

    getConductorId(newId = true) {
        if (newId) {
            conductorId++;
        }
        return conductorId;
    }

    getClientId(newId = true) {
        if (newId) {
            clientId++;
        }
        return clientId;
    }

    getNodeId(newId = true) {
        if (newId) {
            nodeId++;
        }
        return nodeId;
    }
}

var componentIdHandler = new ComponentIdHandler();

export {
    componentIdHandler
}