function cloneLogementModelToNewComponent() {
    $("#selectChauffageModel").clone().appendTo("#appendChauffage");
}

function cloneChauffagModelToNewComponent() {
    $("#selectLogementModel").clone().appendTo("#appendChangeType");
}

export {
    cloneChauffagModelToNewComponent,
    cloneLogementModelToNewComponent
}