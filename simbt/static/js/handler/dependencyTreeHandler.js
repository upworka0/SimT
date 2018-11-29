function buildDependencyTree(componentList) {
    $("#dependenciesTree").empty();
    for (let i = 0; i < componentList.length; i++) {
        if (componentList[i].nom_du_noeud.includes("C")) {
            var conductor = componentList.filter(function(comp) {
                if (componentList[i].predecesseur == comp.nom_du_noeud) {
                    return comp;
                }
            });
            var node = componentList.filter(function(comp) {
                if (conductor[0].predecesseur == comp.nom_du_noeud) {
                    return comp;
                }
            });
            var client = componentList[i].nom_du_noeud;
            $("#dependenciesTree").append(
                "<div class=\"row\"><p class=\"col-md-2\">" + node[0].nom_du_noeud + "</p><p class=\"col-md-2\">" + client + "</p></div>"
            );
        }
    }
}

export {
    buildDependencyTree
}