import uuid
from django.test import TestCase
from django.contrib.auth.models import User
from user_interface.models import TypeDeTransformateur, TypeDeChauffage, TypeDeConducteur, TypeDeLogement, Logement, Conducteur, Transformateur, Client, Etude, CourbeDeDiversitee, PenteOrigineDeDiversitee, LogementCodeSaison, Noeud, Admin
from user_interface.compute_network.compute_network import ComputeNetwork
from user_interface.compute_network.logger_configurer import configure_logging, logger

class TestFQCompute(TestCase):

    def setUp(self):
        """setUp

            Create an admin and a user in a tmp database
            for testing purposes

        """
        admin_user = User.objects.create_user(username="IamAdmin", email="admin@email.root", password="rootAd$m$$i$$n1$23455")
        admin_user.save()
        admin = Admin(admin_id=uuid.uuid1(),user=admin_user)
        admin.save()


    def test_database_up(self):
        """test_database_up

            Make sure my test object are tere

        """
        user_count = User.objects.count()
        admin_count = Admin.objects.count()
        self.assertEqual(user_count, 1)
        self.assertEqual(admin_count, 1)
        user = User.objects.filter(username='IamAdmin').get()
        admin = Admin.objects.get()
        self.assertIsInstance(cls=User, obj=user)
        self.assertIsInstance(cls=Admin, obj=admin)
        self.assertEqual(admin.user, user)
    
    def test_compute_fq_electrique(self):
        admin = Admin.objects.get()
        admin = ComputeNetwork.admin_compute_reactance_factor(admin=admin)
        admin = Admin.objects.get()
        self.assertIsInstance(cls=Admin, obj=admin)
        self.assertEqual(admin.admin_fq_electrique_pointe, 9.98749217771907)

    def test_compute_fq_autre(self):
        admin = Admin.objects.get()
        admin = ComputeNetwork.admin_compute_reactance_factor(admin=admin)
        admin = Admin.objects.get()
        self.assertIsInstance(cls=Admin, obj=admin)
        self.assertEqual(admin.admin_fq_autre_pointe, 31.224989991992) 

    def test_compute_fq_electrique_reprise(self):
        admin = Admin.objects.get()
        admin = ComputeNetwork.admin_compute_reactance_factor(admin=admin)
        admin = Admin.objects.get()
        self.assertIsInstance(cls=Admin, obj=admin)
        self.assertAlmostEqual(admin.admin_fq_recovery_electrique_pointe, 6.51064950150825) 
        
    def test_compute_fq_autre_reprise(self):
        admin = Admin.objects.get()
        admin = ComputeNetwork.admin_compute_reactance_factor(admin=admin)
        admin = Admin.objects.get()
        self.assertIsInstance(cls=Admin, obj=admin)
        self.assertEqual(admin.admin_fq_recovery_autre_pointe, 31.224989991992)