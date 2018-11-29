var $ = require('jQuery');

module.exports = function changeTypeByVoltage(csrfToken, domId) {
    /*
      Function that changes Transformer and Conductor Types in the table
      from  the Voltage they can use.
    */
    var study_voltage = $(domId).val();
    var json_data = "";
    $.ajax({
        url: "get_type_possible_information/" + study_voltage,
        method: "GET",
        headers: {
            "X-CSRFToken": csrfToken,
            "Application-Type": "application/json"
        },
        success: function(response) {
            console.log(response);
            var transformerType = $('#transformerTypeList');
            transformerType.empty();
            transformerType.append($('<option></option>').attr('value', 'None').text(" ---- "));
            $.each(response.type_transformateur, function(key, value) {
                json_data = JSON.parse(value);
                transformerType.append($('<option></option>')
                    .attr("value", json_data.type_transformateur_id)
                    .text(json_data.type_transformateur_type));
            });

            // var conductorType = $('#conductorTypeList');
            // conductorType.empty();
            // conductorType.append($('<option></option>').attr('value','None').text(' ---- '));
            $(".conductorTypeList").each(function() {
                $(this).empty();
                $(this).append($('<option></option>').attr('value', 'None').text(' ---- '));
                var conductorType = $(this);
                $.each(response.type_conducteur, function(key, value) {
                    json_data = JSON.parse(value);
                    conductorType.append($('<option></option')
                        .attr("value", json_data.type_conducteur_id)
                        .text(json_data.type_conducteur_type));

                });
            });

        },
        error: function(response) {
            alert('Fail')
        }
    });
}