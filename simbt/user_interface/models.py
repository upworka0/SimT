from django.db import models
from django.contrib.auth.models import User
import uuid
import datetime

class Company(models.Model):
    """Company

        This represenet a company that would be added
        to the database so they can have an admin and users

        An admin or a user can only work at one company so
        it is a 1 to 1 relationship

        TODO: Fully implement it with User and Admin
        TODO: Complete fields
        TODO: Create method __str__ to make it easier to debug data

    Arguments:
        models {[type]} -- [description]
    """
    company_id = models.UUIDField(primary_key=True, default=uuid.uuid1())
    company_name = models.CharField(max_length=50)


class Admin(models.Model):
    """Admin

        Admin to user, Not to be mixed with Super User

    Arguments:
        models {[type]} -- [description]
    """

    admin_id = models.UUIDField(primary_key=True, default=uuid.uuid1())
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #TODO: Once ready, remove blank=True and null=True
    company = models.OneToOneField("user_interface.Company", on_delete=models.CASCADE, null=True, blank=True)
    admin_cout_pertes_puissance = models.FloatField(default=120.00)
    admin_cout_pertes_energie = models.FloatField(default=7.7)
    admin_r_temp_fixe = models.BooleanField(default=True)
    admin_temp_ambiante_pte_a = models.FloatField(default=-25.0)
    admin_temp_ambiante_pte_s = models.FloatField(default=4.0)
    admin_temp_cond_pte_a = models.FloatField(default=30.4)
    admin_temp_cond_pte_s = models.FloatField(default=90.0)
    admin_fp_electrique_pointe = models.FloatField(default=99.5) # Expressed in %
    admin_fq_electrique_pointe = models.FloatField(default=9.99) # Expressed in %
    admin_fp_autre_pointe = models.FloatField(default=95.0) # Expressed in %
    admin_fq_autre_pointe = models.FloatField(default=31.224989991992) # Expressed in %
    admin_fq_recovery_electrique_pointe = models.FloatField(default=6.51064950150825) # Expressed in % 
    admin_fp_recovery_electrique_pointe = models.FloatField(default=99.7878321393371) # Expressed in %
    admin_fq_recovery_autre_pointe = models.FloatField(default=31.224989991992) # Expressed in %
    admin_fp_recovery_autre_pointe = models.FloatField(default=95.0) # Expressed in %
    admin_frepr_ph_chauff_electrique = models.FloatField(default=2.0) # Need to define what this is
    admin_frepr_qh_chauff_electrique = models.FloatField(default=1.3) # Need to define what this is
    admin_r_source = models.FloatField(default = 0)
    admin_x_source = models.FloatField(default = 0)
    admin_r1_depart_mt = models.FloatField(default = 0.0537)
    admin_x1_depart_mt = models.FloatField(default = 1.324)
    admin_r0_depart_mt = models.FloatField(default = 0.0953)
    admin_x0_depart_mt = models.FloatField(default = 3.8125)
    admin_r1_cond_mt_a = models.FloatField(default = 0.104)
    admin_x1_cond_mt_a = models.FloatField(default = 0.395)
    admin_r0_cond_mt_a = models.FloatField(default = 0.357)
    admin_x0_cond_mt_a = models.FloatField(default = 1.313)
    admin_r1_cond_mt_s = models.FloatField(default = 0.098)
    admin_x1_cond_mt_s = models.FloatField(default = 0.247)
    admin_r0_cond_mt_s = models.FloatField(default = 0.392)
    admin_x0_cond_mt_s = models.FloatField(default = 0.107)
    admin_ph_ph_mt = models.FloatField(default = 24.94) # Tension phase-phase du réseau MT en kV; Tension phase-neutre /= phase-phase

    def __str__(self):
        return "{}".format(self.user) 

class Client(models.Model):
    """
        Model that represents the client
    """
    CHUTE_TENSION_UNITE =(
        ("%", "pourcent"),
        ("120", "base_de_120"),
    )

    CHARGE_UNITE = (
        ("kVA", "kilo_volt_ampere"),
        ("A", "ampere"),
        )


    COURANT_COURT_CIRCUIT = (
         ("%", "pourcent"),
        ("kA", "kilo_ampere"),
     )

    SUPERFICIE_UNITE = (
        ("m^2", "metre_carre"),
        ("p^2", "pied_carre"),
    )

    client_id = models.UUIDField(primary_key=True, default=uuid.uuid1())
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    #TODO: Once ready, remove blank=True and null=True
    company = models.OneToOneField("user_interface.Company", on_delete=models.CASCADE, null=True, blank=True)
    client_nom_projeteur = models.CharField(max_length=75, null=True)
    client_nom_approbateur = models.CharField(max_length=75, null=True)
    client_chute_tension_unite = models.CharField(max_length=15, choices=CHUTE_TENSION_UNITE, default='120')
    client_charge_unite = models.CharField(max_length=15, choices=CHARGE_UNITE, default='kVA')
    client_courant_court_circuit_unite = models.CharField(max_length=15, choices=COURANT_COURT_CIRCUIT, default="%")
    client_superficie_unite = models.CharField(max_length=25, choices=SUPERFICIE_UNITE, default="m^2")
    client_temperature_ambiante_pointe_sout_defaut = models.FloatField(default=4.0)
    client_temperature_ambiante_pointe_aerien_defaut = models.FloatField(default=-25.0)
    client_temperature_conducteur_pointe_sout_defaut = models.FloatField(default=90.0)
    client_temperature_conducteur_pointe_aerien_defaut = models.FloatField(default=30.4)
    client_circuit_constant_defaut = models.BooleanField(default=False)
    client_last_login = models.DateTimeField(blank=True, null=True)
    client_date_creation = models.DateField(auto_now_add=True)
    client_date_modification = models.DateField(auto_now=True)

    def __str__(self):
        return "{} - {} - {} - {} - {} - {} - {} - {} - {} - {} -{} - {} - {} - {}".format(
                                                                                            self.client_id,
                                                                                            self.client_nom_projeteur,
                                                                                            self.client_nom_approbateur,
                                                                                            self.client_chute_tension_unite,
                                                                                            self.client_charge_unite,
                                                                                            self.client_courant_court_circuit_unite,
                                                                                            self.client_superficie_unite,
                                                                                            self.client_temperature_ambiante_pointe_sout_defaut,
                                                                                            self.client_temperature_ambiante_pointe_aerien_defaut,
                                                                                            self.client_temperature_conducteur_pointe_sout_defaut,
                                                                                            self.client_temperature_conducteur_pointe_aerien_defaut,
                                                                                            self.client_circuit_constant_defaut,
                                                                                            self.client_date_creation,
                                                                                            self.client_date_modification
                                                                                          )

class Etude(models.Model):
    """
        Model that reprensent that hold the studies
        and all the componenet related to it
    """

    etude_id = models.UUIDField(primary_key=True, default=uuid.uuid1())
    etude_nom = models.CharField(max_length=250)
    etude_description = models.CharField(max_length=500, null=True, blank=True)
    etude_tension = models.CharField(max_length=10, default="120/240")
    etude_temperature_ambiante_pointe_sout = models.FloatField() # Value that come from the Client model
    etude_temperature_ambiante_pointe_aerien = models.FloatField() # Value that come from the Client model
    etude_conducteur_pointe_sout = models.FloatField()  # Value that come from the Client Model
    etude_conducteur_pointe_aerien = models.FloatField()    #Value that come from the Client Model
    etude_distance_ht_mt_sout = models.FloatField(default=0)
    etude_distance_ht_mt_aerien = models.FloatField(default=0)
    etude_cap_rupture_boitier_client = models.FloatField(default=10.00)
    etude_tension_mt_accru = models.BooleanField(default=False) # Indique si le réseau étudié est situé dans une zone où la tension en MT est plus élevée au sens de la norme A.41-01
    etude_perte_puissance_pointe_dollar_kW = models.DecimalField(max_digits=65, decimal_places=2, default=0.00)
    etude_perte_energie_hors_pointe_Wh = models.FloatField(default=0.00)
    etude_date_creation = models.DateField(auto_now_add=True)
    etude_date_modification = models.DateField(auto_now=True)
    clients_etudes = models.ManyToManyField(Client)
    etude_serialized_visual = models.TextField(null=True, blank=True)
    etude_component_list = models.TextField(null=True, blank=True)

    def __str__(self):
        return "{} - {} - {} - {} - {} - {} - {} - {} - {} - {} -{} - {} - {} - {} - {} - {} - {}".format(
                                                                                                            self.etude_id,
                                                                                                            self.etude_nom,
                                                                                                            self.etude_description,
                                                                                                            self.etude_temperature_ambiante_pointe_sout,
                                                                                                            self.etude_temperature_ambiante_pointe_aerien,
                                                                                                            self.etude_conducteur_pointe_sout,
                                                                                                            self.etude_conducteur_pointe_aerien,
                                                                                                            self.etude_distance_ht_mt_sout,
                                                                                                            self.etude_distance_ht_mt_aerien,
                                                                                                            self.etude_cap_rupture_boitier_client,
                                                                                                            self.etude_tension,
                                                                                                            self.etude_tension_mt_accru,
                                                                                                            self.etude_perte_puissance_pointe_dollar_kW,
                                                                                                            self.etude_perte_energie_hors_pointe_Wh,
                                                                                                            self.etude_date_creation,
                                                                                                            self.etude_date_modification,
                                                                                                            self.clients_etudes
                                                                                                         )

class TypeDeChauffage(models.Model):
    """
        Model that represent the
        type of heating units for a
        building
    """
    type_chauffage_id = models.UUIDField(primary_key=True, default=uuid.uuid1())
    type_chauffage_type = models.CharField(max_length=35)
    type_chauffage_description = models.CharField(max_length=150)
    type_chauffage_date_creation = models.DateField(auto_now_add=True)
    type_chauffage_date_modification = models.DateField(auto_now=True)

    def __str__(self):
        return "{} - {} - {} - {} - {}".format(
                                                self.type_chauffage_id,
                                                self.type_chauffage_type,
                                                self.type_chauffage_description,
                                                self.type_chauffage_date_creation,
                                                self.type_chauffage_date_modification
                                              )

class TypeDeConducteur(models.Model):
    """
        Model that represents the type of
        cable conductor used to link a charge
        to the rest of the network
    """

    TYPE_TENSION = (
        (0, "120V/240V"),
        (1, "120V/208V & 347V/600V")
    )

    type_conducteur_id = models.UUIDField(primary_key=True, default=uuid.uuid1())
    type_conducteur_tension = models.IntegerField(choices=TYPE_TENSION)
    type_conducteur_type = models.CharField(max_length=35)
    type_conducteur_description = models.CharField(max_length=150)
    type_conducteur_est_aerien = models.BooleanField()
    type_conducteur_resistance_par_km = models.FloatField()
    type_conducteur_variation_resistance_par_celcius = models.FloatField()
    type_conducteur_resistance_par_km_avec_temperature = models.FloatField()
    type_conducteur_courant_admissible = models.FloatField()
    type_conducteur_variation_temp_celon_courant = models.FloatField()
    type_conducteur_variation_resistance_celon_courant = models.FloatField()
    type_conducteur_reactance = models.FloatField()
    type_conducteur_capacite_repr_hiver = models.FloatField()
    type_conducteur_capacite_planif_ete = models.FloatField()
    type_conducteur_mat_client = models.ForeignKey('user_interface.MatClient', blank=True, null=True, on_delete=models.PROTECT)
    type_conducteur_date_creation = models.DateField(auto_now_add=True)
    type_conducteur_date_modification = models.DateField(auto_now=True)

    def __str__(self):
        return "{} - {} - {} - {} - {} - {} - {} - {} - {} - {} -{} - {} - {} - {} - {} - {} - {}".format(
                                                                                                            self.type_conducteur_id,
                                                                                                            self.type_conducteur_tension,
                                                                                                            self.type_conducteur_type,
                                                                                                            self.type_conducteur_description,
                                                                                                            self.type_conducteur_est_aerien,
                                                                                                            self.type_conducteur_resistance_par_km,
                                                                                                            self.type_conducteur_variation_resistance_par_celcius,
                                                                                                            self.type_conducteur_resistance_par_km_avec_temperature,
                                                                                                            self.type_conducteur_courant_admissible,
                                                                                                            self.type_conducteur_variation_temp_celon_courant,
                                                                                                            self.type_conducteur_variation_resistance_celon_courant,
                                                                                                            self.type_conducteur_reactance,
                                                                                                            self.type_conducteur_capacite_repr_hiver,
                                                                                                            self.type_conducteur_capacite_planif_ete,
                                                                                                            self.type_conducteur_mat_client,
                                                                                                            self.type_conducteur_date_creation,
                                                                                                            self.type_conducteur_date_modification
                                                                                                         )

class MatClient(models.Model):
    """
       Model that will hold information related to pole
    """
    mat_client_id = models.CharField(primary_key=True, max_length=25)
    mat_client_resistance = models.FloatField()
    mat_client_reactance = models.FloatField()

    def __str__(self):
        return "{} - {} - {}".format(
                                        self.mat_client_id,
                                        self.mat_client_resistance,
                                        self.mat_client_reactance
                                    )

class LogementCodeSaison(models.Model):
    """
        Model that represents
    """
    logement_code_saison_type = models.CharField(primary_key=True, max_length=10)
    logement_code_saison_code_hiver = models.CharField(max_length=15)
    logement_code_saison_code_ete = models.CharField(max_length=15)
    logement_code_saison_date_creation = models.DateField(auto_now=True)
    logement_code_saison_date_modification = models.DateField(auto_now_add=True)

    def __str__(self):
        return "{} - {} - {} - {} - {}".format(
                                                self.logement_code_saison_type,
                                                self.logement_code_saison_code_hiver,
                                                self.logement_code_saison_code_ete,
                                                self.logement_code_saison_date_creation,
                                                self.logement_code_saison_date_modification
                                              )
class TypeDeLogement(models.Model):
    """
        Model that represents a lodging building
    """
    type_logement_id = models.UUIDField(primary_key=True, default=uuid.uuid1())
    type_logement_type = models.CharField(max_length=35)
    type_logement_description = models.CharField(max_length=150)
    type_logement_superficie_habitable_defaut = models.FloatField()
    type_logement_date_creation = models.DateField(auto_now_add=True)
    type_logement_date_modification = models.DateField(auto_now=True)

    def __str__(self):
        return "{} - {} - {} - {} - {} -{}".format(
                                                    self.type_logement_id,
                                                    self.type_logement_type,
                                                    self.type_logement_description,
                                                    self.type_logement_superficie_habitable_defaut,
                                                    self.type_logement_date_creation,
                                                    self.type_logement_date_modification
                                                  )
class TypeDeTransformateur(models.Model):
     """
         Model that represents the type of transformer
     """

     TYPE_TENSION = (
         (0, "120V/240V"),
         (1, "120V/208V"),
         (2, "347V/600V")
     )
     type_transformateur_id = models.UUIDField(primary_key=True, default=uuid.uuid1())
     type_transformateur_tension = models.IntegerField(choices=TYPE_TENSION)
     type_transformateur_type = models.CharField(max_length=35)
     type_transformateur_description = models.CharField(max_length=150)
     type_transformateur_capacite = models.FloatField()
     type_transformateur_resistance_pourcent = models.FloatField()
     type_transformateur_reactance_pourcent = models.FloatField()
     type_transformateur_perte_a_vide_pourcent = models.FloatField()
     type_transformateur_est_aerien = models.BooleanField(default=False)
     type_transformateur_date_creation = models.DateField(auto_now_add=True)
     type_transformateur_date_modification = models.DateField(auto_now=True)

     def __str__(self):
         model_string = "ID {type_transformateur_id}\nTension {type_transformateur_tension}\nType {type_transformateur_type}\nCapacite {type_transformateur_capacite}\nResistance % {type_transformateur_resistance_pourcent}\nReactance % {type_transformateur_reactance_pourcent}\nPerte a vide % {type_transformateur_perte_a_vide_pourcent}\nEst aerien {type_transformateur_est_aerien}"
         return model_string.format(type_transformateur_id = self.type_transformateur_id,
                                    type_transformateur_tension = self.type_transformateur_tension,
                                    type_transformateur_type = self.type_transformateur_type,
                                    type_transformateur_capacite = self.type_transformateur_capacite,
                                    type_transformateur_resistance_pourcent = self.type_transformateur_resistance_pourcent,
                                    type_transformateur_reactance_pourcent = self.type_transformateur_reactance_pourcent,
                                    type_transformateur_perte_a_vide_pourcent = self.type_transformateur_perte_a_vide_pourcent,
                                    type_transformateur_est_aerien = self.type_transformateur_est_aerien
                                   )

class Conducteur(models.Model):
     """
         Model that represents a conductor
         in a study
     """
     conducteur_id = models.UUIDField(primary_key=True, default=uuid.uuid1())
     etude_id = models.ForeignKey('user_interface.Etude', on_delete=models.CASCADE)
     type_conducteur_id = models.ForeignKey('user_interface.TypeDeConducteur', on_delete=models.PROTECT)
     nom_du_noeud = models.CharField(max_length=25)
     noeud_alias = models.CharField(max_length=50)
     longueur = models.FloatField()
     position_x = models.FloatField()
     position_y = models.FloatField()
     predecesseur = models.CharField(max_length=25)
     successeur = models.CharField(max_length=25)
     conducteur_sout = models.BooleanField(default=False) # underground conductor
     conducteur_charge_diversite_ete = models.FloatField(default=0) # Calculé par le logiciel  lors de la routine de calcul : Racine([Charge_divers_E_kW]^2 + [Charge_divers_E_kvar]^2)
     conducteur_charge_diversite_ete_kvar = models.FloatField(default=0)
     conducteur_charge_diversite_ete_kw = models.FloatField(default=0)
     conducteur_charge_diversite_hiver = models.FloatField(default=0)
     conducteur_charge_diversite_hiver_kvar = models.FloatField(default=0)
     conducteur_charge_diversite_hiver_kw = models.FloatField(default=0)
     conducteur_charge_max_ete_aval = models.FloatField(default=0)
     conducteur_charge_max_hiver_aval = models.FloatField(default=0)
     conducteur_reprise_hiver = models.FloatField(default=0)
     conducteur_reprise_hiver_kvar = models.FloatField(default=0)
     conducteur_reprise_hiver_kw = models.FloatField(default=0)
     conducteur_chute_cummul_v_pourcent = models.FloatField(default=0)
     conducteur_chute_loc_v_pourcent = models.FloatField(default=0)
     conducteur_couleur = models.CharField(max_length=10, default="grey")
     conducteur_i_court_circuit = models.FloatField(default=0)
     #conducteur_liste_neoud_charge = models.CharField() #It would be an array (Not sure if it is necessary)
     conducteur_niveau_diversite = models.FloatField(default=0) # Nombre de clients désservis par cet arc
     conducteur_noeud_charge_ete_max = models.CharField(max_length=10, blank=True, null=True) # Name of the node that is the biggest in summer
     conducteur_noeud_charge_hiver_max = models.CharField(max_length=10, blank=True, null=True) # Name of the node that is the biggest in winter
     conducteur_r_source_cummul = models.FloatField(default=0)
     conducteur_x_source_cummul = models.FloatField(default=0)
     conducteur_network = models.IntegerField(default=0)
     conducteur_source = models.IntegerField(blank=True, null=True)
     conducteur_status = models.CharField(max_length=25, default="creating")
     conducteur_date_creation = models.DateField(auto_now_add=True)
     conducteur_date_modifier = models.DateField(auto_now=True)

     def __str__(self):
         model_string = "ID : {conducteur_id},\n Etude : {etude_id},\n Type : {type_conducteur},\n Nom du noeud : {nom_du_noeud},\nCharge diversite Ete : {conducteur_charge_diversite_ete},\n Charge diversite Ete kvar: {conducteur_charge_diversite_ete_kvar},\nCharge diversite Ete KW : {conducteur_charge_diversite_ete_kw},\n Charge diversite Hiver: {conducteur_charge_diversite_hiver},\nCharge diversite Hiver kvar : {conducteur_charge_diversite_hiver_kvar},\n Charge diversite Hiver kw: {conducteur_charge_diversite_hiver_kw},\nCharge Reprise Hiver : {conducteur_reprise_hiver},\n Charge Reprise Hiver kvar: {conducteur_reprise_hiver_kvar},\nCharge Reprise Hiver kw : {conducteur_reprise_hiver_kw},\n Chute Cummul V Pourcent: {conducteur_chute_cummul_v_pourcent},\nChute Loc V Pourcent : {conducteur_chute_loc_v_pourcent},\n Courant Court Circuit: {conducteur_i_court_circuit},\nNiveau de Diversite : {conducteur_niveau_diversite},\n R source cummul: {conducteur_r_source_cummul},\nX source cummul : {conducteur_x_source_cummul},\n Charge ete max : {conducteur_noeud_charge_ete_max},\nCharge Hiver max : {conducteur_noeud_charge_hiver_max},\n"
         return model_string.format(conducteur_id = self.conducteur_id,
                                    etude_id = self.etude_id,
                                    type_conducteur = self.type_conducteur_id,
                                    nom_du_noeud = self.nom_du_noeud,
                                    longueur = self.longueur,
                                    position_x= self.position_x,
                                    position_y= self.position_y,
                                    predecesseur= self.predecesseur,
                                    successeur= self.successeur,
                                    conducteur_sout= self.conducteur_sout,
                                    conducteur_charge_diversite_ete= self.conducteur_charge_diversite_ete,
                                    conducteur_charge_diversite_ete_kvar= self.conducteur_charge_diversite_ete_kvar,
                                    conducteur_charge_diversite_ete_kw= self.conducteur_charge_diversite_ete_kw,
                                    conducteur_charge_diversite_hiver= self.conducteur_charge_diversite_hiver,
                                    conducteur_charge_diversite_hiver_kvar= self.conducteur_charge_diversite_hiver_kvar,
                                    conducteur_charge_diversite_hiver_kw= self.conducteur_charge_diversite_hiver_kw,
                                    conducteur_reprise_hiver= self.conducteur_reprise_hiver,
                                    conducteur_reprise_hiver_kvar= self.conducteur_reprise_hiver_kvar,
                                    conducteur_reprise_hiver_kw= self.conducteur_reprise_hiver_kw,
                                    conducteur_chute_cummul_v_pourcent= self.conducteur_chute_cummul_v_pourcent,
                                    conducteur_chute_loc_v_pourcent = self.conducteur_chute_loc_v_pourcent,
                                    conducteur_couleur= self.conducteur_couleur,
                                    conducteur_i_court_circuit= self.conducteur_i_court_circuit,
                                    conducteur_niveau_diversite= self.conducteur_niveau_diversite,
                                    conducteur_noeud_charge_ete_max= self.conducteur_noeud_charge_ete_max,
                                    conducteur_noeud_charge_hiver_max= self.conducteur_noeud_charge_hiver_max,
                                    conducteur_r_source_cummul= self.conducteur_r_source_cummul,
                                    conducteur_x_source_cummul= self.conducteur_x_source_cummul,
                                    conducteur_network= self.conducteur_network,
                                    conducteur_source= self.conducteur_source,
                                    conducteur_status= self.conducteur_status
                                   )

class Noeud(models.Model):
    """
        Model that represents a node
    """
    noeud_id = models.UUIDField(primary_key=True, default=uuid.uuid1())
    etude_id = models.ForeignKey('user_interface.Etude', on_delete=models.CASCADE)
    nom_du_noeud = models.CharField(max_length=25)
    noeud_alias = models.CharField(max_length=50)
    noeud_cummul_V_pourcent = models.FloatField(blank=True, null=True)
    noeud_couleur = models.CharField(max_length=10, default="grey")
    noeud_i_court_circuit = models.FloatField(blank=True, null=True)
    noeud_connected = models.BooleanField(default=False)
    noeud_network = models.IntegerField(blank=True, null=True)
    noeud_status = models.CharField(max_length=25, default="creating")
    position_x = models.FloatField()
    position_y = models.FloatField()
    predecesseur = models.CharField(max_length=25)
    successeur = models.CharField(max_length=25)
    noeud_date_creation = models.DateField(auto_now_add=True)
    noeud_date_modifier = models.DateField(auto_now=True)

    def __str__(self):
        return "{} - {} - {} - {} - {} - {} - {} - {} - {} - {} ".format(
                                                                            self.noeud_id,
                                                                            self.noeud_cummul_V_pourcent,
                                                                            self.noeud_couleur,
                                                                            self.noeud_i_court_circuit,
                                                                            self.nom_du_noeud,
                                                                            self.noeud_connected,
                                                                            self.noeud_network,
                                                                            self.noeud_status,
                                                                            self.noeud_date_creation,
                                                                            self.noeud_date_modifier
                                                                        )

class Logement(models.Model):
    """
        Model that represents a housing
    """
    logement_id = models.UUIDField(primary_key=True, default=uuid.uuid1())
    etude_id = models.ForeignKey('user_interface.Etude', on_delete=models.CASCADE)
    type_de_logement = models.ForeignKey('user_interface.TypeDeLogement', on_delete=models.PROTECT)
    type_de_chauffage = models.ForeignKey('user_interface.TypeDeChauffage', on_delete=models.PROTECT)
    logement_code_saison = models.ForeignKey('user_interface.LogementCodeSaison', on_delete=models.PROTECT, null=True, blank=True, default=None)
    nom_du_noeud = models.CharField(max_length=25)
    noeud_alias = models.CharField(max_length=50)
    logement_raccorde = models.BooleanField(default=False)
    logement_charge_pointe_ete = models.FloatField(blank=True, null=True)
    logement_charge_pointe_ete_kvar = models.FloatField(blank=True, null=True)
    logement_charge_pointe_ete_kw = models.FloatField(blank=True, null=True)
    logement_charge_pointe_hiver = models.FloatField(blank=True, null=True)
    logement_charge_pointe_hiver_kvar = models.FloatField(blank=True, null=True)
    logement_charge_pointe_hiver_kw = models.FloatField(blank=True, null=True)
    logement_charge_reprise_hiver = models.FloatField(blank=True, null=True)
    logement_charge_reprise_hiver_kvar = models.FloatField(blank=True, null=True)
    logement_charge_reprise_hiver_kw = models.FloatField(blank=True, null=True)
    logement_chute_cummul_v_pourcent = models.FloatField(blank=True, null=True)
    logement_couleur = models.CharField(max_length=25, default="grey")
    logement_fp_ete = models.FloatField(default=0)
    logement_fp_hiver = models.FloatField(default=0)
    logement_fp_reprise_hiver = models.FloatField(default=0)
    logement_fr_ete = models.FloatField(default=0)
    logement_fr_reprise_hiver = models.FloatField(default=0)
    logement_i_court_circuit = models.FloatField(blank=True, null=True)
    logement_i_court_circuit_client = models.FloatField(blank=True, null=True)
    logement_fr_hiver = models.FloatField(default=0)
    logement_network = models.IntegerField(blank=True, null=True)
    surface_habitable = models.FloatField()
    nombre_etage = models.IntegerField()
    nombre_de_logement = models.IntegerField()
    position_x = models.FloatField()
    position_y = models.FloatField()
    predecesseur = models.CharField(max_length=25)
    successeur = models.CharField(max_length=25)
    logement_date_creation = models.DateField(auto_now_add=True)
    logement_date_modification = models.DateField(auto_now=True)

    def __str__(self):
        model_string = "ID: {logement_id},\nEtude: {etude_id},\nType : {type_de_logement},\nChauffage: {type_de_chauffage},\nCode Saison: {logement_code_saison},\nNom noeud: {nom_du_noeud},\nCharge Pointe ete: {logement_charge_pointe_ete},\nCharge Pointe ete kvar: {logement_charge_pointe_ete_kvar},\nCharge pointe ete kw: {logement_charge_pointe_ete_kw},\nCharge pointe hiver: {logement_charge_pointe_hiver},\nCharge pointe hiver kvar: {logement_charge_pointe_hiver_kvar},\nCharge pointe hiver kw: {logement_charge_pointe_hiver_kw},\nCharge Reprise hiver: {logement_charge_reprise_hiver},\nCharge reprise hiver kvar: {logement_charge_reprise_hiver_kvar},\nCharge reprise hiver kw: {logement_charge_reprise_hiver_kw},\nChute cummul V pourcent: {logement_chute_cumul_v_pourcent},\nFacteur de puissance Ete: {logement_fp_ete},\nFacteur puissance hiver: {logement_fp_hiver},\nFacteur de puissance reprise hiver: {logement_fp_reprise_hiver},\nFacteur de reactance ete: {logement_fr_ete},\nFacteur de reactance hiver: {logement_fr_hiver},\nFacteur de reactance hiver reprise: {logement_fr_reprise_hiver},\nCourant court circuit: {logement_i_court_circuit},\nCourant court circuit client: {logement_i_court_circuit_client},\nSuccesseur: {successeur},\nPredecesseur: {predecesseur}"
        return model_string.format(
                                    logement_id = self.logement_id,
                                    etude_id = self.etude_id,
                                    type_de_logement = self.type_de_logement,
                                    type_de_chauffage = self.type_de_chauffage,
                                    logement_code_saison = self.logement_code_saison,
                                    nom_du_noeud = self.nom_du_noeud,
                                    logement_charge_pointe_ete = self.logement_charge_pointe_ete,
                                    logement_charge_pointe_ete_kvar = self.logement_charge_pointe_ete_kvar,
                                    logement_charge_pointe_ete_kw = self.logement_charge_pointe_ete_kw,
                                    logement_charge_pointe_hiver = self.logement_charge_pointe_hiver,
                                    logement_charge_pointe_hiver_kvar = self.logement_charge_pointe_hiver_kvar,
                                    logement_charge_pointe_hiver_kw = self.logement_charge_pointe_hiver_kw,
                                    logement_charge_reprise_hiver = self.logement_charge_reprise_hiver,
                                    logement_charge_reprise_hiver_kvar = self.logement_charge_reprise_hiver_kvar,
                                    logement_charge_reprise_hiver_kw = self.logement_charge_reprise_hiver_kw,
                                    logement_fp_ete = self.logement_fp_ete,
                                    logement_fp_hiver = self.logement_fp_hiver,
                                    logement_fp_reprise_hiver = self.logement_fp_reprise_hiver,
                                    logement_fr_ete = self.logement_fr_ete,
                                    logement_fr_hiver = self.logement_fr_hiver,
                                    logement_fr_reprise_hiver = self.logement_fr_reprise_hiver,
                                    logement_i_court_circuit = self.logement_i_court_circuit,
                                    logement_i_court_circuit_client = self.logement_i_court_circuit_client,
                                    successeur = self.successeur,
                                    predecesseur = self.predecesseur,
                                    logement_chute_cumul_v_pourcent = self.logement_chute_cummul_v_pourcent
                               )

class Transformateur(models.Model):
    """
        Model that represents the tranformer in a network
    """
    transformateur_id = models.UUIDField(primary_key=True, default=uuid.uuid1())
    etude_id = models.ForeignKey('user_interface.Etude', on_delete=models.CASCADE)
    type_de_transformateur = models.ForeignKey("user_interface.TypeDeTransformateur", on_delete=models.PROTECT)
    nom_du_noeud = models.CharField(max_length=25)
    noeud_alias = models.CharField(max_length=50)
    position_x = models.FloatField()
    position_y = models.FloatField()
    successeur = models.CharField(max_length=25)
    predecesseur = models.CharField(max_length=25)
    transformateur_charge_diversite_ete = models.FloatField(default=0)
    transformateur_charge_diversite_ete_kvar = models.FloatField(default=0)
    transformateur_charge_diversite_ete_kw = models.FloatField(default=0)
    transformateur_charge_diversite_hiver = models.FloatField(default=0)
    transformateur_charge_diversite_hiver_kvar = models.FloatField(default=0)
    transformateur_charge_diversite_hiver_kw = models.FloatField(default=0)
    transformateur_charge_max_ete_aval = models.FloatField(default=0)
    transformateur_charge_max_hiver_aval = models.FloatField(default=0)
    transformateur_charge_reprise_hiver = models.FloatField(default=0)
    transformateur_charge_reprise_hiver_kvar = models.FloatField(default=0)
    transformateur_charge_reprise_hiver_kw = models.FloatField(default=0)
    transformateur_chute_cummul_v_pourcent = models.FloatField(blank=True, null=True)
    transformateur_chute_loc_v_pourcent = models.FloatField(blank=True, null=True)
    transformateur_i_court_circuit = models.FloatField(blank=True, null=True)
    transformateur_niveau_diversite = models.FloatField(default=0) # nombre de client desservis par ce transfo
    transformateur_noeud_charge_ete_max = models.CharField(max_length=10,blank=True, null=True)
    transformateur_noeud_charge_hiver_max = models.CharField(max_length=10,blank=True, null=True)
    transformateur_network = models.IntegerField(default=0)
    transformateur_date_creation = models.DateField(auto_now_add=True)
    transformateur_date_modification = models.DateField(auto_now=True)


    def __str__(self):
        model_string = "ID : {transformateur_id},\nEtude: {etude_id},\nType: {type_de_transformateur},\nNom du noeud: {nom_du_noeud},\nCharge Diversite ete: {transformateur_charge_diversite_ete},\nCharge Diversite ete kvar: {transformateur_charge_diversite_ete_kvar},\nCharge Diversite ete kw: {transformateur_charge_diversite_ete_kw},\nCharge diversite hiver: {transformateur_charge_diversite_hiver},\nCharge diversite hiver kvar: {transformateur_charge_diversite_hiver_kvar},\nCharge diversite hiver kw: {transformateur_charge_diversite_hiver_kw},\nCharge reprise: {transformateur_charge_reprise_hiver},\nCharge reprise kvar: {transformateur_charge_reprise_hiver_kvar},\nCharge Reprise kw: {transformateur_charge_reprise_hiver_kw},\nChute cummul V pourcent: {transformateur_chute_cummul_v_pourcent},\nChute loc V pourcent: {transformateur_chute_loc_v_pourcent},\nCourant court circuit: {transformateur_i_court_circuit},\nNiveau Diversite: {transformateur_niveau_diversite},\nCharge ete max: {transformateur_noeud_charge_ete_max},\nCharge hiver max: {transformateur_noeud_charge_hiver_max},\nSuccesseur: {successeur},\nPredecesseur: {predecesseur}"
        return model_string.format(
                                    transformateur_id=self.transformateur_id,
                                    etude_id=self.etude_id,
                                    type_de_transformateur=self.type_de_transformateur,
                                    nom_du_noeud=self.nom_du_noeud,
                                    transformateur_charge_diversite_ete = self.transformateur_charge_diversite_ete,
                                    transformateur_charge_diversite_ete_kvar = self.transformateur_charge_diversite_ete_kvar,
                                    transformateur_charge_diversite_ete_kw = self.transformateur_charge_diversite_ete_kw,
                                    transformateur_charge_diversite_hiver = self.transformateur_charge_diversite_hiver,
                                    transformateur_charge_diversite_hiver_kvar = self.transformateur_charge_diversite_hiver_kvar,
                                    transformateur_charge_diversite_hiver_kw = self.transformateur_charge_diversite_hiver_kw,
                                    transformateur_charge_reprise_hiver = self.transformateur_charge_reprise_hiver,
                                    transformateur_charge_reprise_hiver_kvar = self.transformateur_charge_reprise_hiver_kvar,
                                    transformateur_charge_reprise_hiver_kw = self.transformateur_charge_reprise_hiver_kw,
                                    transformateur_chute_cummul_v_pourcent = self.transformateur_chute_cummul_v_pourcent,
                                    transformateur_chute_loc_v_pourcent = self.transformateur_chute_loc_v_pourcent,
                                    transformateur_i_court_circuit = self.transformateur_i_court_circuit,
                                    transformateur_niveau_diversite = self.transformateur_niveau_diversite,
                                    transformateur_noeud_charge_ete_max = self.transformateur_noeud_charge_ete_max,
                                    transformateur_noeud_charge_hiver_max = self.transformateur_noeud_charge_hiver_max,
                                    predecesseur = self.predecesseur,
                                    successeur = self.successeur
                                 )

class CourbeDeDiversitee(models.Model):
    """
        Model that represents the diversity curve
    """
    courbe_de_diversite_id = models.UUIDField(primary_key=True, default=uuid.uuid1())
    courbe_de_diversite_superficie = models.IntegerField()
    courbe_de_diversite_code_saison = models.CharField(max_length=10)
    courbe_de_diversite_reprise_m = models.FloatField()
    courbe_de_diversite_reprise_b = models.FloatField()
    courbe_de_diversite_date_creation = models.DateField(auto_now_add=True)
    courbe_de_diversite_date_modification = models.DateField(auto_now=True)

    def __str__(self):
        stringModel = "ID: {courbe_de_diversite_id},\nSuperficie: {courbe_de_diversite_superficie},\nCode Saison: {courbe_de_diversite_code_saison},\nReprise m: {courbe_de_diversite_reprise_m},\nReprise b: {courbe_de_diversite_reprise_b}\n"
        return stringModel.format(
                                  courbe_de_diversite_id = self.courbe_de_diversite_id,
                                  courbe_de_diversite_code_saison = self.courbe_de_diversite_code_saison,
                                  courbe_de_diversite_superficie = self.courbe_de_diversite_superficie,
                                  courbe_de_diversite_reprise_m = self.courbe_de_diversite_reprise_m,
                                  courbe_de_diversite_reprise_b = self.courbe_de_diversite_reprise_b
                                )

class PenteOrigineDeDiversitee(models.Model):
    """
        Model that hold different values for y = mx + b (To compute the diversity load)
    """
    pente_origine_diversite_id = models.UUIDField(primary_key=True, default=uuid.uuid1())
    pente_origine_diversite_nbr_client = models.IntegerField()
    pente_origine_diversite_m = models.FloatField()
    pente_origine_diversite_b = models.FloatField()
    courbe_de_diversite_id = models.ForeignKey('user_interface.CourbeDeDiversitee',on_delete=models.PROTECT)

    def __str__(self):
        stringModel = "ID: {pente_origine_diversite_id},\nNbr de client: {pente_origine_diversite_nbr_client},\nPente: {pente_origine_diversite_m},\nOrigine: {pente_origine_diversite_b},\nCourbe de diversite: {courbe_de_diversite_id}\n"
        return stringModel.format(
                                    pente_origine_diversite_id= self.pente_origine_diversite_id,
                                    pente_origine_diversite_nbr_client= self.pente_origine_diversite_nbr_client,
                                    pente_orgine_diversite_m= self.pente_origne_diversite_m,
                                    pente_origine_diversite_b= self.pente_origine_diversite_b,
                                    courbe_de_diversite_id = self.courbe_de_diversite_id
                                )

class AutreCharge(models.Model):
    """
        Model that represents additionnal charges (It can be a housing or something else)
    """
    autre_charge_id = models.UUIDField(primary_key=True, default=uuid.uuid1())
    nom_du_noeud = models.CharField(max_length=25)
    noeud_alias = models.CharField(max_length=50)
    position_x = models.FloatField()
    position_y = models.FloatField()
    successeur = models.CharField(max_length=25)
    predecesseur = models.CharField(max_length=25)
    autre_charge_description = models.CharField(max_length=150)
    autre_charge_raccorde = models.BooleanField(default=False)
    autre_charge_kVA = models.FloatField()
    autre_charge_FP = models.FloatField()
    autre_charge_Fr = models.FloatField()
    autre_charge_facteur_reprise = models.FloatField(default=120)
    autre_charge_facteur_simultaneite_de_niveau_2 = models.FloatField(default=85)
    autre_charge_i_court_circuit = models.FloatField(blank=True, null=True)
    autre_charge_i_court_circuit_client = models.FloatField(blank=True, null=True)
    autre_charge_pte_ete_pte_hiver_pourcent = models.FloatField(default=80)
    autre_charge_network = models.FloatField(default=0)
    autre_charge_pointe_ete = models.FloatField()
    autre_charge_pointe_ete_kvar = models.FloatField()
    autre_charge_pointe_ete_kw = models.FloatField()
    autre_charge_pointe_hiver = models.FloatField()
    autre_charge_pointe_hiver_kvar = models.FloatField()
    autre_charge_pointe_hiver_kw = models.FloatField()
    autre_charge_reprise_hiver = models.FloatField()
    autre_charge_reprise_hiver_kvar = models.FloatField()
    autre_charge_reprise_hiver_kw = models.FloatField()
    autre_charge_cummul_v_pourcent = models.FloatField()
    autre_charge_couleur = models.CharField(max_length=25, default="gris")
    autre_charge_facteur_utilisation_annuel = models.FloatField()
    autre_charge_date_creation = models.DateField(auto_now=True)
    autre_charge_date_modification = models.DateField(auto_now_add=True)

def __str__(self):
    return "{} - {} - {} - {} - {} - {} - {} - {} - {} - {}".format(
                                                                    self.autre_charge_id,
                                                                    self.logement_id,
                                                                    self.autre_charge_description,
                                                                    self.autre_charge_kVA,
                                                                    self.autre_charge_FP,
                                                                    self.autre_charge_Fr,
                                                                    self.autre_charge_facteur_simultaneite_de_niveau_2,
                                                                    self.autre_charge_pointe_ete,
                                                                    self.autre_charge_pointe_hiver,
                                                                    self.autre_charge_facteur_utilisation_annuel
                                                                   )
