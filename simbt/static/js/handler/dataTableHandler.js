import HtmlTagElementFactory from "./../factory/htmlTagElementFactory";
var $ = require('jQuery');

class DataTableHandler {
    /* Expect an ID -> #transformer_data */
    constructor(tableId) {
        this.tableId = tableId;
        this.htmlTagFactory = new HtmlTagElementFactory();
        this.tableDom = $(tableId);
        this.emptyTable();
        this.buildTableHeader();
    }

    emptyTable() {
        $(this.tableId).empty();
    }

    buildTableHeader() {
        var header = "";
        switch (true) {
            case this.tableId.includes("transformer"):
                header = this.__generateTransformerHeader();
                break;
            case this.tableId.includes('client'):
                header = this.__generateClientHeader();
                break;
            case this.tableId.includes("node"):
                header = this.__generateNodeHeader();
                break;
            case this.tableId.includes("conductor"):
                header = this.__generateConductorHeader();
                break;
        }
        var thead = this.htmlTagFactory.createTheadElement();
        header.forEach(function(element) {
            thead.appendChild(element);
        });
        this.tableDom.append(thead);
    }

    addDataRow(jsonObject) {
        var data = "";

        switch (true) {
            case this.tableId.includes("transformer"):
                data = this.__buildTransformerDataRow(jsonObject);
                break;
            case this.tableId.includes("client"):
                data = this.__buildCliendDataRow(jsonObject);
                break;
            case this.tableId.includes('node'):
                data = this.__buildNodeDataRow(jsonObject);
                break;
            case this.tableId.includes('conductor'):
                data = this.__buildConductorDataRow(jsonObject);
                break;
        }
        var tbody = this.htmlTagFactory.createTbodyElement();
        data.forEach(function(element) {
            tbody.appendChild(element);
        });
        this.tableDom.append(tbody);
    }

    __buildTransformerDataRow(jsonObject) {
        var data = [
            this.__buildTdElement(jsonObject.nom_du_noeud),
            this.__buildTdElement(jsonObject.noeud_alias),
            this.__buildTdElement(jsonObject.transformateur_charge_diversite_ete),
            this.__buildTdElement(jsonObject.transformateur_charge_diversite_ete_kvar),
            this.__buildTdElement(jsonObject.transformateur_charge_diversite_ete_kw),
            this.__buildTdElement(jsonObject.transformateur_charge_diversite_hiver),
            this.__buildTdElement(jsonObject.transformateur_charge_diversite_hiver_kvar),
            this.__buildTdElement(jsonObject.transformateur_charge_diversite_hiver_kw),
            this.__buildTdElement(jsonObject.transformateur_charge_max_ete_aval),
            this.__buildTdElement(jsonObject.transformateur_charge_max_hiver_aval),
            this.__buildTdElement(jsonObject.transformateur_charge_reprise_hiver),
            this.__buildTdElement(jsonObject.transformateur_charge_reprise_hiver_kvar),
            this.__buildTdElement(jsonObject.transformateur_charge_reprise_hiver_kw),
            this.__buildTdElement(jsonObject.transformateur_chute_cummul_v_pourcent * 100),
            this.__buildTdElement(jsonObject.transformateur_chute_loc_v_pourcent * 100),
            this.__buildTdElement(jsonObject.transformateur_i_court_circuit),
            this.__buildTdElement(jsonObject.transformateur_noeud_charge_ete_max),
            this.__buildTdElement(jsonObject.transformateur_noeud_charge_hiver_max),
            this.__buildTdElement(jsonObject.transformateur_niveau_diversite)
        ];
        return data;
    }

    __buildConductorDataRow(jsonObject) {
        var data = [
            this.__buildTdElement(jsonObject.nom_du_noeud),
            this.__buildTdElement(jsonObject.conducteur_charge_diversite_ete),
            this.__buildTdElement(jsonObject.conducteur_charge_diversite_ete_kvar),
            this.__buildTdElement(jsonObject.conducteur_charge_diversite_ete_kw),
            this.__buildTdElement(jsonObject.conducteur_charge_diversite_hiver),
            this.__buildTdElement(jsonObject.conducteur_charge_diversite_hiver_kvar),
            this.__buildTdElement(jsonObject.conducteur_charge_diversite_hiver_kw),
            this.__buildTdElement(jsonObject.conducteur_charge_max_ete_aval),
            this.__buildTdElement(jsonObject.conducteur_charge_max_hiver_aval),
            this.__buildTdElement(jsonObject.conducteur_reprise_hiver),
            this.__buildTdElement(jsonObject.conducteur_reprise_hiver_kvar),
            this.__buildTdElement(jsonObject.conducteur_reprise_hiver_kw),
            this.__buildTdElement(jsonObject.conducteur_chute_cummul_v_pourcent * 100),
            this.__buildTdElement(jsonObject.conducteur_chute_loc_v_pourcent * 100),
            this.__buildTdElement(jsonObject.conducteur_i_court_circuit),
            this.__buildTdElement(jsonObject.conducteur_noeud_charge_ete_max),
            this.__buildTdElement(jsonObject.conducteur_noeud_charge_hiver_max),
            this.__buildTdElement(jsonObject.conducteur_niveau_diversite)
        ];
        return data;

    }

    __buildNodeDataRow(jsonObject) {
        var data = [
            this.__buildTdElement(jsonObject.nom_du_noeud),
            this.__buildTdElement(jsonObject.noeud_alias),
        ]
        return data;
    }

    __buildCliendDataRow(jsonObject) {
        var data = [
            this.__buildTdElement(jsonObject.nom_du_noeud),
            this.__buildTdElement(jsonObject.noeud_alias),
            this.__buildTdElement(jsonObject.logement_charge_pointe_ete),
            this.__buildTdElement(jsonObject.logement_charge_pointe_ete_kvar),
            this.__buildTdElement(jsonObject.logement_charge_pointe_ete_kw),
            this.__buildTdElement(jsonObject.logement_charge_pointe_hiver),
            this.__buildTdElement(jsonObject.logement_charge_pointe_hiver_kvar),
            this.__buildTdElement(jsonObject.logement_charge_pointe_hiver_kw),
            this.__buildTdElement(jsonObject.logement_charge_reprise_hiver),
            this.__buildTdElement(jsonObject.logement_charge_reprise_hiver_kvar),
            this.__buildTdElement(jsonObject.logement_charge_reprise_hiver_kw),
            this.__buildTdElement(jsonObject.logement_fp_ete),
            this.__buildTdElement(jsonObject.logement_fp_hiver),
            this.__buildTdElement(jsonObject.logement_fr_ete),
            this.__buildTdElement(jsonObject.logement_fr_hiver),
            this.__buildTdElement(jsonObject.logement_fp_reprise_hiver),
            this.__buildTdElement(jsonObject.logement_fr_reprise_hiver),
            this.__buildTdElement(jsonObject.logement_i_court_circuit_client),
            this.__buildTdElement(jsonObject.logement_i_court_circuit)
        ];
        return data;
    }

    __generateTransformerHeader() {
        var header = [
            this.__buildThElement("Nom"),
            this.__buildThElement('Alias'),
            this.__buildThElement("Charge de diversité (Été)"),
            this.__buildThElement("Charge de diversité en kVar (Été)"),
            this.__buildThElement("Charge de diversité en KW (Été)"),
            this.__buildThElement("Charge de diversité (Hiver)"),
            this.__buildThElement("Charge de diversité en kVar (Hiver)"),
            this.__buildThElement("Charge de diversité en KW (Hiver)"),
            this.__buildThElement("Charge maximum en aval (Été)"),
            this.__buildThElement("Charge maximum en aval (Hiver)"),
            this.__buildThElement("Charge de reprise (Hiver)"),
            this.__buildThElement("Charge de reprise en kVar (Hiver)"),
            this.__buildThElement("Charge de reprise en KW (Hiver)"),
            this.__buildThElement("Chute de tension cummulée (%)"),
            this.__buildThElement("Chute de tension loc (%)"),
            this.__buildThElement("Courant de court-circuit"),
            this.__buildThElement("Charge max (Été)"),
            this.__buildThElement("Charge max (Hiver)"),
            this.__buildThElement("Niveau de diversité"),
        ];
        return header;
    }

    __generateClientHeader() {
        var header = [
            this.__buildThElement("Nom"),
            this.__buildThElement('Alias'),
            this.__buildThElement("Pointe de la charge (Été)"),
            this.__buildThElement("Pointe de la Charge en kVar (Été)"),
            this.__buildThElement("Pointe de la charge en KW (Été)"),
            this.__buildThElement("Pointe de la charge (Hiver)"),
            this.__buildThElement("Pointe de la charge en kVar (Hiver)"),
            this.__buildThElement("Pointe de la charge en KW (Hiver)"),
            this.__buildThElement("Charge de reprise (Hiver)"),
            this.__buildThElement("Charge de reprise en kVar (Hiver)"),
            this.__buildThElement("Charge de reprise en KW (Hiver)"),
            this.__buildThElement("Facteur de puissance (Été)"),
            this.__buildThElement("Facteur de puissance (Hiver)"),
            this.__buildThElement("Facteur de réactance (Été)"),
            this.__buildThElement("Facteur de réactance (Hiver)"),
            this.__buildThElement("Facteur de puissance en reprise (Hiver)"),
            this.__buildThElement("Facteur de réactance en reprise (Hiver)"),
            this.__buildThElement("Courant de court-circuit (Client)"),
            this.__buildThElement("Courant de court-circuit"),
        ];
        return header;
    }

    __generateNodeHeader() {
        var header = [
            this.__buildThElement("Nom"),
            this.__buildThElement('Alias'),
        ];
        return header;
    }

    __generateConductorHeader() {
        var header = this.__generateTransformerHeader();
        header.splice(1, 1);
        return header;
    }

    __buildThElement(text) {
        var th = this.htmlTagFactory.createThElement();
        th.innerHTML = text;
        return th;
    }

    __buildTdElement(text) {
        var td = this.htmlTagFactory.createTdElement();
        if (typeof text == typeof 0 || typeof text == typeof 0.00) {
            text = parseFloat(text).toFixed(4);
        }
        td.innerHTML = text;
        return td;
    }
}

export {
    DataTableHandler
}