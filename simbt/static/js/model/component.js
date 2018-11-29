module.exports = class ComponentFactory {
    /*
      Class meant to mimic the component
      that comes out of Konva component objet
    */
    constructor() {
        this.transformerId = 1;
        this.conductorId = 1;
        this.clientId = 1;
        this.nodeId = 1;
    }

    buildComponentFromString(component) {
        var object = "";
        switch (true) {
            case component.includes("A"):
                object = this.buildNewConductor();
                break;
            case component.includes("N"):
                object = this.buildNewNode();
                break;
            case component.includes("C"):
                object = this.buildNewClient();
                break;
        }

        return object;
    }

    buildNewTransformer() {
        return {
            attrs: {
                id: "T" + this.transformerId++
            }
        };
    }

    buildNewConductor() {
        return {
            attrs: {
                id: "A" + this.conductorId++
            }
        };
    }

    buildNewClient() {
        return {
            attrs: {
                id: "C" + this.clientId++
            }
        };
    }

    buildNewNode() {
        return {
            attrs: {
                id: "N" + this.nodeId++
            }
        };
    }
}