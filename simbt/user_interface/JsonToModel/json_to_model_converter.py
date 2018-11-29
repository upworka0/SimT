from django.core import serializers
from user_interface.models import Logement, AutreCharge, Conducteur, Transformateur, Noeud, TypeDeTransformateur, TypeDeChauffage, TypeDeConducteur, TypeDeLogement, LogementCodeSaison
import uuid

class JsonToModelConverter:
    """JsonToModelConverter"""
    def __init__(self, etude):
        """__init__"""
        self.etude = etude

    def convert_json_array_to_model_array(self, json_array):
        """convert_json_array_to_model_array

        :param json_array: array of json object
        """
        self.__clear_study_components_database()
        model_array = []
        for json_object in json_array:
            model_array.append(self.__convert_json_object_to_model(json_object=json_object))
        return model_array

    def __convert_json_object_to_model(self, json_object):
        """__convert_json_object_to_model

        :param json_object: json object
        :return component : Model for database
        """
        component = None
        if 'C' in json_object['nom_du_noeud']:
            type_de_logement = TypeDeLogement.objects.get(type_logement_id=json_object['type_de_logement'])
            type_de_chauffage = TypeDeChauffage.objects.get(type_chauffage_id=json_object['type_de_chauffage'])
            logement_code_saison = LogementCodeSaison.objects.get(logement_code_saison_type=type_de_logement.type_logement_type + type_de_chauffage.type_chauffage_type)
            component = Logement.objects.create(logement_id=uuid.uuid1(), etude_id=self.etude, type_de_logement=type_de_logement, type_de_chauffage=type_de_chauffage,
                                nom_du_noeud=json_object['nom_du_noeud'], surface_habitable=json_object['surface_habitable'],
                                nombre_etage=json_object['nombre_etage'], nombre_de_logement=json_object['nombre_de_logement'],
                                position_x=json_object['position_x'], position_y=json_object['position_y'],
                                predecesseur=json_object['predecesseur'], successeur=json_object['successeur'],
                                logement_code_saison=logement_code_saison)
        elif 'A' in json_object['nom_du_noeud']:
            type_de_conducteur = TypeDeConducteur.objects.get(type_conducteur_id=json_object['type_de_conducteur'])
            component = Conducteur.objects.create(conducteur_id=uuid.uuid1(), etude_id=self.etude, type_conducteur_id=type_de_conducteur, nom_du_noeud=json_object['nom_du_noeud'],
                                    longueur=json_object['longueur'], position_x=json_object['position_x'],
                                    position_y=json_object['position_y'], predecesseur=json_object['predecesseur'],
                                    successeur=json_object['successeur'])
        elif 'N' in json_object['nom_du_noeud']:
            component = Noeud.objects.create(noeud_id=uuid.uuid1(), etude_id=self.etude, nom_du_noeud=json_object['nom_du_noeud'], position_x=json_object['position_x'], position_y=json_object['position_y'], predecesseur=json_object['predecesseur'], successeur=json_object['successeur'])
        elif 'T' in json_object['nom_du_noeud']:
            type_de_transformateur = TypeDeTransformateur.objects.get(type_transformateur_id=json_object['type_de_transformateur'])
            component = Transformateur.objects.create(etude_id=self.etude, type_de_transformateur=type_de_transformateur,
                                            nom_du_noeud=json_object['nom_du_noeud'], position_x=json_object['position_x'],
                                            position_y=json_object['position_y'], successeur=json_object['successeur'],
                                            predecesseur=json_object['predecesseur'])

        return component

    def create_json_array_with_new_model(self, model_array):
        """create_json_array_with_new_model

        :param model_array: array of model object 
        """
        new_model_array = []
        for model_object in model_array:
            new_model_array.append(self.__fetch_model_database(model_object))
        return serializers.serialize('json', new_model_array)

    def __fetch_model_database(self, model_object):
        """__fetch_model_database

            Takes in an object and return the right component
            i.e model_object is a "Transformateur" then it will return a "Transformateur"

        :param model_object:
        """
        if "A" in model_object.nom_du_noeud:
            return Conducteur.objects.get(nom_du_noeud=model_object.nom_du_noeud, etude_id=self.etude)
        elif "C" in model_object.nom_du_noeud:
            return Logement.objects.get(nom_du_noeud=model_object.nom_du_noeud, etude_id=self.etude)
        elif "T" in model_object.nom_du_noeud:
            return Transformateur.objects.get(nom_du_noeud=model_object.nom_du_noeud, etude_id=self.etude)
        elif "N" in model_object.nom_du_noeud:
            return Noeud.objects.get(nom_du_noeud=model_object.nom_du_noeud, etude_id=self.etude)

    def __clear_study_components_database(self):
        """__clear_study_components_database"""
        Logement.objects.filter(etude_id=self.etude).delete()
        Transformateur.objects.filter(etude_id=self.etude).delete()
        Conducteur.objects.filter(etude_id=self.etude).delete()
        Noeud.objects.filter(etude_id=self.etude).delete()

