var $ = require('jQuery');

function displayLodgingSpecificationDetails(lodging_object, callback) {
    var csrf_token = $('.voltageBox input[type="hidden"]').val();
    var type_id = $("#lodgingTypeList").val();
    $.ajax({
        url: "/user_interface/get_type_details/1/" + type_id,
        type: "GET",
        headers: {
            'X-CSRFToken': csrf_token,
            'Application-Type': "application/json"
        },
        success: function(lodging_details) {
            lodging_details = JSON.parse(lodging_details);
            lodging_object.type_de_logement = lodging_details.type_logement_id;
            $("#lodging_description").val(lodging_details.type_logement_description);
            //$("#habitable_area").val(lodging_details.type_logement_superficie_habitable_defaut);
            lodging_object.surface_habitable = lodging_details.type_logement_superficie_habitable_defaut
            callback(lodging_object);
        },
        error: function(err) {
            alert("Erreur");
        }
    });
}

function displayHeatingSpecificationDetails(lodging_object, callback) {
    var csrf_token = $('.voltageBox input[type="hidden"]').val();
    var type_id = $("#heatingTypeList").val();
    $.ajax({
        url: "/user_interface/get_type_details/2/" + type_id,
        type: "GET",
        headers: {
            'X-CSRFToken': csrf_token,
            'Application-Type': "application/json"
        },
        success: function(heating_details) {
            heating_details = JSON.parse(heating_details);
            lodging_object.type_de_chauffage = heating_details.type_chauffage_id;
            $("#heating_description").val(heating_details.type_chauffage_description)
            callback(lodging_object);
        },
        error: function(error) {
            alert("Erreur");
        }
    })
}


function displayConductorSpecificationDetails(conductor_object, callback) {
    var csrf_token = $('.voltageBox input[type="hidden"]').val();
    var type_id = $("#conductorTypeList").val();
    $.ajax({
        url: "/user_interface/get_type_details/0/" + type_id,
        method: "GET",
        headers: {
            'X-CSRFToken': csrf_token,
            'Application-Type': "application/json"
        },
        success: function(conductor_details) {
            conductor_details = JSON.parse(conductor_details);
            conductor_object.type_de_conducteur = conductor_details.type_conducteur_id;
            $("#conductor_description").val(conductor_details.type_conducteur_description);
            $("#conductor_overhead").prop("checked", conductor_details.type_conducteur_est_aerien);
            $("#conductor_resistance_per_km").val(conductor_details.type_conducteur_resistance_par_km);
            $("#conductor_resistance_variation_by_celcius").val(conductor_details.type_conducteur_variation_resistance_par_celcius);
            $("#conductor_resistance_per_km_with_temperature").val(conductor_details.type_conducteur_resistance_par_km_avec_temperature);
            $("#conductor_admissible_current").val(conductor_details.type_conducteur_courant_admissible);
            $("#conductor_variation_temp_depending_current").val(conductor_details.type_conducteur_variation_temp_celon_courant);
            $("#conductor_variation_resistance_depending_current").val(conductor_details.type_conducteur_variation_temp_celon_courant);
            $("#conductor_reactance").val(conductor_details.type_conducteur_reactance);
            $("#conductor_winter_recovery").val(conductor_details.type_conducteur_capacite_repr_hiver);
            $("#conductor_summer_schelude").val(conductor_details.type_conducteur_capacite_planif_ete);
            $("#conductor_client_pole").val(conductor_details.type_conducteur_mat_client == "" ? "------" : conductor_details.type_conducteur_mat_client);
            if (conductor_details.type_conducteur_mat_client != "") {
                var mat_client_id = conductor_details.type_conducteur_mat_client.replace(" ", "sp");
                mat_client_id = mat_client_id.replace('/', 'fs');
                $.ajax({
                    url: "/user_interface/get_type_details/4/" + mat_client_id,
                    method: "GET",
                    headers: {
                        'X-CSRFToken': csrf_token,
                        'Application-Type': "application/json"
                    },
                    success: function(mat_details) {
                        var mat_client_details = JSON.parse(mat_details);
                        $("#client_pole_resistance").val(mat_client_details.mat_client_resistance);
                        $("#client_pole_reactance").val(mat_client_details.mat_client_reactance);
                    },
                    error: function(error) {
                        alert("Erreur");
                    }
                })
            } else {
                $("#client_pole_resistance").val("----");
                $("#client_pole_reactance").val("----");
            }
            callback(conductor_object);
        },
        error: function(error) {
            //TODO Handle erreur differently
            alert("Erreur");
        }
    });
}


function displayTransformerSpecificationDetails(transformer_object, callback) {
    var csrf_token = $('.voltageBox input[type="hidden"]').val();

    var type_id = $("#transformerTypeList").val();
    $.ajax({
        url: "/user_interface/get_type_details/3/" + type_id,
        method: "GET",
        headers: {
            "X-CSRFToken": csrf_token,
            "Application-Type": "application/json"
        },
        success: function(transformer_details) {
            transformer_details = JSON.parse(transformer_details);
            transformer_object.type_de_transformateur = transformer_details.type_transformateur_id;
            $("#transformer_description").val(transformer_details.type_transformateur_description);
            $("#transformer_capacity").val(transformer_details.type_transformateur_capacite);
            $("#transformer_resistance").val(transformer_details.type_transformateur_resistance_pourcent);
            $("#transformer_reactance").val(transformer_details.type_transformateur_reactance_pourcent);
            $("#transformer_no_load_loss").val(transformer_details.type_transformateur_perte_a_vide_pourcent);
            $("#transformer_overhead").prop("checked", transformer_details.type_transformateur_est_aerien);
            callback(transformer_object);
        },
        error: function(error) {
            //TODO Handle error differently
            alert("Erreur");
        }
    })
}


export {
    displayConductorSpecificationDetails,
    displayHeatingSpecificationDetails,
    displayLodgingSpecificationDetails,
    displayTransformerSpecificationDetails
}