import os
import json
import csv
import re
import uuid
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

TYPE_CONDUCTEUR_FILE = os.path.join(BASE_DIR, "Type_conducteur.csv")
TYPE_XFO_FILE = os.path.join(BASE_DIR, 'Type_xfo.csv')
TYPE_CHAUFFAGE_FILE = os.path.join(BASE_DIR, "Type_chauffage.csv")
LOGEMENT_CODE_SAISON_FILE = os.path.join(BASE_DIR, "Logement_code_saison.csv")
COURBE_DE_DIVERSITEES_FILE = os.path.join(BASE_DIR, "courbe_diversites.csv")
TYPE_LOGEMENT_FILE = os.path.join(BASE_DIR, "Type_logements.csv")

JSON_FILE_XFO = os.path.join(BASE_DIR, 'xfo_data.json')
JSON_FILE_CONDUCTEUR = os.path.join(BASE_DIR, 'conducteur.json')
JSON_FILE_MAT_CLIENT = os.path.join(BASE_DIR, 'mat_client.json')
JSON_FILE_CHAUFFAGE = os.path.join(BASE_DIR, "chauffage.json")
JSON_FILE_LOGEMENT_CODE_SAISON = os.path.join(BASE_DIR, "logement_code_saison.json")
JSON_FILE_COURBE_DIVERSITEES = os.path.join(BASE_DIR, "courbe_diversites.json")
JSON_FILE_TYPE_LOGEMENT = os.path.join(BASE_DIR, 'type_logement.json')

VOLTAGE_REGEX_STRING = r'([0-6]{2}\d\/[0-6]{2}\d(( [V|v])|[V|v]))'
AIRBORNE_REGEX_STRING = r'(aerien)\w'

def seed_type_xfo():
    """
        Function that will handle seeding of xfo
    """
    with open(TYPE_XFO_FILE, newline='', encoding='latin-1') as csvfile:
        xfo_data = csv.reader(csvfile, dialect='excel')
        json_dump_object = list()
        type_voltage = ""
        for row in xfo_data:
            voltage_pattern = re.match(VOLTAGE_REGEX_STRING, row[0].strip())
            if voltage_pattern is not None:
                type_voltage = voltage_pattern.group()
            elif voltage_pattern is None:
                type_value = 0
                if type_voltage == "120/240 V":
                    type_value = 0
                elif type_voltage == "120/208 V":
                    type_value = 1
                elif type_voltage == "347/600 V":
                    type_value = 2

                if type_voltage is not "" and row[1].strip() is not '':
                    is_airborne = False
                    airborne_pattern = re.match(AIRBORNE_REGEX_STRING, row[1])

                    if airborne_pattern is not None:
                        is_airborne = True

                    json_dump_object.append({
                        "model": "user_interface.TypeDeTransformateur",
                        "pk": str(uuid.uuid1()),
                        "fields" : {
                            "type_transformateur_tension": type_value,
                            "type_transformateur_description": row[1],
                            "type_transformateur_type":row[0],
                            "type_transformateur_capacite": row[3],
                            "type_transformateur_resistance_pourcent": row[4].strip('%'),
                            "type_transformateur_reactance_pourcent": row[5].strip('%'),
                            "type_transformateur_perte_a_vide_pourcent": row[6].strip('%'),
                            "type_transformateur_est_aerien": is_airborne,
                            "type_transformateur_date_creation": str(time.strftime("%Y-%m-%d", time.localtime())),
                            "type_transformateur_date_modification": str(time.strftime("%Y-%m-%d", time.localtime()))
                        }
                    })

        with open(JSON_FILE_XFO, 'w') as fw:
            fw.write(json.dumps(json_dump_object))

def seed_type_conductor():
    """
        Function that handle the seedinng of conductors to database
    """
    with open(TYPE_CONDUCTEUR_FILE, newline='', encoding='latin-1') as csvfile:
        conductor_data = csv.reader(csvfile, dialect='excel')
        json_dump_object = list()
        type_voltage = ""
        json_client_mat = list()
        for row in conductor_data:
            voltage_pattern = re.match(VOLTAGE_REGEX_STRING, row[0].strip())
            if voltage_pattern is not None:
                type_voltage = voltage_pattern.group()
            elif voltage_pattern is None:
                type_value = 0
                if type_voltage == "120/240V":
                    type_value = 0
                elif type_voltage == "120/208V":
                    type_value = 1

                if type_voltage is not "" and row[0].strip() is not '':
                    json_dump_object.append({
                        "model" : "user_interface.TypeDeConducteur",
                        "pk": str(uuid.uuid1()),
                        "fields":{
                            "type_conducteur_tension": type_value,
                            "type_conducteur_type": row[0],
                            "type_conducteur_description": row[1],
                            "type_conducteur_est_aerien": (True if row[3] == "A" else False),
                            "type_conducteur_resistance_par_km": row[4].replace(",", ""),
                            "type_conducteur_variation_resistance_par_celcius":row[5].replace(",",""),
                            "type_conducteur_resistance_par_km_avec_temperature": row[6].replace(",",""),
                            "type_conducteur_courant_admissible": row[7].replace(",",""),
                            "type_conducteur_variation_temp_celon_courant": row[8].replace(",",""),
                            "type_conducteur_variation_resistance_celon_courant": row[9].replace(",",""),
                            "type_conducteur_reactance": row[10].replace(",",""),
                            "type_conducteur_capacite_repr_hiver": row[11].replace(",",""),
                            "type_conducteur_capacite_planif_ete": row[12].replace(",",""),
                            "type_conducteur_mat_client": row[13].replace(",",""),
                            "type_conducteur_date_creation": str(time.strftime("%Y-%m-%d", time.localtime())),
                            "type_conducteur_date_modification": str(time.strftime("%Y-%m-%d", time.localtime())),
                        }
                    })
                    key_exists = False
                    for mat_client in json_client_mat:
                        if row[13] == mat_client['pk']:
                            key_exists = True

                    if key_exists is False:
                        json_client_mat.append({
                            "model": "user_interface.MatClient",
                            "pk": row[13],
                            'fields': {
                                "mat_client_resistance": row[14],
                                "mat_client_reactance": row[15]
                            }
                        })

        with open(JSON_FILE_CONDUCTEUR, 'w') as fw:
            fw.write(json.dumps(json_dump_object))
        with open(JSON_FILE_MAT_CLIENT, 'w') as fw:
            fw.write(json.dumps(json_client_mat))

def seed_type_chauffage():
    """
        Function that will create json file so it can be loaded up
        into the database
    """
    with open(TYPE_CHAUFFAGE_FILE, newline='', encoding='latin-1') as csvreader:
        heating_data = csv.reader(csvreader, dialect='excel')
        json_data_dump = list()
        for row in heating_data:
            if row[0] != "Type de chauffage":
                if row[0] != "":
                    json_data_dump.append({
                        "model": "user_interface.TypeDeChauffage",
                        "pk": str(uuid.uuid1()),
                        "fields":{
                            "type_chauffage_type" : row[0],
                            "type_chauffage_description": row[1],
                            "type_chauffage_date_creation": str(time.strftime("%Y-%m-%d", time.localtime())),
                            "type_chauffage_date_modification": str(time.strftime("%Y-%m-%d", time.localtime()))
                        }
                    })
        with open(JSON_FILE_CHAUFFAGE, 'w') as fw:
            fw.write(json.dumps(json_data_dump))

def seed_logement_code_saison():
    """
        Function that will create json file so it can be loaded up
        into the database
    """
    with open(LOGEMENT_CODE_SAISON_FILE, newline='', encoding='latin-1') as csvreader:
        season_code = csv.reader(csvreader, dialect="excel")
        json_data_dump = list()
        for row in season_code:
            if row[2] != '' and row[0] != 'Type':
                json_data_dump.append({
                    "model": "user_interface.LogementCodeSaison",
                    "pk": row[0],
                    "fields":{
                        "logement_code_saison_code_hiver": row[1],
                        "logement_code_saison_code_ete": row[2],
                        "logement_code_saison_date_creation": str(time.strftime('%Y-%m-%d', time.localtime())),
                        "logement_code_saison_date_modification": str(time.strftime("%Y-%m-%d", time.localtime()))
                    }
                })
        with open(JSON_FILE_LOGEMENT_CODE_SAISON, 'w') as fw:
            fw.write(json.dumps(json_data_dump))


def handle_pente_origine_diversite(json_dump, courbe_id, row):
    """
        Function that will add the different slope and origin
        to the new Pente Origin Diversitee model
    """
    nbr_client_possible = [1, 2 ,3 ,4, 5 , 6, 7 ,8 ,9 ,10, 15 , 20,
                           25, 30, 40, 50, 60, 200]
    nbr_client_length = len(nbr_client_possible) + 1
    index = 2
    for client in nbr_client_possible:
        json_dump.append({
            "model": "user_interface.PenteOrigineDeDiversitee",
            "pk": str(uuid.uuid1()),
            "fields": {
                "pente_origine_diversite_nbr_client": client,
                "pente_origine_diversite_m": row[index],
                "pente_origine_diversite_b": row[index + nbr_client_length],
                "courbe_de_diversite_id": courbe_id
            }
        })
        index = index + 1
    return json_dump


def seed_courbe_diversites_and_pente_origin():
    """
        Function that will create a json file from the csv file so it
        can be loaded up into the database
    """
    with open(COURBE_DE_DIVERSITEES_FILE, newline='', encoding='latin-1') as csvreader:
        diversity = csv.reader(csvreader, dialect='excel')
        json_data_dump = list()
        index = 0
        for row in diversity:
            if row[0] == '' or row[0] == 'Type-Superf':
                continue
            else:
                courbe_de_diversite_id = str(uuid.uuid1())
                code_saison_and_superfie = row[0].split(' ')
                code_saison = code_saison_and_superfie[0]
                code_saison = code_saison[ :len(code_saison) -1]
                superficie = code_saison_and_superfie[len(code_saison_and_superfie) - 1]

                json_data_dump.append({
                    "model": "user_interface.CourbeDeDiversitee",
                    "pk": courbe_de_diversite_id,
                    "fields": {
                        "courbe_de_diversite_superficie": superficie,
                        "courbe_de_diversite_code_saison": str(code_saison),
                        "courbe_de_diversite_reprise_m": float(row[1]),
                        "courbe_de_diversite_reprise_b": float(row[20]),
                        "courbe_de_diversite_date_creation": str(time.strftime("%Y-%m-%d", time.localtime())),
                        "courbe_de_diversite_date_modification": str(time.strftime("%Y-%m-%d", time.localtime()))
                    }
                })
                json_data_dump = handle_pente_origine_diversite(json_dump=json_data_dump, courbe_id=courbe_de_diversite_id, row=row)
        with open(JSON_FILE_COURBE_DIVERSITEES, 'w') as fw:
            fw.write(json.dumps(json_data_dump))


def seed_type_logements():
    """
        Method that creates a json file from a csv file
        for the housings
    """
    with open(TYPE_LOGEMENT_FILE, newline='', encoding="latin-1") as csvreader:
        logement_type = csv.reader(csvreader, dialect="excel")
        json_dump_data = list()
        for row in logement_type:
            if row[0] == "Type" or row[0] == '':
                continue
            else:
                json_dump_data.append({
                    'model': 'user_interface.TypeDeLogement',
                    'pk': str(uuid.uuid1()),
                    'fields':{
                        'type_logement_type': row[0],
                        'type_logement_description': "Logement de type : {}".format(row[0]),
                        "type_logement_superficie_habitable_defaut": float(row[1]),
                        "type_logement_date_creation": str(time.strftime('%Y-%m-%d', time.localtime())),
                        "type_logement_date_modification": str(time.strftime("%Y-%m-%d", time.localtime()))
                    }
                })
        with open(JSON_FILE_TYPE_LOGEMENT, 'w') as fw:
            fw.write(json.dumps(json_dump_data))

seed_type_xfo()
seed_type_conductor()
seed_type_chauffage()
seed_logement_code_saison()
seed_courbe_diversites_and_pente_origin()
seed_type_logements()
