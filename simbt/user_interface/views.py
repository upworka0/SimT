from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.models import User
from user_interface.compute_network.compute_network import ComputeNetwork
from user_interface.edit_study_context import EditStudyContext
from user_interface.forms import SignUpForm, LoginForm, AddNewStudy, UpdateAdminConfigurations
from user_interface.models import Client, Admin, Etude
from django.contrib.auth.decorators import login_required
import uuid
# Create your views here.

edit_study_context = EditStudyContext()

def index(request):
    """
        function that returns the index
    """
    return render(request, 'user_interface/index.html')

def signup(request):
    """signup

    :param request:
    """
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            Client.objects.create(user=user).save()
            auth_login(request, user)
            return redirect('login')
        else:
            return redirect('signup')
    else:
        form = SignUpForm()
        return render(request, 'user_interface/signup.html', { 'form':form })

def login(request):
    """login

    :param request:
    """
    form = LoginForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            user = form.clean()
            if user is not None:
                user = User.objects.get(username=user['username'])
                auth_login(request, user)
                if Client.objects.filter(user=user).exists():
                    request.session['is_admin'] = False
                    return redirect('home')
                elif Admin.objects.filter(user=user).exists():
                    request.session['is_admin'] = True
                    return redirect('admin')
    return render(request, "user_interface/login.html", {'form': form})

@login_required
def logout(request):
    """logout

    :param request:
    """
    django_logout(request)
    return redirect('login')


@login_required
def edit_study(request):
    """
        function that returns the edit_study page with
        data from database
    """
    study_voltage = request.GET['voltage']
    etude_id = request.GET['etude_id']
    etude = None
    client = None
    if Etude.objects.filter(etude_id=etude_id).exists():
        etude = Etude.objects.filter(etude_id=etude_id).get()
        client = etude.clients_etudes.filter().all().get()
    type_list = edit_study_context.build_context(study_voltage=study_voltage)
    type_list['etude'] = etude
    type_list['clients'] = client
    return render(request, 'user_interface/edit_study.html', context=type_list)

@login_required
def home(request):
    """home

    :param requests:
    """
    form = AddNewStudy()
    client = Client.objects.filter(user=request.user).get()
    if request.method == "POST":
        form = AddNewStudy(request.POST)
        if form.is_valid():
            etude = Etude.objects.create(etude_id=uuid.uuid1(),etude_nom=form.cleaned_data['etude_nom'], etude_tension=form.cleaned_data['etude_tension'], etude_description=form.cleaned_data['etude_description'],etude_temperature_ambiante_pointe_sout= client.client_temperature_ambiante_pointe_sout_defaut, etude_temperature_ambiante_pointe_aerien=client.client_temperature_ambiante_pointe_aerien_defaut, etude_conducteur_pointe_sout=client.client_temperature_conducteur_pointe_sout_defaut, etude_conducteur_pointe_aerien=client.client_temperature_conducteur_pointe_aerien_defaut)
            etude.clients_etudes = [client]
            etude.save()
            form = AddNewStudy()
        elif form.is_valid() == False and request.POST['etude_id']:
            Etude.objects.filter(etude_id=request.POST['etude_id']).delete()
    etude = []
    if Etude.objects.filter(clients_etudes=client).exists():
        for _etude in Etude.objects.filter(clients_etudes=client):
            etude.append(_etude)
    return render(request, 'user_interface/home.html', context={"username" : request.user.username, 'forms': form, "etudes": etude})


@login_required
def admin(request):
    """admin
    
    Arguments:
        request {http_request} -- [request with user embedded]
    """
    admin = ""
    update_admin_form_configurations = ""

    if request.method == "GET" :
        if Admin.objects.filter(user=request.user).exists():
            admin = Admin.objects.filter(user=request.user).get()
            update_admin_form_configurations = UpdateAdminConfigurations(instance=admin)
    else :
        update_admin_form_configurations = UpdateAdminConfigurations(request.POST)
        if update_admin_form_configurations.is_valid():
            admin = update_admin_form_configurations.save(commit=False)
            admin.admin_id = Admin.objects.filter(user=request.user).get().admin_id # Need to add admin_ID to new admin model
            admin.user = request.user # Need to add FK user to new admin Model, otherwise it won't update
            admin = ComputeNetwork.admin_compute_reactance_factor(admin=admin) # Compute FQ from FP inputed
            admin.save()

    return render(request, 'user_interface/admin.html', context={"admin" : admin, "form": update_admin_form_configurations, "username" : request.user.username})
    



def compute_test(request):
    """
        @ARGS : Request
        @RETURNS compute_test VIEW -> template/user_interface/compute_test.html
    """
    study_context = edit_study_context.build_context(0)
    return render(request, 'user_interface/compute_test.html', context=study_context)
