from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from user_interface.models import Admin

TENSION_ETUDE = (
    ("120/240", "120/240"),
    ("120/208", "120/208"),
    ("347/600", '347/600')
)

class SignUpForm(UserCreationForm):
    """SignUpForm"""
    email = forms.EmailField(max_length=254, help_text="Obligatoire" )

    class Meta:
        model = User
        fields = ("email","username","password2", "password1", )


class LoginForm(forms.Form):
    """LoginForm"""
    username = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder': "Nom d'utilisateur", 'class' : "form-control"}))
    password = forms.CharField(max_length=255, widget=forms.PasswordInput(attrs={'placeholder': "Mot de passe", "class" : "form-control"}))

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password') 
        if username and password : 
            user = authenticate(username=username, password=password)
            if ((not user)) or (not user.check_password(password)):
                raise forms.ValidationError(message="Les information son incorrectes. Veuillez essayer de nouveau")
        return super(LoginForm, self).clean()
    

class AddNewStudy(forms.Form):
    """AddNewStudy"""
    etude_nom = forms.CharField(max_length=255, required=True, label="Nom de l'étude")
    etude_tension = forms.ChoiceField(choices=TENSION_ETUDE)
    etude_description = forms.CharField(max_length=500, widget=forms.Textarea)

class UpdateAdminConfigurations(ModelForm):
    """UpdateAdminConfigurations

        form responsible for changing the configurations
        of an admin which ultimatly is going to change
        something for the end-user computation results

    Arguments:
        forms {[ModelForm]} -- [Objet from django.core]
    """
    class Meta:
        model = Admin

        exclude = [
            "admin_id",
            "user",
            "admin_r_source",
            "admin_x_source"
        ]

        widgets = {
            "admin_cout_pertes_puissance" : forms.NumberInput(attrs={"class": "form-control"}),
            "admin_cout_pertes_energie" : forms.NumberInput(attrs={"class": "form-control"}),
            "admin_r_temp_fixe" : forms.CheckboxInput(attrs={"class": "form-control"}),
            "admin_temp_ambiante_pte_a" : forms.NumberInput(attrs={"class": "form-control"}),
            "admin_temp_ambiante_pte_s" : forms.NumberInput(attrs={"class": "form-control"}),
            "admin_temp_cond_pte_a" : forms.NumberInput(attrs={"class": "form-control"}),
            "admin_temp_ambiante_pte_s" : forms.NumberInput(attrs={"class": "form-control"}),
            "admin_temp_cond_pte_a" : forms.NumberInput(attrs={"class": "form-control"}),
            "admin_temp_ambiante_pte_s" : forms.NumberInput(attrs={"class": "form-control"}),
            "admin_temp_cond_pte_a" : forms.NumberInput(attrs={"class": "form-control"}),
            "admin_temp_cond_pte_s" : forms.NumberInput(attrs={"class": "form-control"}),
            "admin_fp_electrique_pointe" : forms.NumberInput(attrs={"class": "form-control"}),
            "admin_fq_electrique_pointe" : forms.NumberInput(attrs={"class": "form-control", "disabled": "disabled"}),
            "admin_fp_autre_pointe" : forms.NumberInput(attrs={"class": "form-control"}),
            "admin_fq_autre_pointe" : forms.NumberInput(attrs={"class": "form-control", "disabled":"disabled"}),
            "admin_fq_recovery_electrique_pointe" : forms.NumberInput(attrs={"class": "form-control", "disabled":"disabled"}),
            "admin_fp_recovery_electrique_pointe" : forms.NumberInput(attrs={"class": "form-control"}),
            "admin_fp_recovery_autre_pointe" : forms.NumberInput(attrs={"class": "form-control"}),
            "admin_fq_recovery_autre_pointe" : forms.NumberInput(attrs={"class": "form-control", "disabled":"disabled"}),
            "admin_r1_depart_mt" : forms.NumberInput(attrs={"class": "form-control"}),
            "admin_x1_depart_mt" : forms.NumberInput(attrs={"class": "form-control"}),
            "admin_r0_depart_mt" : forms.NumberInput(attrs={"class": "form-control"}),
            "admin_x0_depart_mt" : forms.NumberInput(attrs={"class": "form-control"}),
            "admin_r1_cond_mt_a" : forms.NumberInput(attrs={"class": "form-control"}),
            "admin_x1_cond_mt_a" : forms.NumberInput(attrs={"class": "form-control"}),
            "admin_r0_cond_mt_a" : forms.NumberInput(attrs={"class": "form-control"}),
            "admin_x0_cond_mt_a" : forms.NumberInput(attrs={"class": "form-control"}),
            "admin_r1_cond_mt_a" : forms.NumberInput(attrs={"class": "form-control"}),
            "admin_x1_cond_mt_a" : forms.NumberInput(attrs={"class": "form-control"}),
            "admin_r0_cond_mt_s" : forms.NumberInput(attrs={"class": "form-control"}),
            "admin_x0_cond_mt_s" : forms.NumberInput(attrs={"class": "form-control"}),
            "admin_r1_cond_mt_s" : forms.NumberInput(attrs={"class": "form-control"}),
            "admin_x1_cond_mt_s" : forms.NumberInput(attrs={"class": "form-control"}),
            "admin_ph_ph_mt" : forms.NumberInput(attrs={"class": "form-control"}),
        }

        # TODO:Work on the wording
        labels = {
            "admin_cout_pertes_puissance" : "Coût marginal des pertes en puissance à la pointe ($/kW) :",
            "admin_cout_pertes_energie" : "Coût marginal des pertes en énergie en période hors pointe (¢/kW) :",
            "admin_r_temp_fixe" : "Température fixe des conducteurs :",
            "admin_temp_ambiante_pte_a" : "Température ambiante en aérien au moment de la pointe (°C) :",
            "admin_temp_ambiante_pte_s" : "Température ambiante en souterrain au moment de la pointe (°C) :",
            "admin_temp_cond_pte_a" : "Température des conducteurs en aérien au moment de la pointe (°C) :",
            "admin_temp_ambiante_pte_s" : "Température ambiante en souterrain au moment de la pointe (°C) :",
            "admin_temp_cond_pte_a" : "Température des conducteurs en aérien au moment de la pointe (°C) :",
            "admin_temp_ambiante_pte_s" : "Température ambiante en souterrain au moment de la pointe (°C) :",
            "admin_temp_cond_pte_a" : "Température des conducteurs en aérien au moment de la pointe (°C) :",
            "admin_temp_cond_pte_s" : "Température des conducteurs en souterrain au moment de la pointe (°C) :",
            "admin_fp_electrique_pointe" : "Facteur de puissance chauffage électrique en pointe ( % ) :",
            "admin_fq_autre_pointe" : "Facteur de réactance autre chauffage en pointe ( % ) :",
            "admin_fq_recovery_electrique_pointe" : "Facteur de puissance en reprise chauffage électrique en pointe ( % ) :",
            "admin_fp_recovery_electrique_pointe" : "Facteur de réactance en reprise chauffage électrique en pointe ( % ) :",
            "admin_fp_recovery_autre_pointe" : "Facteur de puissance en reprise autre chauffage en pointe ( % ) :",
            "admin_fq_recovery_autre_pointe" : "Facteur de réactance en reprise autre chauffage en pointe ( % ) :",
            "admin_frepr_ph_chauff_electrique" : "Facteur de reprise de la puissance active avec chauffage électrique en pointe :",
            "admin_frepr_qh_chauff_electrique" : "Facteur de reprise de la puissance réactive  avec chauffage électrique en pointe :",
            "admin_r1_depart_mt" : "Résistance directe du départ de ligne MT au poste HT/MT ( ohms ) :",
            "admin_x1_depart_mt" : "Réactance inductive directe du départ de ligne MT au poste HT/MT ( ohmss ) :",
            "admin_r0_depart_mt" : "Résistance homopolaire du départ de ligne MT au poste HT/MT ( ohms ) :",
            "admin_x0_depart_mt" : "Réactance inductive homopolaire du départ de ligne MT au poste HT/MT ( ohms ) :",
            "admin_r1_cond_mt_a" : "Résistance linéaire directe des conducteurs MT aériens entre le poste et le réseau MT  ( ohms/km ) :",
            "admin_x1_cond_mt_a" : "Réactance inductive linéaire directe des conducteurs MT aériens entre le poste et le réseau MT ( ohms/km ) :",
            "admin_r0_cond_mt_a" : "Résistance linéaire homopolaire des conducteurs MT aériens entre le poste et le réseau MT ( ohms/km ) :",
            "admin_x0_cond_mt_a" : "Réactance inductive linéaire homopolaire des conducteurs MT aériens entre le poste et le réseau MT ( ohms/km ) :",
            "admin_r1_cond_mt_a" : "Résistance linéaire directe des conducteurs MT aériens entre le poste et le réseau MT ( ohms/km ) :",
            "admin_x1_cond_mt_a" : "Réactance inductive linéaire directe des conducteurs MT aérens entre le poste et le réseau MT ( ohms/km ) :",
            "admin_r0_cond_mt_s" : "Résistance linéaire directe des conducteurs MT souterrains entre le poste et le réseau MT ( ohms/km ) :",
            "admin_x0_cond_mt_s" : "Réactance inductive linéaire directe des conducteurs MT souterrains entre le poste et le réseau MT ( ohms/km ) :",
            "admin_r1_cond_mt_s" : "Résistance linéaire homopolaire des conducteurs MT souterrains entre le poste et le réseau MT ( ohms/km ) :",
            "admin_x1_cond_mt_s" : "Réactance inductive linéaire homopolaire des conducteurs MT souterrains entre le poste et le réseau MT ( ohmw/km ) :",
            "admin_ph_ph_mt" : "Tension phase-phase du réseau MT ( kV ) :"
        }