import json
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from user_interface.edit_study_context import EditStudyContext
from user_interface.compute_network.compute_network import  ComputeNetwork
from user_interface.models import Etude, Client, Logement, Conducteur, Transformateur, TypeDeLogement, TypeDeChauffage, TypeDeConducteur, TypeDeTransformateur, LogementCodeSaison, Admin
from user_interface.JsonToModel.json_to_model_converter import JsonToModelConverter
edit_study_context = EditStudyContext()
import uuid

def get_type_possible_information(request, voltage_type=None):
    """
        Method that takes the voltage from the study in use and returns all
        possible value that can be used with the different component in the
        study
    """
    if request.method == "GET":
        print(request)
        study_context = edit_study_context.build_context_json(study_voltage=voltage_type)
        return JsonResponse(study_context, safe=False)

def save_study(request, study_id=None):
    """save_study
        Takes in a JSON with both
        visual and data json object from front-end

        Expected body :
            {
                "visual": "[ ... JSON ARRAY ...  ]",
                "data" :  "[ ... JSON ARRAY ...  ]"
            }
    :param request: HTTP request
    """
    if request.method == "POST" and study_id != None:
        try:
            json_body = json.loads(request.body.decode('utf-8'))
            etude = Etude.objects.filter(etude_id=study_id).get()
            etude.etude_component_list = json_body['data']#JSON array from Front-end "data"
            etude.etude_serialized_visual = json_body['visual'] # JSON array from Front-end "visual"
            etude.save()
            return HttpResponse(status=202)
        except Exception :
            return HttpResponse(status=500)
    return HttpResponse(status=400)


def get_type_details(request, what_type=None, type_id=None):
    """
        Request that fetch the details for a
        conductor, transformer, heating unit,
        lodging, or a client pole as a JsonResponse
    """
    possible_type = {
        0: "conducteur",
        1: "logement",
        2: "chauffage",
        3: "transformateur",
        4: "matclient",
    }
    if request.method == "GET":
        details = ""
        what_type = int(what_type)
        if int(what_type) in possible_type.keys():
            type_request = possible_type[what_type]
            if type_request == possible_type[0]:
                details = edit_study_context.fetch_conductor_type_details(conductor_id=type_id)
            elif type_request == possible_type[1]:
                details = edit_study_context.fetch_housing_type_details(housing_id=type_id)
            elif type_request == possible_type[2]:
                details = edit_study_context.fetch_heating_type_details(heating_id=type_id)
            elif type_request == possible_type[3]:
                details = edit_study_context.fetch_transformer_type_details(transformer_id=type_id)
            elif type_request == possible_type[4]:
                type_id = type_id.replace("sp", ' ')
                type_id = type_id.replace("fs", '/')
                details = edit_study_context.fetch_client_pole_details(client_pole_id=type_id)
        return JsonResponse(details, safe=False)

def get_compute_network(request, etude_id):
    """Compute network
    
    Arguments:
        request {HttpRequests} -- Information from front-end
    
    Returns:
        JSON Object -- Computed data from backend that goes back to fron-end so it can display the data
    """
    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        json_data = json.loads(body_unicode)
        admin = Admin.objects.all().get()
        etude = Etude.objects.get(etude_id=etude_id)
        compute_network = ComputeNetwork(admin=admin, study=etude) 
        json_converter = JsonToModelConverter(etude=etude)
        model_array = json_converter.convert_json_array_to_model_array(json_array=json_data)
        print(len(model_array))
        for model in model_array:
            if 'C' in model.nom_du_noeud:
                compute_network.compute_loads_node(logement_id=model.nom_du_noeud)
        for model in model_array:
            if 'T' in model.nom_du_noeud:
                compute_network.compute_network(transformateur_id=model.nom_du_noeud)
        return JsonResponse({"status_code": 1, "data": json_converter.create_json_array_with_new_model(model_array=model_array)})