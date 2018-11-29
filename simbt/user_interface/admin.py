from django.contrib import admin
from user_interface.models import Client, Admin, Etude, TypeDeLogement, TypeDeChauffage, TypeDeConducteur, TypeDeTransformateur, AutreCharge, Transformateur, Conducteur, Logement, CourbeDeDiversitee, MatClient, LogementCodeSaison, PenteOrigineDeDiversitee

# Register your models here.

admin.site.register(Client)
admin.site.register(Etude)
admin.site.register(TypeDeLogement)
admin.site.register(TypeDeChauffage)
admin.site.register(TypeDeConducteur)
admin.site.register(TypeDeTransformateur)
admin.site.register(AutreCharge)
admin.site.register(Transformateur)
admin.site.register(Conducteur)
admin.site.register(Logement)
admin.site.register(CourbeDeDiversitee)
admin.site.register(MatClient)
admin.site.register(LogementCodeSaison)
admin.site.register(PenteOrigineDeDiversitee)
admin.site.register(Admin)
