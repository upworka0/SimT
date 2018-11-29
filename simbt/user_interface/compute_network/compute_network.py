from user_interface.models import CourbeDeDiversitee, PenteOrigineDeDiversitee, Conducteur, Logement, Noeud, Transformateur, AutreCharge, Admin
from user_interface.compute_network.interpolation import Interpolation
from user_interface.compute_network.logger_configurer import configure_logging, logger
import math
import collections

class ComputeNetwork():
    """
        Class that will compute all information
    """
    configure_logging() # Configure logging statically
    __WINTER_CAPACITY_FACTOR = 2.2


    # Static values used during computing of "Charges", "courant de court circuit", "chute des tensions"
    # TODO: Set those values as instance attributes instead of Static variables
    __CHUTE_V_amont_V_POURCENT = 0
    __NUMBER_PHASE = 0
    __V_OF_PHASE = 0 # TODO: Change name for something that tells more

    __TEMP_AMBIANTE = 0 # In Celcius
    __TEMP_COND = 0 # In Celcius
    __CURRENT = 0
    __CURRENT_ACTIF = 0
    __CURRENT_REACTIF = 0
    __COURT_CIRCUIT_amont = 0
    __CONDUCTEUR_RESISTANCE = 0


    def __init__(self, study=None, admin=None):
        """__init__

            The constructor initialize constant variable and object.
            
            methods that begins with "init" are method designed
            to be used in __init__

            Init : 

        Keyword Arguments:
            study {[Etude]} -- Model object that holds data from the database (default: {None})
            admin {[Admin]} -- Model object that holds data from the database (default: {None})
        """
        self.etude = study
        self.admin = admin
        self.init_compute_z_source() # Required : compute R_SOURCE and X_SOURCE using the voltage of the study
        self.init_factors()
        self.__r_source = admin.admin_r_source
        self.__x_source = admin.admin_x_source
        self.__r_source_amont = 0
        self.__x_source_amont = 0
        self.__TEMP_ARRAY = collections.OrderedDict()
        self.__LOAD_CONDUCTOR_RELATED = collections.OrderedDict()
        self.interpolation = Interpolation()
        self.__instanciate_number_of_phases_phase_tension(study_tension=study.etude_tension)

    def init_factors(self):
        """compute factors
            
            Intanciate power and reactance factors from
            admin model to local variables
        """
        self.__fp_electrique_pointe =  self.admin.admin_fp_electrique_pointe# value expressed in %
        self.__fq_electrique_pointe = self.admin.admin_fq_electrique_pointe # value expressed in % Facteur de Reactance == FR 
        self.__fp_autre_pointe = self.admin.admin_fp_autre_pointe # value expressed in %
        self.__fq_autre_pointe = self.admin.admin_fq_autre_pointe # value expressed in % Facteur de Reactance == FR

        self.__fq_recovery_electrique_pointe = self.admin.admin_fq_recovery_electrique_pointe # value expressed in % Facteur de reactance == FR
        self.__fp_recovery_electrique_pointe = self.admin.admin_fp_recovery_electrique_pointe # value expressed in %
        self.__fq_recovery_autre_pointe = self.admin.admin_fq_recovery_autre_pointe # value expressed in % Facteur de reactance == FR 
        self.__fp_recovery_autre_pointe = self.admin.admin_fp_recovery_autre_pointe # value expressed in %

    
    def init_compute_z_source(self):
        """compute_z_source
        
            This method is going to compute the Z source. 
            
            This computation ends up with admin_r_source & admin_x_source computed 
            and stored in admin object 
        """
        nombre_phase = 3 if self.etude.etude_tension == "347/600" else 2
        v_phase_neutre = 347 if self.etude.etude_tension == "347/600" else 120 
        constant = (math.pow((v_phase_neutre) / (self.admin.admin_ph_ph_mt * 1000), 2)) * 3
        r1_mt = (self.admin.admin_r1_depart_mt + self.admin.admin_r1_cond_mt_a) * (self.etude.etude_distance_ht_mt_aerien + self.admin.admin_r1_cond_mt_s) * self.etude.etude_distance_ht_mt_sout
        x1_mt = (self.admin.admin_x1_depart_mt + self.admin.admin_x1_cond_mt_a) * (self.etude.etude_distance_ht_mt_aerien + self.admin.admin_x1_cond_mt_s) * self.etude.etude_distance_ht_mt_sout
        r0_mt = (self.admin.admin_r0_depart_mt + self.admin.admin_r0_cond_mt_a) * (self.etude.etude_distance_ht_mt_aerien + self.admin.admin_r0_cond_mt_s) * self.etude.etude_distance_ht_mt_sout
        x0_mt = (self.admin.admin_x0_depart_mt + self.admin.admin_x0_cond_mt_a) * (self.etude.etude_distance_ht_mt_aerien + self.admin.admin_x0_cond_mt_s) * self.etude.etude_distance_ht_mt_sout

        if nombre_phase == 3:
            self.admin.admin_r_source = r1_mt
            self.admin.admin_x_source = x1_mt
        else:
            self.admin.admin_r_source = (2 * (r1_mt + r0_mt)) * constant
            self.admin.admin_x_souxce = (2 * (x1_mt + x0_mt)) * constant
        self.admin.save()

    @staticmethod
    def admin_compute_reactance_factor(admin):
        """admin_compute_reactance_factor

            Compute Reactance factor using the Power Factor inputed
            by the user
        
        Arguments:
            admin {Admin} -- [Model for admin, it holds all the constants for computing a study]
        """
        admin.admin_fq_electrique_pointe = math.sqrt(1 - (math.pow(admin.admin_fp_electrique_pointe / 100 , 2))) * 100 
        admin.admin_fq_autre_pointe = math.sqrt(1 - math.pow(admin.admin_fp_autre_pointe / 100, 2)) * 100
        admin.admin_fq_recovery_autre_pointe = admin.admin_fq_autre_pointe
        p_repr_h_chauff_elect = (admin.admin_frepr_ph_chauff_electrique * (admin.admin_fp_electrique_pointe / 100)) 
        q_repr_h_chauff_elect = (admin.admin_frepr_qh_chauff_electrique * (admin.admin_fq_electrique_pointe / 100)) 
        s_reprise_h_chauffage_electrique = math.sqrt(math.pow(p_repr_h_chauff_elect, 2) + math.pow(q_repr_h_chauff_elect, 2))
        admin.admin_fp_recovery_electrique_pointe = (p_repr_h_chauff_elect / s_reprise_h_chauffage_electrique) * 100
        admin.admin_fq_recovery_electrique_pointe = (q_repr_h_chauff_elect / s_reprise_h_chauffage_electrique) * 100
        admin.admin_fq_recovery_autre_pointe = admin.admin_fq_autre_pointe
        admin.save()

    def compute_loads_node(self, logement_id):
        """compute_loads_node

            Parsing network from the load to the Transformer

        :param logement_id:
        """
        temp_array =  []
        component = Logement.objects.filter(nom_du_noeud=logement_id, etude_id=self.etude).get()
        component = self.assign_factors_to_logement(lodging_object=component)
        conductor_array = []
        while component is not None:
            if 'C' in component.nom_du_noeud:
                conductor = Conducteur.objects.filter(nom_du_noeud=component.predecesseur, etude_id=self.etude).get()
                conductor.conducteur_niveau_diversite = conductor.conducteur_niveau_diversite + 1
                component = self.__compute_logement_charge_pointe_ete(lodging_object=component, niveau_diversite=conductor.conducteur_niveau_diversite)
                component = self.__compute_logement_charge_pointe_hiver(lodging_object=component, niveau_diversite=conductor.conducteur_niveau_diversite)
                component = self.__compute_logement_charge_reprise_hiver(lodging_object=component)
                if conductor.conducteur_charge_max_ete_aval < component.logement_charge_pointe_ete:
                    conductor.conducteur_charge_max_ete_aval = component.logement_charge_pointe_ete
                    conductor.conducteur_noeud_charge_ete_max = component.nom_du_noeud

                if conductor.conducteur_charge_max_hiver_aval < component.logement_charge_pointe_hiver:
                    conductor.conducteur_charge_max_hiver_aval = component.logement_charge_pointe_hiver
                    conductor.conducteur_noeud_charge_hiver_max = component.nom_du_noeud
                conductor.save()
                temp_array.append(component.nom_du_noeud)
                conductor_array.append(conductor.nom_du_noeud)
                component = conductor
            elif 'A' in component.nom_du_noeud:
                nom_predecesseur = component.predecesseur
                conductor = None
                if 'N' in nom_predecesseur:
                    node = Noeud.objects.filter(nom_du_noeud=nom_predecesseur, etude_id=self.etude).get()
                    conductor = Conducteur.objects.filter(successeur=node.nom_du_noeud, etude_id=self.etude).get()
                    conductor.conducteur_niveau_diversite = conductor.conducteur_niveau_diversite + 1
                elif 'T' in nom_predecesseur:
                    component = Transformateur.objects.filter(nom_du_noeud=nom_predecesseur, etude_id=self.etude).get()
                    successeur_conductor = Conducteur.objects.filter(nom_du_noeud=component.successeur, etude_id=self.etude).get()
                    if component.transformateur_charge_max_ete_aval < successeur_conductor.conducteur_charge_max_ete_aval:
                        component.transformateur_charge_max_ete_aval = successeur_conductor.conducteur_charge_max_ete_aval
                        component.transformateur_noeud_charge_ete_max = successeur_conductor.conducteur_noeud_charge_ete_max

                    if component.transformateur_charge_max_hiver_aval < successeur_conductor.conducteur_charge_max_hiver_aval:
                        component.transformateur_charge_max_hiver_aval = successeur_conductor.conducteur_charge_max_hiver_aval
                        component.transformateur_noeud_charge_hiver_max = successeur_conductor.conducteur_noeud_charge_hiver_max

                    if component.transformateur_charge_reprise_hiver < successeur_conductor.conducteur_reprise_hiver:
                        component.transformateur_charge_reprise_hiver = successeur_conductor.conducteur_reprise_hiver

                    component.transformateur_niveau_diversite = component.transformateur_niveau_diversite + 1
                    temp_array.append(successeur_conductor.nom_du_noeud)
                    logger.info(msg="\nCharge max Tranfo : \n{}\n".format(component))
                    if component.nom_du_noeud not in self.__TEMP_ARRAY.keys() :
                        self.__TEMP_ARRAY[component.nom_du_noeud] = []
                    self.__TEMP_ARRAY[component.nom_du_noeud].extend(temp_array)

                    self.__LOAD_CONDUCTOR_RELATED[component.nom_du_noeud] = []
                    conductor_array.append(component.nom_du_noeud)
                    component.save()
                    component = None
                    continue

                self.__assign_bigger_load(conductor=conductor, component=component)
                logger.info(msg="\nCharge sur arc 1 :\n {} \n".format(conductor))
                logger.info(msg="\nCharge sur arc 2 :\n {} \n".format(component))
                temp_array.append(component.nom_du_noeud)
                conductor_array.append(conductor.nom_du_noeud)
                conductor.save()
                component.save()
                component = conductor

        conductor_array.sort()
        for conduc in conductor_array:
            if conduc not in self.__LOAD_CONDUCTOR_RELATED.keys():
                self.__LOAD_CONDUCTOR_RELATED[conduc] = []
            self.__LOAD_CONDUCTOR_RELATED[conduc].append(logement_id)
        print(self.__LOAD_CONDUCTOR_RELATED)

    def compute_network(self, transformateur_id):
        """compute_network

        :param transformateur_id: string
        """
        transformateur = Transformateur.objects.filter(nom_du_noeud=transformateur_id, etude_id=self.etude).get()
        self.__TEMP_ARRAY[transformateur_id].sort()
        print("Temp Array : {}".format(self.__TEMP_ARRAY))
        for nom_noeud in self.__TEMP_ARRAY[transformateur_id]:
            if 'C' in nom_noeud:
                self.__compute_network_logement(transformateur=transformateur, conducteur=None, nom_noeud=nom_noeud)
        self.__assign_initial_values_to_conductor()
        self.__compute_network_conducteur()

    def __compute_network_logement(self, transformateur, conducteur, nom_noeud):
        """__compute_network_logement

        :param transformateur: Transformateur object
        :param nom_noeud: String
        """
        logement_found = Logement.objects.filter(nom_du_noeud=nom_noeud, etude_id=self.etude).get()
        charge_repr_hiver_kw = logement_found.logement_charge_reprise_hiver_kw
        charge_repr_hiver_kvar = logement_found.logement_charge_reprise_hiver_kvar
        charge_diversite_ete_kw = None
        charge_diversite_ete_kvar = None
        charge_diversite_hiver_kw = None
        charge_diversite_hiver_kvar = None
        noeud_charge_ete_max = ""
        noeud_charge_hiver_max = ""
        niveau_diversite = 0

        if transformateur is not None:
            noeud_charge_ete_max = transformateur.transformateur_noeud_charge_ete_max
            noeud_charge_hiver_max = transformateur.transformateur_noeud_charge_hiver_max
            niveau_diversite = transformateur.transformateur_niveau_diversite
        elif conducteur is not None:
            noeud_charge_ete_max = conducteur.conducteur_noeud_charge_ete_max
            noeud_charge_hiver_max = conducteur.conducteur_noeud_charge_hiver_max
            niveau_diversite = conducteur.conducteur_niveau_diversite
        #Question : Est-ce que je conserve la charge avec diversite
        if nom_noeud == noeud_charge_ete_max:
            charge_diversite_ete_kvar = logement_found.logement_charge_pointe_ete_kvar
            charge_diversite_ete_kw = logement_found.logement_charge_pointe_ete_kw
        else:
            old_logement = logement_found
            new_lodging = self.__compute_logement_charge_pointe_ete(lodging_object=logement_found, niveau_diversite=niveau_diversite)
            charge_diversite_ete_kvar = new_lodging.logement_charge_pointe_ete_kvar
            charge_diversite_ete_kw = new_lodging.logement_charge_pointe_ete_kw
            #old_logement.save()

        if nom_noeud == noeud_charge_hiver_max:
            charge_diversite_hiver_kvar = logement_found.logement_charge_pointe_hiver_kvar
            charge_diversite_hiver_kw = logement_found.logement_charge_pointe_hiver_kw
        else:
            old_logement = logement_found
            new_lodging = self.__compute_logement_charge_pointe_hiver(lodging_object=logement_found, niveau_diversite=niveau_diversite)
            charge_diversite_hiver_kw = new_lodging.logement_charge_pointe_hiver_kw
            charge_diversite_hiver_kvar = new_lodging.logement_charge_pointe_hiver_kvar
            #old_logement.save()

        if transformateur is not None:
            transformateur = self.add_charge_to_transformateur(transformateur=transformateur, charge_diversite_ete_kvar=charge_diversite_ete_kvar, charge_diversite_ete_kw=charge_diversite_ete_kw,
                                             charge_diversite_hiver_kvar=charge_diversite_hiver_kvar, charge_diversite_hiver_kw=charge_diversite_hiver_kw,
                                             charge_repr_hiver_kvar=charge_repr_hiver_kvar, charge_repr_hiver_kw=charge_repr_hiver_kw)
            self.compute_transformateur_attributes(transformateur=transformateur)
        elif conducteur is not None:
            conducteur = self.add_charge_to_conducteur(conducteur=conducteur, charge_diversite_ete_kvar=charge_diversite_ete_kvar, charge_diversite_ete_kw=charge_diversite_ete_kw,
                                             charge_diversite_hiver_kvar=charge_diversite_hiver_kvar, charge_diversite_hiver_kw=charge_diversite_hiver_kw,
                                             charge_repr_hiver_kvar=charge_repr_hiver_kvar, charge_repr_hiver_kw=charge_repr_hiver_kw)
            self.compute_conducteur_attributes(conducteur=conducteur)

    def __assign_initial_values_to_conductor(self):
        """__assign_initial_values_to_conductor"""
        for key, value in self.__LOAD_CONDUCTOR_RELATED.items():
            if "T" not in key:
                conducteur = Conducteur.objects.filter(nom_du_noeud=key, etude_id=self.etude).get()
                conducteur.conducteur_chute_cummul_v_pourcent = self.__CHUTE_V_amont_V_POURCENT
                conducteur.conducteur_r_source_cummul = self.__r_source_amont
                conducteur.conducteur_x_source_cummul = self.__x_source_amont
                conducteur.save()

    def __compute_network_conducteur(self):
        """__compute_network_conducteur"""
        for key, value in self.__LOAD_CONDUCTOR_RELATED.items():
            if "T" not in key:
                conducteur = Conducteur.objects.filter(nom_du_noeud=key, etude_id=self.etude).get()
                for val in value:
                    self.__compute_network_logement(transformateur=None, conducteur=conducteur, nom_noeud=val)
                    logement = Logement.objects.filter(nom_du_noeud=val, etude_id=self.etude).get()
                    self.__assign_conductor_node_values(conducteur_object=conducteur, logement_object=logement)
                    logger.info("Load values : \n{}\n".format(Logement.objects.filter(nom_du_noeud=val, etude_id=self.etude).get()))
                logger.info("Values of conductor after : {}".format(Conducteur.objects.filter(nom_du_noeud=conducteur.nom_du_noeud, etude_id=self.etude).get()))

    def __assign_conductor_node_values(self, conducteur_object, logement_object):
        """__assign_conductor_node_values

        :param conducteur_object: Conducteur object model
        """
        r_mat = 0
        x_mat = 0
        try:
            r_mat = conducteur_object.type_conducteur_mat_client.mat_client_resistance
            x_mat = conducteur_object.type_conducteur_mat_client.mat_client_reactance
        except AttributeError:
            pass
        logement_object.logement_chute_cumul_v_pourcent = self.__CHUTE_V_amont_V_POURCENT
        logement_object.logement_i_court_circuit = self.__COURT_CIRCUIT_amont
        logement_object.logement_i_court_circuit_client = self.__NUMBER_PHASE / ( math.sqrt( math.pow(self.__r_source_amont + r_mat, 2) + math.pow(self.__x_source_amont + x_mat, 2) ) )
        logement_object.save()

    def compute_conductor_parameters(self, conductor_object):
        """
            See spec conductor type * length
        """
        logger.info("<br /> ****************************************")
        logger.info("  Calcul des attributs du conducteur")
        logger.info("           celon sa longueur")
        logger.info("**************************************** <br />")
        logger.info("Calcul des attributs du conducteur : {} <br />".format(conductor_object))
        self.__computed_conductor = conductor_object
        conductor_length = self.__computed_conductor.longueur
        logger.info("Longueur du conducteur : {} <br />".format(conductor_length))
        self.__computed_conductor.type_conducteur_id.type_conducteur_resistance_par_km = self.__computed_conductor.type_conducteur_id.type_conducteur_resistance_par_km * conductor_length
        logger.info("Resistance par km * longeur : {} * {} = {} <br />".format(conductor_object.type_conducteur_id.type_conducteur_resistance_par_km / conductor_length, conductor_length, self.__computed_conductor.type_conducteur_id.type_conducteur_resistance_par_km))
        self.__computed_conductor.type_conducteur_id.type_conducteur_variation_resistance_par_celcius = self.__computed_conductor.type_conducteur_id.type_conducteur_variation_resistance_par_celcius * conductor_length
        logger.info("Variation resistance par celcius : {} * {} = {} <br />".format(conductor_object.type_conducteur_id.type_conducteur_variation_resistance_par_celcius / conductor_length, conductor_length, self.__computed_conductor.type_conducteur_id.type_conducteur_variation_resistance_par_celcius,))
        self.__computed_conductor.type_conducteur_id.type_conducteur_resistance_par_km_avec_temperature = self.__computed_conductor.type_conducteur_id.type_conducteur_resistance_par_km_avec_temperature  * conductor_length
        logger.info("Resistance par KM avec temperature : {} * {} = {} <br />".format(conductor_object.type_conducteur_id.type_conducteur_resistance_par_km_avec_temperature / conductor_length, conductor_length, self.__computed_conductor.type_conducteur_id.type_conducteur_resistance_par_km_avec_temperature))
        self.__computed_conductor.type_conducteur_id.type_conducteur_courant_admissible = self.__computed_conductor.type_conducteur_id.type_conducteur_courant_admissible * conductor_length
        logger.info("Courant Admissible : {} * {} = {} <br />".format(conductor_object.type_conducteur_id.type_conducteur_courant_admissible / conductor_length, conductor_length, self.__computed_conductor.type_conducteur_id.type_conducteur_courant_admissible))
        self.__computed_conductor.type_conducteur_id.type_conducteur_variation_temp_celon_courant = self.__computed_conductor.type_conducteur_id.type_conducteur_variation_temp_celon_courant * conductor_length
        logger.info("Variation temp celon courant : {} * {} = {} <br />".format(conductor_object.type_conducteur_id.type_conducteur_variation_temp_celon_courant / conductor_length, conductor_length, self.__computed_conductor.type_conducteur_id.type_conducteur_variation_temp_celon_courant))
        self.__computed_conductor.type_conducteur_id.type_conducteur_variation_resistance_celon_courant = self.__computed_conductor.type_conducteur_id.type_conducteur_variation_resistance_celon_courant * conductor_length
        logger.info("Variation resistance celon courant : {} * {} = {} <br />".format(conductor_object.type_conducteur_id.type_conducteur_variation_resistance_celon_courant / conductor_length, conductor_length, self.__computed_conductor.type_conducteur_id.type_conducteur_variation_resistance_celon_courant))
        self.__computed_conductor.type_conducteur_id.type_conducteur_reactance = self.__computed_conductor.type_conducteur_id.type_conducteur_reactance * conductor_length
        logger.info("La reactance: {} * {} = {} <br />".format(conductor_object.type_conducteur_id.type_conducteur_reactance / conductor_length, conductor_length, self.__computed_conductor.type_conducteur_id.type_conducteur_reactance))
        self.__computed_conductor.type_conducteur_id.type_conducteur_capacite_repr_hiver = self.__computed_conductor.type_conducteur_id.type_conducteur_capacite_repr_hiver * conductor_length
        logger.info("Capacite de reprise en hiver : {} * {} = {} <br />".format(conductor_object.type_conducteur_id.type_conducteur_capacite_repr_hiver / conductor_length, conductor_length, self.__computed_conductor.type_conducteur_id.type_conducteur_capacite_repr_hiver))
        self.__computed_conductor.type_conducteur_id.type_conducteur_capacite_planif_ete = self.__computed_conductor.type_conducteur_id.type_conducteur_capacite_planif_ete * conductor_length
        logger.info("Capacite planifier ete: {} * {} = {} <br />".format(conductor_object.type_conducteur_id.type_conducteur_capacite_planif_ete / conductor_length, conductor_length, self.__computed_conductor.type_conducteur_id.type_conducteur_capacite_planif_ete))
        if self.__computed_conductor.type_conducteur_id.type_conducteur_mat_client is not None:
            self.__computed_conductor.type_conducteur_id.type_conducteur_mat_client.mat_client_resistance = self.__computed_conductor.type_conducteur_id.type_conducteur_mat_client.mat_client_resistance * conductor_length
            logger.info("Resistance du mat du client: {} * {} = {} <br />".format(conductor_object.type_conducteur_id.type_conducteur_mat_client.mat_client_resistance / conductor_length, conductor_length, self.__computed_conductor.type_conducteur_id.type_conducteur_mat_client.mat_client_resistance))
            self.__computed_conductor.type_conducteur_id.type_conducteur_mat_client.mat_client_reactance = self.__computed_conductor.type_conducteur_id.type_conducteur_mat_client.mat_client_reactance * conductor_length
            logger.info("Reactance du mat du client: {} * {} = {} <br />".format(conductor_object.type_conducteur_id.type_conducteur_mat_client.mat_client_reactance / conductor_length, conductor_length, self.__computed_conductor.type_conducteur_id.type_conducteur_mat_client.mat_client_reactance))
        return self.__computed_conductor

    def compute_network_recovery_load(self, housing_object, is_winter):
        """
           Compute the load on network reset
           the value returned will expressed
           in kVA
        """
        logger.info("<br />****************************************")
        logger.info("  Calcul de reprise de charge en kVA")
        logger.info("****************************************<br />")
        result = 0
        livable_area = housing_object.surface_habitable
        number_of_housing = housing_object.nombre_de_logement
        logger.info("Surface habitable : {} <br />".format(livable_area))
        logger.info("Nombre de logements : {} <br />".format(number_of_housing))
        if is_winter == True:
            winter_season_code = housing_object.logement_code_saison.logement_code_saison_code_hiver
            logger.info("Code d'hiver : {} <br />".format(winter_season_code))
            result =  self.__compute_reprise_diversite_linear_values(code_saison=winter_season_code,livable_area=lodging_object.surface_habitable) 
            housing_object.logement_charge_reprise_hiver = result
            housing_object.save()
        else:
            summer_season_code = housing_object.logement_code_saison.logement_code_saison_code_ete
            logger.info("Code d'ete : {} <br />".format(summer_season_code))
            result =  self.__compute_reprise_diversite_linear_values(code_saison=summer_season_code,livable_area=lodging_object.surface_habitable)
            housing_object.logement_charge_reprise_ete = result
            housing_object.save()
        return result

    def add_charge_to_transformateur(self, transformateur, charge_diversite_ete_kvar, charge_diversite_ete_kw, charge_diversite_hiver_kvar, charge_diversite_hiver_kw, charge_repr_hiver_kvar, charge_repr_hiver_kw):
        """add_charge_to_transformateur

        :param transformateur: Transformateur object model
        :param charge_diversite_ete_kvar: float
        :param charge_diversite_ete_kw: float
        :param charge_diversite_hiver_kvar: float
        :param charge_diversite_hiver_kw: float
        :param charge_repr_hiver_kvar: float
        :param charge_repr_hiver_kw: float
        """
        self.__add_charge_diversite_ete_kvar_transformateur(transformateur_object=transformateur, noeud_charge_diversite_ete_kvar=charge_diversite_ete_kvar)
        self.__add_charge_diversite_ete_kw_transformateur(transformateur_object=transformateur, noeud_charge_diversite_ete_kw=charge_diversite_ete_kw)
        self.__add_charge_diversite_hiver_kvar_transformateur(transformateur_object=transformateur, noeud_charge_diversite_hiver_kvar=charge_diversite_hiver_kvar)
        self.__add_charge_diversite_hiver_kw_transformateur(transformateur_object=transformateur, noeud_charge_diversite_hiver_kw=charge_diversite_hiver_kw)
        self.__add_charge_reprise_hiver_kvar_transformateur(transformateur_object=transformateur, noeud_charge_reprise_hiver_kvar=charge_repr_hiver_kvar)
        self.__add_charge_reprise_hiver_kw_transformateur(transformateur_object=transformateur, noeud_charge_reprise_hiver_kw=charge_repr_hiver_kw)
        return Transformateur.objects.filter(nom_du_noeud=transformateur.nom_du_noeud, etude_id=self.etude).get()

    def add_charge_to_conducteur(self, conducteur, charge_diversite_ete_kvar, charge_diversite_ete_kw, charge_diversite_hiver_kvar, charge_diversite_hiver_kw, charge_repr_hiver_kvar, charge_repr_hiver_kw):
        """add_charge_to_conducteur

        :param conducteur: Conducteur object model
        :param charge_diversite_ete_kvar: flaot
        :param charge_diversite_kw: float
        :param charge_diversite_hiver_kvar: float
        :param charge_diversite_hiver_kw: float
        :param charge_repr_hiver_kvar: float
        :param charge_repr_hiver_kw: float
        """
        self.__add_charge_diversite_ete_kvar_conducteur(conducteur_object=conducteur, noeud_charge_diversite_ete_kvar=charge_diversite_ete_kvar)
        self.__add_charge_diversite_ete_kw_conducteur(conducteur_object=conducteur, noeud_charge_diversite_ete_kw=charge_diversite_ete_kw)
        self.__add_charge_diversite_hiver_kvar_conducteur(conducteur_object=conducteur, noeud_charge_diversite_hiver_kvar=charge_diversite_hiver_kvar)
        self.__add_charge_diversite_hiver_kw_conducteur(conducteur_object=conducteur, noeud_charge_diversite_hiver_kw=charge_diversite_hiver_kw)
        self.__add_charge_reprise_hiver_kvar_conducteur(conducteur_object=conducteur, noeud_charge_reprise_hiver_kvar=charge_repr_hiver_kvar)
        self.__add_charge_reprise_hiver_kw_conducteur(conducteur_object=conducteur, noeud_charge_reprise_hiver_kw=charge_repr_hiver_kw)
        return Conducteur.objects.filter(nom_du_noeud=conducteur.nom_du_noeud, etude_id=self.etude).get()

    def compute_transformateur_attributes(self, transformateur):
        """compute_transformateur_attribute

        :param transformateur: transformateur
        """
        self.__convert_to_charge_diversite_ete_transformateur(transformateur_object=transformateur)
        self.__convert_to_charge_diversite_hiver_transformateur(transformateur_object=transformateur)
        self.__convert_to_charge_reprise_hiver_transformateur(transformateur_object=transformateur)
        self.__compute_chute_tension_nominale_hiver_transformateur(transformateur_object=transformateur)
        self.__compute_chute_cummulee_tension_hiver_transformateur(transformateur_object=transformateur)
        self.__compute_r_source_amont(transformateur_object=transformateur)
        self.__compute_x_source_amont(transformateur_object=transformateur)
        self.__compute_courant_court_circuit(transformateur_object=transformateur)
        transformateur = Transformateur.objects.filter(nom_du_noeud=transformateur.nom_du_noeud, etude_id=self.etude).get()
        logger.info("*******************************************************\n")
        logger.info(msg="Nouveau Transformateur : {}\n".format(transformateur))
        logger.info("*******************************************************\n")
        return transformateur

    def compute_conducteur_attributes(self, conducteur):
        """compute_conducteur_attributes

        :param conducteur:
        """
        admin = Admin.objects.all().get()
        conducteur = self.__convert_to_charge_diversite_ete_conducteur(conducteur_object=conducteur)
        conducteur = self.__convert_to_charge_diversite_hiver_conducteur(conducteur_object=conducteur)
        conducteur = self.__convert_to_charge_reprise_hiver_conducteur(conducteur_object=conducteur)
        self.__set_global_temperature(conducteur_object=conducteur, admin_object=admin)
        self.__compute_conducteur_current(conducteur_object=conducteur)
        self.__compute_conducteur_resistance(conducteur_object=conducteur, admin_object=admin)
        conducteur = self.__compute_chute_tension_conducteur(conducteur_object=conducteur)
        conducteur = self.__compute_resistance_reactance_conducteur(conducteur_object=conducteur)
        conducteur = self.__compute_court_circuit_conducteur(conducteur_object=conducteur)
        logger.info("*******************************************************\n")
        logger.info(msg="Nouveau Conducteur : {}\n".format(conducteur))
        logger.info("*******************************************************\n")
        return conducteur


    def assign_factors_to_logement(self, lodging_object):
        """assign_factors_to_logement

        :param lodging_object: Logement model
        """
        type_chauffage = lodging_object.type_de_chauffage
        lodging_object.logement_fp_ete = self.__fp_autre_pointe / 100
        lodging_object.logement_fp_hiver = (self.__fp_autre_pointe / 100) if 'a' in type_chauffage.type_chauffage_type else (self.__fp_electrique_pointe / 100)
        lodging_object.logement_fr_ete = math.sqrt(1 - (math.pow(lodging_object.logement_fp_ete, 2))) #TODO Test with SimBT excel document
        lodging_object.logement_fr_hiver = math.sqrt(1 - (math.pow(lodging_object.logement_fp_hiver, 2)))#TODO Test with SimBT excel document
        lodging_object.logement_fp_reprise_hiver = (self.__fp_recovery_autre_pointe / 100) if 'a' in type_chauffage.type_chauffage_type else (self.__fp_recovery_electrique_pointe / 100)
        lodging_object.logement_fr_reprise_hiver = math.sqrt(1 - (math.pow(lodging_object.logement_fp_reprise_hiver, 2))) #TODO Test with SimBT excel document
        lodging_object.save()
        logger.info("*******************************************************\n")
        logger.info(msg="Nouvel objet apres assignation \n Logement :{}".format(lodging_object))
        logger.info("*******************************************************\n")
        return lodging_object

    def compute_recovery_factor(self,): #TODO Change the way this method work (is_winter might be useless)
        """compute_recovery_factor

            Compute recovery factor using
            both peak "FQ" and "FP" using
            the following formula :

            square_root((2*FP)^2 + (1.3*FQ)^2)

        :param heating_is_electric: boolean
        :param is_winter: boolean
        :return result : float
        """
        logger.info("<br />****************************************")
        logger.info("     Calcul du facteur de reprise") #TODO make sure what value I am computing
        logger.info("****************************************<br />")
        result = 0
        if heating_is_electric:
            if is_winter :
                result = self.___compute_recovery_factor(power_factor=self.__fp_electrique_pointe , reactance_factor=self.__fq_electrique_pointe)
            else:
                result = self.__compute_recovery_factor(power_factor=self.__fp_autre_pointe, reactance_factor=self.__fq_autre_pointe)
        else:
            if is_winter :
                result = self.__compute_recovery_factor(power_factor=self.__fp_autre_pointe, reactance_factor=self.__fq_autre_pointe)
            else:
                result = self.__compute_recovery_factor(power_factor=self.__fp_autre_pointe, reactance_factor=self.__fq_autre_pointe)
                return result

            lodging_object = self.__compute_logement_charge_pointe_hiver(lodging_object=lodging_object, niveau_diversite=conductor.conducteur_niveau_diversite)
            lodging_object = self.__compute_logement_charge_reprise_hiver(lodging_object=lodging_object)
            conductor.conducteur_charge_max_ete_aval = lodging_object.logement_charge_pointe_ete
            conductor.conducteur_charge_max_hiver_aval = lodging_object.logement_charge_pointe_hiver
            conductor.conducteur_noeud_charge_ete_max = lodging_object.nom_du_noeud
            conductor.conducteur_noeud_charge_hiver_max = lodging_object.nom_du_noeud
            conductor.save()
            return conductor

    def __assign_bigger_load(self, conductor, component):
            """__assign_bigger_load

            :param conductor:
            :param component:
            """
            if conductor.conducteur_charge_max_ete_aval < component.conducteur_charge_max_ete_aval:
               conductor.conducteur_charge_max_ete_aval = component.conducteur_charge_max_ete_aval
               conductor.conducteur_noeud_charge_ete_max = component.conducteur_noeud_charge_ete_max

            if conductor.conducteur_charge_max_hiver_aval < component.conducteur_charge_max_hiver_aval:
               conductor.conducteur_charge_max_hiver_aval = component.conducteur_charge_max_hiver_aval
               conductor.conducteur_noeud_charge_hiver_max = component.conducteur_noeud_charge_hiver_max

            conductor.save()
            return conductor
    def __instanciate_number_of_phases_phase_tension(self, study_tension):
        """__instanciate_number_phase_phase_tension

        :param study_tension: String i.e 120/240
        """
        if study_tension == "120/240":
            self.__NUMBER_PHASE = 2
            self.__V_OF_PHASE = 120
        elif study_tension == "120/208":
            self.__NUMBER_PHASE = 3
            self.__V_OF_PHASE = 120
        elif study_tension == "348/600":
            self.__NUMBER_PHASE = 3
            self.__V_OF_PHASE = 348

    def __compute_xfo_capacity(self, capacity, is_winter):
            """
                Compute capacity of a tranformer
                Capacity * capacity factor (2.2 in winter)
            """
            result = 0
            if is_winter:
                result = capacity * self.__WINTER_CAPACITY_FACTOR
                logger.info(msg="La capacite en hiver = capacite * facteur de capacite en hiver = {} * {} = {} <br />".format(capacity, self.__WINTER_CAPACITY_FACTOR, result))
            else:
                result = capacity
                logger.info(msg="La capacitee en ete = xfo_capacite = {} <br />".format(capacity))
            return result

    def __fetch_courbe_de_diversite_reprise(self, season_code, livable_area):
            """
                Retrieve "Courbe de diversite" from the data received
            """
            if(CourbeDeDiversitee.objects.filter(courbe_de_diversite_code_saison=season_code, courbe_de_diversite_superficie=livable_area).exists()):
               return CourbeDeDiversitee.objects.filter(courbe_de_diversite_code_saison=season_code, courbe_de_diversite_superficie=livable_area).order_by("courbe_de_diversite_superficie").get()
            else :
                begin_object = CourbeDeDiversitee.objects.filter(courbe_de_diversite_code_saison=season_code, courbe_de_diversite_superficie__lt=livable_area).order_by("courbe_de_diversite_superficie")[0:1].get()
                end_object = CourbeDeDiversitee.objects.filter(courbe_de_diversite_code_saison=season_code, courbe_de_diversite_superficie__gt=livable_area).order_by("courbe_de_diversite_superficie")[0:1].get()
                new_courbe_de_diversite = self.interpolation.compute_linear_interpolation(begin_object=begin_object, end_object=end_object, area_needed=livable_area)
                return new_courbe_de_diversite

    def __fetch_courbe_de_diversite(self, season_code, livable_area, niveau_diversite):
            """__fetch_courbe_de_diversite

            :param season_code:
            :param livable_area:
            :param niveau_diversite:
            """
            courbe_de_diversite = self.__fetch_courbe_de_diversite_reprise(season_code=season_code, livable_area=livable_area)
            if PenteOrigineDeDiversitee.objects.filter(courbe_de_diversite_id=courbe_de_diversite.courbe_de_diversite_id, pente_origine_diversite_nbr_client=niveau_diversite).exists():
                return PenteOrigineDeDiversitee.objects.filter(courbe_de_diversite_id=courbe_de_diversite.courbe_de_diversite_id, pente_origine_diversite_nbr_client=niveau_diversite).order_by('pente_origine_diversite_nbr_client').get()
            else:
                begin_object = CourbeDeDiversitee.objects.filter(courbe_de_diversite_code_saison=season_code, courbe_de_diversite_superficie__lt=livable_area).order_by("courbe_de_diversite_superficie")[0:1].get()
                end_object = CourbeDeDiversitee.objects.filter(courbe_de_diversite_code_saison=season_code, courbe_de_diversite_superficie__gt=livable_area).order_by("courbe_de_diversite_superficie")[0:1].get()
                new_pente = self.interpolation.compute_linear_interpolation_niveau_diversite(begin_object=begin_object, end_object=end_object, niveau_diversite=niveau_diversite, area_needed=livable_area)
                pente = self.interpolation.save_pente_origine(array=new_pente, courbe_diversite=courbe_de_diversite)
                return pente

    def __compute_reprise_diversite_linear_values(self, code_saison, livable_area):
            """__compute_reprise_diversite_linear_values

            :param code_saison: str
            :return result
            """
            diversity_slope_recovery = self.__fetch_courbe_de_diversite_reprise(season_code=code_saison, livable_area=livable_area)
            logger.info("Pente et Origine de reprise en hiver : m={}, b={} <br />".format(diversity_slope_recovery.courbe_de_diversite_reprise_m, diversity_slope_recovery.courbe_de_diversite_reprise_b))
            recovery_computing = diversity_slope_recovery.courbe_de_diversite_reprise_m * livable_area
            logger.info("m * sh : {} * {} = {} <br />".format(diversity_slope_recovery.courbe_de_diversite_reprise_m, livable_area, recovery_computing))
            recovery_computing = recovery_computing + diversity_slope_recovery.courbe_de_diversite_reprise_b
            logger.info("resultat ulterieur + b : {} + {} = {} <br />".format(recovery_computing - diversity_slope_recovery.courbe_de_diversite_reprise_b,
                                                                       diversity_slope_recovery.courbe_de_diversite_reprise_b,
                                                                       recovery_computing
                                                                             ))
            result = recovery_computing #* number_of_housing

            return result

    def __compute_diversite_linear_value(self, code_saison, livable_area, niveau_diversite):
            """__compute_diversite_linear_value

            :param code_saison:
            :param niveau_diversite:
            """
            diversity_slope_recovery = self.__fetch_courbe_de_diversite_reprise(season_code=code_saison, livable_area=livable_area)
            diversity_slope = self.__fetch_courbe_de_diversite(season_code=code_saison, livable_area=livable_area, niveau_diversite=niveau_diversite)
            diversity_computing = diversity_slope.pente_origine_diversite_m * livable_area
            diversity_computing = diversity_computing + diversity_slope.pente_origine_diversite_b
            return diversity_computing

    def __compute_facteur_reprise(self, power_factor, reactance_factor):
            """__compute_facteur_reprise
            :param power_factor:
            :param reactance_factor:
            """
            result = math.pow(2 * (power_factor / 100), 2)
            logger.info("(2 * FP%)^2 : ({} * {})^ 2 = {}<br />".format(2, power_factor, result))
            result = result + (math.pow(1.3 * (power_factor/100), 2))
            logger.info("result + (1.3 * FQ%)^2: (1.3 * {})^2 + resultat anterieur = {}<br />".format(reactance_factor, result))
            result = math.sqrt(result)
            return result

    def __compute_logement_charge_pointe_ete(self, lodging_object, niveau_diversite): 
        """__compute_charge_pointe_ete compute kVA, KW and KVAR during summer
        :param lodging_object:
        :param niveau_diversite:
        """
        livable_area = lodging_object.surface_habitable
        summer_season_code = lodging_object.logement_code_saison.logement_code_saison_code_ete
        lodging_object.logement_charge_pointe_ete = self.__compute_diversite_linear_value(code_saison=summer_season_code, livable_area=livable_area, niveau_diversite=niveau_diversite)
        lodging_object = self.__compute_logement_charge_pointe_ete_kw(lodging_object=lodging_object)
        lodging_object = self.__compute_logement_charge_pointe_ete_kvar(lodging_object=lodging_object)
        lodging_object.save()
        logger.info("*******************************************************\n")
        logger.info(msg="Logement apres charge pointe ete \n Logement : {}\n".format(lodging_object))
        logger.info("*******************************************************\n")
        return lodging_object

    def __compute_logement_charge_pointe_ete_kw(self, lodging_object):
            """__compute_charge_pointe_ete_kw

              charge_diversite en ete = (M * Superficie + B) * FP_E (Du logement AKA la charge)
              Must have computed the "logement_charge_pointe_ete" first
            :param logding_object: Object Logement
            """
            power_factor_summer = lodging_object.logement_fp_ete
            lodging_object.logement_charge_pointe_ete_kw = lodging_object.logement_charge_pointe_ete * power_factor_summer
            return lodging_object

    def __compute_logement_charge_pointe_ete_kvar(self, lodging_object):
            """__compute_charge_pointe_ete_kvar

              charge_diversite en ete = (M * Superficie + B) * FR_E (Du logement AKA la charge)
              Must have computed the "logement_charge_pointe_ete" first
            :param lodging_object:
            """
            reactance_factor_summer = lodging_object.logement_fr_ete
            lodging_object.logement_charge_pointe_ete_kvar = lodging_object.logement_charge_pointe_ete * reactance_factor_summer
            return lodging_object

    def __compute_logement_charge_pointe_hiver(self, lodging_object, niveau_diversite):
            """__compute_charge_pointe_hiver

            :param lodging_object:
            :param niveau_diversite:
            """
            livable_area = lodging_object.surface_habitable
            winter_season_code = lodging_object.logement_code_saison.logement_code_saison_code_hiver
            lodging_object.logement_charge_pointe_hiver = self.__compute_diversite_linear_value(code_saison=winter_season_code, livable_area=livable_area, niveau_diversite=niveau_diversite)
            lodging_object = self.__compute_logement_charge_pointe_hiver_kw(lodging_object=lodging_object)
            lodging_object = self.__compute_logement_charge_pointe_hiver_kvar(lodging_object=lodging_object)
            lodging_object.save()
            logger.info("*******************************************************\n")
            logger.info(msg="Logement apres charge pointe hiver \n Logement : {}\n".format(lodging_object))
            logger.info("*******************************************************\n")
            return lodging_object

    def __compute_logement_charge_pointe_hiver_kw(self, lodging_object):
            """__compute_charge_pointe_hiver_kw

              charge_diversite en ete = (M * Superficie + B) * FP_E (Du logement AKA la charge)
            :param lodging_object:
            """
            power_factor_winter = lodging_object.logement_fp_hiver
            lodging_object.logement_charge_pointe_hiver_kw = lodging_object.logement_charge_pointe_hiver * power_factor_winter
            return lodging_object

    def __compute_logement_charge_pointe_hiver_kvar(self, lodging_object):
            """__compute_charge_pointe_hiver_kvar

              charge_diversite en_hiver = (M * Superficie + B) * FR_E (Du logement AKA la charge)
            :param lodging_object:
            """
            reactance_factor_winter = lodging_object.logement_fr_hiver
            lodging_object.logement_charge_pointe_hiver_kvar = lodging_object.logement_charge_pointe_hiver * reactance_factor_winter
            return lodging_object

    def __compute_logement_charge_reprise_hiver(self, lodging_object):
            """__compute_logement_charge_reprise_hiver

            :param lodging_object:
            """
            livable_area  = lodging_object.surface_habitable
            winter_season_code = lodging_object.logement_code_saison.logement_code_saison_code_hiver
            lodging_object.logement_charge_reprise_hiver = self.__compute_reprise_diversite_linear_values(code_saison=winter_season_code, livable_area=livable_area)
            lodging_object = self.__compute_logement_charge_reprise_hiver_kw(lodging_object=lodging_object)
            lodging_object = self.__compute_logement_charge_reprise_hiver_kvar(lodging_object=lodging_object)
            lodging_object.save()
            logger.info("*******************************************************\n")
            logger.info(msg="Logement apres charge reprise hiver \n Logement : {}\n".format(lodging_object))
            logger.info("*******************************************************\n")
            return lodging_object

    def __compute_logement_charge_reprise_hiver_kw(self, lodging_object):
        """__compute_logement_charge_reprise_hiver_kw

        :param lodging_object:
        """
        power_factor_recovery_winter = lodging_object.logement_fp_reprise_hiver
        lodging_object.logement_charge_reprise_hiver_kw = lodging_object.logement_charge_reprise_hiver * power_factor_recovery_winter
        return lodging_object

    def __compute_logement_charge_reprise_hiver_kvar(self, lodging_object):
        """__compute_logement_charge_reprise_hiver_kvar

        :param lodging_object:
        """
        reactance_factor_recovery_winter = lodging_object.logement_fr_reprise_hiver
        lodging_object.logement_charge_reprise_hiver_kvar = lodging_object.logement_charge_reprise_hiver * reactance_factor_recovery_winter
        return lodging_object

    def __add_charge_diversite_ete_kw_transformateur(self, transformateur_object, noeud_charge_diversite_ete_kw):
        """__add_charge_diversite_ete_kw_transformateur

        :param transformateur_object:
        :param noeud_charge_diversite_ete_kw:
        """
        transformateur_object.transformateur_charge_diversite_ete_kw = transformateur_object.transformateur_charge_diversite_ete_kw + noeud_charge_diversite_ete_kw
        transformateur_object.save()

    def __add_charge_diversite_ete_kvar_transformateur(self, transformateur_object, noeud_charge_diversite_ete_kvar):
        """__add_charge_diversite_ete_kvar_transformateur

        :param transformateur_object:
        :param noeud_charge_diversite_ete_kvar:
        """
        transformateur_object.transformateur_charge_diversite_ete_kvar = transformateur_object.transformateur_charge_diversite_ete_kvar + noeud_charge_diversite_ete_kvar
        transformateur_object.save()

    def __add_charge_diversite_hiver_kw_transformateur(self, transformateur_object, noeud_charge_diversite_hiver_kw):
        """__add_charge_diversite_hiver_kw_transformateur

        :param transformateur_object:
        :param noeud_charge_diversite_hiver_kw:
        """
        transformateur_object.transformateur_charge_diversite_hiver_kw = transformateur_object.transformateur_charge_diversite_hiver_kw + noeud_charge_diversite_hiver_kw
        transformateur_object.save()

    def __add_charge_diversite_hiver_kvar_transformateur(self, transformateur_object, noeud_charge_diversite_hiver_kvar):
        """__add_charge_diversite_hiver_kvar_transformateur

        :param transformateur_object:
        :param noeud_charge_diversite_hiver_kvar:
        """
        transformateur_object.transformateur_charge_diversite_hiver_kvar = transformateur_object.transformateur_charge_diversite_hiver_kvar + noeud_charge_diversite_hiver_kvar
        transformateur_object.save()

    def __add_charge_reprise_hiver_kw_transformateur(self, transformateur_object, noeud_charge_reprise_hiver_kw):
        """__add_charge_reprise_hiver_kw_transformateur

        :param transformateur_object:
        :param noeud_charge_reprise_hiver_kw:
        """
        transformateur_object.transformateur_charge_reprise_hiver_kw = transformateur_object.transformateur_charge_reprise_hiver_kw + noeud_charge_reprise_hiver_kw
        transformateur_object.save()

    def __add_charge_reprise_hiver_kvar_transformateur(self, transformateur_object, noeud_charge_reprise_hiver_kvar):
        """__add_charge_reprise_hiver_kvar_transformateur

        :param transformateur_object:
        :param noeud_charge_reprise_hiver_kvar:
        """
        transformateur_object.transformateur_charge_reprise_hiver_kvar = transformateur_object.transformateur_charge_reprise_hiver_kvar + noeud_charge_reprise_hiver_kvar
        transformateur_object.save()

    def __add_charge_diversite_ete_kw_conducteur(self, conducteur_object, noeud_charge_diversite_ete_kw):
        """__add_charge_diversite_ete_kw_conducteur

        :param conducteur_object:
        :param noeud_charge_diversite_ete_kw:
        """
        conducteur_object.conducteur_charge_diversite_ete_kw = conducteur_object.conducteur_charge_diversite_ete_kw + noeud_charge_diversite_ete_kw
        conducteur_object.save()

    def __add_charge_diversite_ete_kvar_conducteur(self, conducteur_object, noeud_charge_diversite_ete_kvar):
        """__add_charge_diversite_ete_kvar_conducteur

        :param conducteur_object:
        :param noeud_charge_diversite_ete_kvar:
        """
        conducteur_object.conducteur_charge_diversite_ete_kvar = conducteur_object.conducteur_charge_diversite_ete_kvar + noeud_charge_diversite_ete_kvar
        conducteur_object.save()

    def __add_charge_diversite_hiver_kw_conducteur(self, conducteur_object, noeud_charge_diversite_hiver_kw):
        """__add_charge_diversite_hiver_kw_conducteur

        :param conducteur_object:
        :param noeud_charge_diversite_hiver_kw:
        """
        conducteur_object.conducteur_charge_diversite_hiver_kw = conducteur_object.conducteur_charge_diversite_hiver_kw + noeud_charge_diversite_hiver_kw
        conducteur_object.save()

    def __add_charge_diversite_hiver_kvar_conducteur(self, conducteur_object, noeud_charge_diversite_hiver_kvar):
        """__add_charge_diversite_hiver_kvar_conducteur

        :param conducteur_object:
        :param noeud_charge_diversite_hiver_kvar:
        """
        conducteur_object.conducteur_charge_diversite_hiver_kvar = conducteur_object.conducteur_charge_diversite_hiver_kvar + noeud_charge_diversite_hiver_kvar
        conducteur_object.save()

    def __add_charge_reprise_hiver_kvar_conducteur(self, conducteur_object, noeud_charge_reprise_hiver_kvar):
        """__add_charge_reprise_hiver_kvar_conducteur

        :param conducteur_object:
        :param noeud_charge_reprise_hiver_kvar:
        """
        conducteur_object.conducteur_reprise_hiver_kvar = conducteur_object.conducteur_reprise_hiver_kvar + noeud_charge_reprise_hiver_kvar
        conducteur_object.save()

    def __add_charge_reprise_hiver_kw_conducteur(self, conducteur_object, noeud_charge_reprise_hiver_kw):
        """__add_charge_reprise_hiver_kw_conducteur

        :param conducteur_object:
        :param noeud_charge_reprise_hiver_kw:
        """
        conducteur_object.conducteur_reprise_hiver_kw = conducteur_object.conducteur_reprise_hiver_kw + noeud_charge_reprise_hiver_kw
        conducteur_object.save()

    def __convert_to_charge_diversite_ete_transformateur(self, transformateur_object):
        """__convert_to_charge_diversite_ete_kva_transformateur

        :param transformateur_object:
        """
        transformateur_object.transformateur_charge_diversite_ete = math.sqrt(
                                                                                math.pow(transformateur_object.transformateur_charge_diversite_ete_kw, 2) +
                                                                                math.pow(transformateur_object.transformateur_charge_diversite_ete_kvar, 2)
                                                                             )
        transformateur_object.save()

    def __convert_to_charge_diversite_hiver_transformateur(self, transformateur_object):
        """__convert_to_charge_diversite_hiver_kva_transformateur

        :param transformateur_object:
        """
        transformateur_object.transformateur_charge_diversite_hiver = math.sqrt(
                                                                                math.pow(transformateur_object.transformateur_charge_diversite_hiver_kw, 2) +
                                                                                math.pow(transformateur_object.transformateur_charge_diversite_hiver_kvar, 2)
                                                                             )
        transformateur_object.save()

    def __convert_to_charge_reprise_hiver_transformateur(self, transformateur_object):
        """__convert_to_charge_reprise_hiver_kva_transformateur

        :param transformateur_object:
        """
        transformateur_object.transformateur_charge_reprise_hiver = math.sqrt(
                                                                                math.pow(transformateur_object.transformateur_charge_reprise_hiver_kw, 2) +
                                                                                math.pow(transformateur_object.transformateur_charge_reprise_hiver_kvar, 2)
                                                                            )
        transformateur_object.save()

    def __convert_to_charge_diversite_ete_conducteur(self, conducteur_object):
        """__convert_to_charge_diversite_ete_conducteur

        :param conducteur_object:
        """
        conducteur_object.conducteur_charge_diversite_ete = math.sqrt(
                                                                                math.pow(conducteur_object.conducteur_charge_diversite_ete_kw, 2) +
                                                                                math.pow(conducteur_object.conducteur_charge_diversite_ete_kvar, 2)
                                                                             )
        conducteur_object.save()
        return conducteur_object

    def __convert_to_charge_diversite_hiver_conducteur(self, conducteur_object):
        """__convert_to_charge_diversite_hiver_conducteur

        :param conducteur_object:
        """
        conducteur_object.conducteur_charge_diversite_hiver = math.sqrt(
                                                                          math.pow(conducteur_object.conducteur_charge_diversite_hiver_kw, 2) +
                                                                          math.pow(conducteur_object.conducteur_charge_diversite_hiver_kvar, 2)
                                                                       )
        conducteur_object.save()
        return conducteur_object

    def __convert_to_charge_reprise_hiver_conducteur(self, conducteur_object):
        """__convert_to_charge_reprise_hiver_conducteur

        :param conducteur_object:
        """
        conducteur_object.conducteur_reprise_hiver = math.sqrt(
                                                                 math.pow(conducteur_object.conducteur_reprise_hiver_kw, 2) +
                                                                 math.pow(conducteur_object.conducteur_reprise_hiver_kvar, 2)
                                                              )
        conducteur_object.save()
        return conducteur_object

    def __set_global_temperature(self, conducteur_object, admin_object):
        """__set_global_temperature

        :param conducteur_object:
        """
        if conducteur_object.conducteur_sout is True:
            self.__TEMP_AMBIANTE = admin_object.admin_temp_ambiante_pte_s
            self.__TEMP_COND = admin_object.admin_temp_cond_pte_s
        else:
            self.__TEMP_AMBIANTE = admin_object.admin_temp_ambiante_pte_a
            self.__TEMP_COND = admin_object.admin_temp_cond_pte_a

    def __compute_conducteur_current(self, conducteur_object):
        """__compute_conducteur_current

        :param conducteur_object: Conducteur object
        """
        phase_tension_product = (self.__NUMBER_PHASE * self.__V_OF_PHASE)
        self.__CURRENT = conducteur_object.conducteur_charge_diversite_hiver / phase_tension_product
        self.__CURRENT_ACTIF = conducteur_object.conducteur_charge_diversite_hiver_kw / phase_tension_product
        self.__CURRENT_REACTIF = conducteur_object.conducteur_charge_diversite_hiver_kvar / phase_tension_product

    def __compute_conducteur_resistance(self, conducteur_object, admin_object):
        """__compute_conducteur_resistance
            IF TEMP FIXE :
                R = (ARC.[R25] + ARC.[Del_R_T] x (Temp_cond – 25) / 1000) x [Longueur] / 1000
            ELSE :
                R = (ARC.[R25] + (ARC.[Del_R_T] x (Temp_amb – 25) +  ARC.[Del_R_I2] x I2 ) / 1000) x ARC.[Longueur] / 1
        :param conducteur_object:
        :param admin_object:
        """
        if admin_object.admin_r_temp_fixe is True:
            r_25 = conducteur_object.type_conducteur_id.type_conducteur_resistance_par_km_avec_temperature
            del_r_t = conducteur_object.type_conducteur_id.type_conducteur_variation_resistance_par_celcius
            self.__CONDUCTEUR_RESISTANCE = (r_25 + del_r_t * (self.__TEMP_COND - 25) / 1000) * (conducteur_object.longueur /1000)
        else:
            self.__CONDUCTEUR_RESISTANCE = (conducteur_object.type_conducteur_id.type_conducteur_resistance_par_km_avec_temperature + (conducteur_object.type_conducteur_id.type_conducteur_variation_resistance_par_celcius * (self.__TEMP_AMBIANTE - 25) + conducteur_object.type_conducteur_id.type_conducteur_variation_resistance_celon_courant * math.pow(self.__CURRENT, 2)) / 1000) * (conducteur_object.longueur / 1000)
            print("Resistance du conducteur : {} -> {}".format(conducteur_object.nom_du_noeud, self.__CONDUCTEUR_RESISTANCE))

    def __compute_chute_tension_conducteur(self, conducteur_object):
        """__compute_chute_tension_conducteur

        :param conducteur_object: Conducteur object model
        :return conducteur_object : Edited Conducteur object model
        """
        conducteur_object.conducteur_chute_loc_v_pourcent = ((self.__CONDUCTEUR_RESISTANCE * self.__CURRENT_ACTIF) + (conducteur_object.type_conducteur_id.type_conducteur_reactance * self.__CURRENT_REACTIF)) / self.__NUMBER_PHASE
        conducteur_object.conducteur_chute_cummul_v_pourcent = conducteur_object.conducteur_chute_cummul_v_pourcent + conducteur_object.conducteur_chute_loc_v_pourcent
        conducteur_object.save()
        return conducteur_object

    def __compute_resistance_reactance_conducteur(self, conducteur_object):
        """__compute_resistance_reactance_conducteur

        :param conducteur_object: Conducteur Object model
        """
        conducteur_object.conducteur_r_source_cummul = conducteur_object.conducteur_r_source_cummul + (self.__CONDUCTEUR_RESISTANCE * 0.9)
        conducteur_object.conducteur_x_source_cummul = conducteur_object.conducteur_x_source_cummul + (conducteur_object.type_conducteur_id.type_conducteur_resistance_par_km * (conducteur_object.longueur / 1000))
        print("Nom du conducteur : {}".format(conducteur_object.nom_du_noeud))
        print("R source cummul : {}".format(conducteur_object.conducteur_r_source_cummul))
        print("X Source cummul : {}".format(conducteur_object.conducteur_x_source_cummul))
        self.__r_source_amont = conducteur_object.conducteur_r_source_cummul
        self.__x_source_amont = conducteur_object.conducteur_x_source_cummul
        conducteur_object.save()
        return conducteur_object

    def __compute_court_circuit_conducteur(self, conducteur_object):
        """__compute_court_circuit_conducteur

        :param conducteur_object:
        """
        print("R source : {}".format(self.__r_source))
        print("X Source : {}".format(self.__x_source))
        conducteur_object.conducteur_i_court_circuit = self.__NUMBER_PHASE /(math.sqrt(math.pow(self.__r_source_amont, 2) + math.pow(self.__x_source_amont, 2)))
        self.__COURT_CIRCUIT_amont = conducteur_object.conducteur_i_court_circuit
        conducteur_object.save()
        return conducteur_object


    def __compute_chute_tension_nominale_hiver_transformateur(self, transformateur_object):
        """__compute_chute_tension_nominale_hiver_transformateur

        :param transformateur_object:
        """
        reactance_pourcent = transformateur_object.type_de_transformateur.type_transformateur_reactance_pourcent / 100
        resistance_pourcent = transformateur_object.type_de_transformateur.type_transformateur_resistance_pourcent / 100
        capacitee = transformateur_object.type_de_transformateur.type_transformateur_capacite
        transformateur_object.transformateur_chute_loc_v_pourcent = (resistance_pourcent * transformateur_object.transformateur_charge_diversite_hiver_kw
        + reactance_pourcent * transformateur_object.transformateur_charge_diversite_hiver_kvar) / capacitee
        transformateur_object.save()

    def __compute_chute_cummulee_tension_hiver_transformateur(self, transformateur_object):
        """__compute_chute_cummulee_tension_hiver_transformateur

        :param transformateur_object:
        """
        transformateur_object.transformateur_chute_cummul_v_pourcent = transformateur_object.transformateur_chute_loc_v_pourcent
        transformateur_object.save()

    def __compute_r_source_amont(self, transformateur_object):
        """__compute_r_source_amont

        :param transfomer_object: Transformateur Object model
        :param global_parameters:
        """
        self.__r_source_amont = (transformateur_object.type_de_transformateur.type_transformateur_resistance_pourcent / 100) * math.pow(self.__NUMBER_PHASE, 2) / (transformateur_object.type_de_transformateur.type_transformateur_capacite / self.__V_OF_PHASE) + self.__r_source

    def __compute_x_source_amont(self, transformateur_object):
        """__compute_x_source_amont

        :param transformateur_object:
        """
        self.__x_source_amont = (transformateur_object.type_de_transformateur.type_transformateur_reactance_pourcent / 100)* math.pow(self.__NUMBER_PHASE, 2) / (transformateur_object.type_de_transformateur.type_transformateur_capacite / self.__V_OF_PHASE) + self.__x_source

    def __compute_courant_court_circuit(self, transformateur_object):
        """__courant_court_circuit

        :param transformateur_object:
        """
        print("Nombre de phase : {}".format(self.__NUMBER_PHASE))
        print("R Source amont {}: {}".format(transformateur_object.nom_du_noeud, self.__r_source_amont))
        print("X Source amont {}: {}".format(transformateur_object.nom_du_noeud, self.__x_source_amont))
        print("".format())
        transformateur_object.transformateur_i_court_circuit = self.__NUMBER_PHASE / math.sqrt(math.pow(self.__r_source_amont, 2) + math.pow(self.__x_source_amont, 2))
        transformateur_object.save()

