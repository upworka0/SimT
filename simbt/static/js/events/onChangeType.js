const typeRegex = /([T]{1}[0-9]{1,3}|[A]{1}[0-9]{1,3}|[C]{1}[0-9]{1,3}|[N]{1}[0-9]{1,3})/;

function onTypeChangeEvent(dom, componentList) {
    let parent = $(dom).attr("id");
    let compID = typeRegex.exec(parent);
    let typeId = $(dom).children().val();
    let typeChauffageId = undefined;
    let areaHabitable = undefined;
    let numberHousing = 1;
    let logementId = undefined;
    let longueur = undefined;
    let nombreEtage = undefined;
    if (compID[0].includes("C")) {
        typeChauffageId = $("#type_chauffage_" + compID[0]).children().val().trim("-");
        logementId = $("#type_" + compID[0]).children().val().trim("-");
        areaHabitable = Number($("#area_" + compID[0]).val());
        numberHousing = Number($("#housings_" + compID[0]).val());
        nombreEtage = Number($("#etage_" + compID[0]).val())
    } else if (compID[0].includes("A")) {
        var selectType = $("#type_" + compID[0]).children();
        typeId = selectType[0].options[selectType[0].selectedIndex].value;
        longueur = Number($("#longueur_" + compID[0]).children().val());
    }
    //TODO find ID in componentList and make the changes
    let component = componentList.filter(function(comp) {
        if (comp.nom_du_noeud == compID[0]) {
            return comp;
        }
    });

    switch (true) {
        case compID[0].includes("T"):
            component[0].type_de_transformateur = typeId;
            break;
        case compID[0].includes("A"):
            console.log(typeId);
            console.log(longueur);
            component[0].type_de_conducteur = typeId;
            component[0].longueur = longueur;
            break;
        case compID[0].includes("C"):
            component[0].type_de_logement = logementId;
            component[0].type_de_chauffage = typeChauffageId;
            component[0].surface_habitable = areaHabitable;
            component[0].nombre_de_logement = numberHousing;
            component[0].nombre_etage = nombreEtage;
            break;
    }

    for (let i = 0; i < componentList.length; i++) {
        if (component[0].nom_du_noeud == componentList[i].nom_du_noeud) {
            componentList[i] = component[0];
            return componentList;
        }
    }
}

export {
    onTypeChangeEvent
}