import {
    handleConductorSplitting,
    setSelectionNode,
    handleConductorSpecificationTab,
    hideAllSpecs
} from "../canvas";
var isLineOnElement = false;
class KonvaComponentsEvents {
    conductorOnClick(conductorElement) {
        conductorElement.addEventListener('click', function(event) {
            var self = this;
            if (createLine == true) {
                isLineOnElement = true;
                setSelectionNode(self);
                handleConductorSplitting(self);
            } else {
                // specificationConductorModal.style.display = "block";
                // document.getElementById("conductor-name").innerHTML = this.attrs.id;
                hideAllSpecs();
                conductorSpecs.style.display = "block";
                elementName.innerHTML = "Conducteur : " + this.attrs.id;
                //TODO Set value to input type hidden
                handleConductorSpecificationTab(self);
            }
        });
    }

    transformerOnClick() {}

    clientOnClick() {}

    nodeOnClick() {}
}

var konvaComponentEvents = new KonvaComponentsEvents();

export {
    konvaComponentEvents
}