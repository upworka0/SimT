import json
from django.forms.models import model_to_dict
from user_interface.models import TypeDeChauffage, TypeDeConducteur, TypeDeLogement, TypeDeTransformateur, MatClient

class EditStudyContext():
    """
        Class that will return the context for edit_study page
    """
    __TYPE_CONDUCTOR_ID="type_conducteur_id"
    __TYPE_HOUSING_ID="type_logement_id"
    __TYPE_HEATING_ID="type_chauffage_id"
    __TYPE_TRANSFORMER_ID="type_transformateur_id"
    __MAT_CLIENT_ID="mat_client_id"

    def __init__(self):
        pass

    def build_context(self, study_voltage):
        """
            Method that will build a dictionnary
            as a context for edit_study
            ***
                PARAMETER :
                    study_id (For now, it is the study voltage)
            ***
        """
        type_list = dict()
        type_list['type_chauffage'] = TypeDeChauffage.objects.all()
        type_conductor = TypeDeConducteur.objects
        type_transformateur = TypeDeTransformateur.objects
        # Type conductor voltage are between 0 and 1
        # But it is possible to have a value of 2
        if study_voltage == "120/240": #Voltage of 120/240V
            type_conductor = type_conductor.filter(type_conducteur_tension = 0)
            type_transformateur = TypeDeTransformateur.objects.filter(type_transformateur_tension = 0)
        elif study_voltage == "120/208": #Voltage of 120/208V or 347/600V
            type_conductor = type_conductor.filter(type_conducteur_tension = 1)
            type_transformateur = TypeDeTransformateur.objects.filter(type_transformateur_tension = 1)
        elif study_voltage == "347/600":
            type_conductor = type_conductor.filter(type_conducteur_tension = 1)
            type_transformateur = TypeDeTransformateur.objects.filter(type_transformateur_tension = 2)
        type_list['type_conducteur'] = type_conductor.all()
        type_list['type_logement'] = TypeDeLogement.objects.all()
        type_list['type_transformateur'] = type_transformateur.all()
        return type_list


    def build_context_json(self, study_voltage):
        """
            Method that takes in the study voltage to
            retrieve data from database, then return
            a serialize list in json for the user
        """
        type_list = dict()
        type_conductor = TypeDeConducteur.objects
        if int(study_voltage) == 0:
            type_conductor = type_conductor.filter(type_conducteur_tension=study_voltage)
        elif int(study_voltage) >= 1:
            type_conductor = type_conductor.filter(type_conducteur_tension__lte=study_voltage,
                                                   type_conducteur_tension__gte=int(study_voltage) - 1)
        type_list['type_conducteur'] = self.__serialize_list_model_to_json(model_list=type_conductor, model_id=self.__TYPE_CONDUCTOR_ID)
        type_list['type_transformateur'] = self.__serialize_list_model_to_json(model_list=TypeDeTransformateur.objects.filter(type_transformateur_tension=study_voltage), model_id=self.__TYPE_TRANSFORMER_ID)
        return type_list


    def fetch_housing_type_details(self, housing_id):
        """
            Method that returns all the information related
            to a specific type of housing
        """
        housing_type_details = TypeDeLogement.objects.get(type_logement_id=housing_id)
        return self.__serialize_model_to_json(model=housing_type_details, model_id=self.__TYPE_HOUSING_ID)

    def fetch_conductor_type_details(self, conductor_id):
        """
            Method that returns all the information related
            to a specific conductor
        """
        conductor_type_details = TypeDeConducteur.objects.get(type_conducteur_id=conductor_id)
        return self.__serialize_model_to_json(model=conductor_type_details, model_id=self.__TYPE_CONDUCTOR_ID)

    def fetch_heating_type_details(self, heating_id):
        """
            Method that returns all the information related
            to a specific heating type
        """
        heating_type_details = TypeDeChauffage.objects.get(type_chauffage_id=heating_id)
        return self.__serialize_model_to_json(model=heating_type_details, model_id=self.__TYPE_HEATING_ID)

    def fetch_transformer_type_details(self, transformer_id):
        """
            Method that returns all the information related
            to a specific tranformer type
        """
        transformer_type_details = TypeDeTransformateur.objects.get(type_transformateur_id=transformer_id)
        return self.__serialize_model_to_json(model=transformer_type_details, model_id=self.__TYPE_TRANSFORMER_ID)

    def fetch_client_pole_details(self, client_pole_id):
        """
            Method that retunrs all the information
            related to a specific "MatClient"
        """
        mat_client_details = MatClient.objects.get(mat_client_id=client_pole_id)
        return self.__serialize_model_to_json(model=mat_client_details, model_id=self.__MAT_CLIENT_ID)

    def __serialize_list_model_to_json(self, model_list, model_id):
        """
                       *** PRIVATE METHOD ***
            Method that will take in the list from the database
            and return a list serialized as a json list of object
        """
        json_list = list()
        for model in model_list.all():
           json_list.append(self.__serialize_model_to_json(model=model, model_id=model_id))
        return json_list

    def __serialize_model_to_json(self, model, model_id):
        """
                    *** PRIVATE METHOD ***
            Method that takes in the model as parameter
            returns an object serialized as a json file
        """
        dict_obj = model_to_dict(instance=model)
        dict_obj[model_id] = str(dict_obj[model_id])
        return json.dumps(dict_obj)
