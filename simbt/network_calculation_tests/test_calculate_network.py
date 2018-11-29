import uuid
from django.test import TestCase
from django.contrib.auth.models import User
from user_interface.models import TypeDeTransformateur, TypeDeChauffage, TypeDeConducteur, TypeDeLogement, Logement, Conducteur, Transformateur, Client, Etude, CourbeDeDiversitee, PenteOrigineDeDiversitee, LogementCodeSaison, Noeud, Admin
from user_interface.compute_network.compute_network import ComputeNetwork
from user_interface.compute_network.logger_configurer import configure_logging, logger

class computeNetworkTest(TestCase):
    TEST_EMAIL = "example@exemple.com"
    compute_network = ""
    fixtures = ['courbe_diversites.json', 'chauffage.json', 'conducteur.json',
                'mat_client.json', 'xfo_data.json', 'logement_code_saison.json',
                'type_logement.json']
    __NETWORK_ARRAY = []
    __NETWORK_ARRAY_2 = []
    __NETWORK_ARRAY_3 = []


    def setUp(self):
        user = User.objects.create_user(username="Test", email=self.TEST_EMAIL, password="wwsasdxx123456772312w")
        admin_user = User.objects.create_user(username="IamAdmin", email="admin@email.root", password="rootAd$m$$i$$n1$23455")
        user.save()
        admin_user.save()
        admin = Admin(admin_id=uuid.uuid1(),user=admin_user)
        admin.save()
        ComputeNetwork.admin_compute_reactance_factor(admin=admin)
        client = Client(client_id=uuid.uuid1() ,user=user, client_nom_projeteur="Test Name")
        client.save()
        etude = Etude(etude_nom="Etude Test",
                      etude_temperature_ambiante_pointe_sout=client.client_temperature_ambiante_pointe_sout_defaut,
                      etude_temperature_ambiante_pointe_aerien=client.client_temperature_ambiante_pointe_aerien_defaut,
                      etude_conducteur_pointe_sout=client.client_temperature_conducteur_pointe_sout_defaut,
                      etude_conducteur_pointe_aerien=client.client_temperature_conducteur_pointe_aerien_defaut)
        etude.save()
        self.compute_network = ComputeNetwork(admin=admin, study=etude)
        client_db = Client.objects.get(user=user)
        etude.clients_etudes.add(client_db)
        etude.save()
        type_de_tranformateur = TypeDeTransformateur.objects.get(type_transformateur_type="10a")
        transformateur = Transformateur.objects.create(type_de_transformateur=type_de_tranformateur,
                                        etude_id=etude, nom_du_noeud="T1", position_x=0,
                                        position_y=0, successeur="A1", predecesseur="")
        transformateur.save()
        self.__NETWORK_ARRAY.append(transformateur)

        type_conducteur = TypeDeConducteur.objects.get(type_conducteur_type="Tx4/0")
        conducteur = Conducteur.objects.create(etude_id=etude, type_conducteur_id=type_conducteur,
                                nom_du_noeud="A1", predecesseur="T1", successeur="N1",
                                position_x=0, position_y=0, longueur=10)
        conducteur.save()
        self.__NETWORK_ARRAY.append(conducteur)

        noeud = Noeud.objects.create(etude_id=etude, nom_du_noeud="N1", predecesseur="A1", successeur="A2",
                     position_x=0, position_y=0)
        noeud.save()
        self.__NETWORK_ARRAY.append(noeud)

        type_conducteur = TypeDeConducteur.objects.get(type_conducteur_type="Tx4/0")
        conducteur_A2 = Conducteur.objects.create(conducteur_id=uuid.uuid1(),etude_id=etude,type_conducteur_id=type_conducteur,
                                nom_du_noeud="A2", predecesseur="N1", successeur="N2",
                                position_x=0, position_y=0, longueur=10)
        conducteur_A2.save()
        self.__NETWORK_ARRAY.append(conducteur_A2)


        noeud_2 = Noeud.objects.create(noeud_id=uuid.uuid1(),etude_id=etude, nom_du_noeud="N2", predecesseur="A2", successeur="A3",
                     position_x=0, position_y=0)
        noeud_2.save()
        self.__NETWORK_ARRAY.append(noeud_2)

        type_conducteur = TypeDeConducteur.objects.get(type_conducteur_type="Tx4/0")
        conducteur_A3 = Conducteur.objects.create(conducteur_id=uuid.uuid1(),etude_id=etude,type_conducteur_id=type_conducteur,
                                nom_du_noeud="A3", predecesseur="N2", successeur="C1",
                                position_x=0, position_y=0, longueur=10)
        conducteur_A3.save()
        self.__NETWORK_ARRAY.append(conducteur_A3)

        type_chauffage = TypeDeChauffage.objects.get(type_chauffage_type="ec20")
        type_logement = TypeDeLogement.objects.get(type_logement_type="U1")
        code_saison = LogementCodeSaison.objects.get(logement_code_saison_type="U1ec20")
        logement = Logement(etude_id=etude, type_de_logement=type_logement, type_de_chauffage=type_chauffage,
                            logement_code_saison=code_saison, nom_du_noeud="C1",
                            surface_habitable=288, nombre_etage=1, position_x=0,
                            position_y=0, predecesseur="A3", successeur="", nombre_de_logement=1)
        logement.save()
        self.__NETWORK_ARRAY.append(logement)
#        self.__NETWORK_ARRAY_2 = self.__NETWORK_ARRAY
#
#        type_conducteur = TypeDeConducteur.objects.get(type_conducteur_type="Tx4/0")
#        conducteur_A4 = Conducteur.objects.create(conducteur_id=uuid.uuid1(), etude_id=etude, type_conducteur_id=type_conducteur,
#                                                  nom_du_noeud="A4", predecesseur="N2", successeur="C2",
#                                                 position_x=0, position_y=0, longueur=10)
#
#        conducteur_A4.save()
#        self.__NETWORK_ARRAY_2.append(conducteur_A4)
#
#        type_chauffage = TypeDeChauffage.objects.get(type_chauffage_type="ec20")
#        type_logement = TypeDeLogement.objects.get(type_logement_type="U1")
#        code_saison = LogementCodeSaison.objects.get(logement_code_saison_type="U1ec20")
#        logement = Logement.objects.create(logement_id=uuid.uuid1(),etude_id=etude, type_de_logement=type_logement, type_de_chauffage=type_chauffage,
#                            logement_code_saison=code_saison, nom_du_noeud="C2",
#                            surface_habitable=120, nombre_etage=1, position_x=0,
#                            position_y=0, predecesseur="A4", successeur="", nombre_de_logement=1)
#
#        logement.save()
#        self.__NETWORK_ARRAY_2.append(logement)
#        self.__NETWORK_ARRAY_3 = self.__NETWORK_ARRAY_2
#
#        type_conducteur = TypeDeConducteur.objects.get(type_conducteur_type="Tx4/0")
#        conducteur_A5 = Conducteur.objects.create(conducteur_id=uuid.uuid1(), etude_id=etude, type_conducteur_id=type_conducteur,
#                                                  nom_du_noeud="A5", predecesseur="N1", successeur="C3",
#                                                 position_x=0, position_y=0, longueur=10)
#
#        conducteur_A4.save()
#        self.__NETWORK_ARRAY_3.append(conducteur_A4)
#
#        type_chauffage = TypeDeChauffage.objects.get(type_chauffage_type="ec20")
#        type_logement = TypeDeLogement.objects.get(type_logement_type="U1")
#        code_saison = LogementCodeSaison.objects.get(logement_code_saison_type="U1ec20")
#        logement = Logement.objects.create(logement_id=uuid.uuid1(),etude_id=etude, type_de_logement=type_logement, type_de_chauffage=type_chauffage,
#                            logement_code_saison=code_saison, nom_du_noeud="C3",
#                            surface_habitable=400, nombre_etage=1, position_x=0,
#                            position_y=0, predecesseur="A5", successeur="", nombre_de_logement=1)
#
#        logement.save()
#        self.__NETWORK_ARRAY_3.append(logement)
#
    def test_database_up(self):
        """
            Test to make sure the test database
            has all the rows it needs
        """
        client = Client.objects.get(client_nom_projeteur="Test Name")
        etude = Etude.objects.get(etude_nom="Etude Test")
        self.assertIsInstance(obj=client, cls=Client)
        self.assertIsInstance(obj=etude, cls=Etude)

#    def test_compute_recovery_capacity_summer(self):
#        """
#            Test to computing of recovery capacity in summer.
#
#            Computed using the XFO capacity
#        """
#        transformer = Transformateur.objects.get(nom_du_noeud="T1")
#        result = self.compute_network.compute_xfo_capacity(
#                                                              capacity=transformer.type_de_transformateur.type_transformateur_capacite,
#                                                              is_winter=False
#                                                             )
#        self.assertEqual(first=result, second=10)
#
#    def test_compute_recovery_capacity_winter(self):
#        """
#            Test to computing of recovery capacity in winter.
#
#            Computed using the XFO capacity
#        """
#        tranformer = Transformateur.objects.get(nom_du_noeud="T1")
#        result = self.compute_network.compute_xfo_capacity(
#                                                               capacity=tranformer.type_de_transformateur.type_transformateur_capacite,
#                                                               is_winter=True
#                                                              )
#        self.assertEqual(first=result, second=22)

#    def test_compute_conductor_attributes(self):
#        """
#            Test computing of conductor attributes
#            with its length
#        """
#        conducteur = Conducteur.objects.get(nom_du_noeud="A1")
#        computed_conducteur = self.compute_network.compute_conductor_parameters(conductor_object=conducteur)
#        self.assertAlmostEqual(first=computed_conducteur.type_conducteur_id.type_conducteur_resistance_par_km, second=2.76)
#        self.assertAlmostEqual(first=computed_conducteur.type_conducteur_id.type_conducteur_variation_resistance_par_celcius, second=10.9)
#        self.assertAlmostEqual(first=computed_conducteur.type_conducteur_id.type_conducteur_resistance_par_km_avec_temperature, second=2.21)
#        self.assertAlmostEqual(first=computed_conducteur.type_conducteur_id.type_conducteur_courant_admissible, second=3717)
#        self.assertAlmostEqual(first=computed_conducteur.type_conducteur_id.type_conducteur_variation_temp_celon_courant, second=0.00470)
#        self.assertAlmostEqual(first=computed_conducteur.type_conducteur_id.type_conducteur_variation_resistance_celon_courant, second=0.0051)
#        self.assertAlmostEqual(first=computed_conducteur.type_conducteur_id.type_conducteur_reactance, second=0.94)
#        self.assertAlmostEqual(first=computed_conducteur.type_conducteur_id.type_conducteur_capacite_repr_hiver, second=1128)
#        self.assertAlmostEqual(first=computed_conducteur.type_conducteur_id.type_conducteur_capacite_planif_ete, second=758.0)
#        self.assertAlmostEqual(first=computed_conducteur.type_conducteur_id.type_conducteur_mat_client.mat_client_resistance, second=3.18)
#        self.assertAlmostEqual(first=computed_conducteur.type_conducteur_id.type_conducteur_mat_client.mat_client_reactance, second=4.01)

    def test_allocation_des_charges(self):
        """test_allocation_des_charges"""
        for component in self.__NETWORK_ARRAY:
            if "C" in component.nom_du_noeud:
                self.compute_network.compute_loads_node(logement_id=component.nom_du_noeud)
       # for component in self.__NETWORK_ARRAY_2:
       #     if "C" in component.nom_du_noeud:
       #         self.compute_network.compute_loads_node(logement_id=component.nom_du_noeud)
       # for component in self.__NETWORK_ARRAY_3:
       #     if "C" in component.nom_du_noeud:
       #         self.compute_network.compute_loads_node(logement_id=component.nom_du_noeud)
        for component in self.__NETWORK_ARRAY:
            if "T" in component.nom_du_noeud:
                self.compute_network.compute_network(transformateur_id=component.nom_du_noeud)

        for component in self.__NETWORK_ARRAY:
            if "N" not in component.nom_du_noeud:
                if 'A' in component.nom_du_noeud:
                    conducteur = Conducteur.objects.filter(nom_du_noeud=component.nom_du_noeud).get()
                    logger.info("Final result of {} \n {}".format(component.nom_du_noeud, conducteur))
                elif 'C' in component.nom_du_noeud:
                    logement = Logement.objects.filter(nom_du_noeud=component.nom_du_noeud).get()
                    logger.info("Final result of {} \n {}".format(component.nom_du_noeud, logement))
                elif 'T' in component.nom_du_noeud:
                    transformateur = Transformateur.objects.filter(nom_du_noeud=component.nom_du_noeud).get()
                    logger.info("Final result of {} \n {}".format(component.nom_du_noeud, transformateur))


#    def test_compute_recovery_load_winter(self):
#        """
#            Compute recovery load for network
#        """
#        logement = Logement.objects.get(nom_du_noeud="C1")
#        code_hiver_logement = logement.logement_code_saison.logement_code_saison_code_hiver
#        code_ete_logement = logement.logement_code_saison.logement_code_saison_code_ete
#        self.assertEqual(first=logement.surface_habitable, second=288)
#        courbe_de_diversitee_ete = CourbeDeDiversitee.objects.get(courbe_de_diversitee_code_saison=code_ete_logement, courbe_de_diversitee_superficie=logement.surface_habitable)
#        courbe_de_diversitee_hiver = CourbeDeDiversitee.objects.get(courbe_de_diversitee_code_saison=code_hiver_logement, courbe_de_diversitee_superficie=logement.surface_habitable)
#        self.assertAlmostEqual(first=courbe_de_diversitee_hiver.courbe_de_diversitee_reprise_m, second=0.00485)
#        self.assertAlmostEqual(first=courbe_de_diversitee_hiver.courbe_de_diversitee_reprise_b, second=25.848)
#        self.assertEqual(first=logement.nombre_de_logement, second=1)
#        result = self.compute_network.compute_network_recovery_load(housing_object=logement, is_winter=True)
#        self.assertAlmostEqual(first=result, second=27.2448)
#
#    def test_compute_recovery_factor(self):
#        """
#            Compute the recovery factor
#        """
#        logement = Logement.objects.get(nom_du_noeud="C1")
#        type_chauffage = logement.type_de_chauffage.type_chauffage_type
#        self.assertNotEqual(first=type_chauffage, second="a")
#        recovery_factor = self.compute_network.compute_recovery_factor(heating_is_electric=True)
#        self.assertAlmostEqual(first=recovery_factor, second=1.99423324)
#
#    def test_convert_kVA_to_kW_and_kVAR(self):
#        """
#            Compute convertion of kVA to kW
#        """
#        logement = Logement.objects.get(nom_du_noeud="C1")
#        result = self.compute_network.compute_network_recovery_load(housing_object=logement, is_winter=True)
#        self.assertAlmostEqual(first=result, second=27.2448)
#        self.assertNotEqual(first=logement.type_de_chauffage.type_chauffage_type, second='a')
#        value_in_kW = self.compute_network.convert_kVA_load_to_kW(load_in_kVA=result, heating_is_electric=True)
#        self.assertAlmostEqual(first=value_in_kW, second=27.18758591)
#        value_kVAR = self.compute_network.convert_kVA_load_to_kVAR(load_in_kVA=result, heating_is_electric=True)
#        self.assertAlmostEqual(first=value_kVAR, second=1.77363648)
