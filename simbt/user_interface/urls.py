from django.conf.urls import url
from user_interface import views
from user_interface import http_request

urlpatterns = [
    url(r'^$', views.login, name='login'),
    url(r'^signup', views.signup, name='signup'),
    url(r'^logout', views.logout, name='logout'),
    url(r'^home', views.home, name='home'),
    url(r'^edit_study', views.edit_study, name="edit_study"),
    url(r'^admin', views.admin, name="admin"),
    url(r'^compute_test', views.compute_test, name="compute_test"),
    url(r'^get_type_possible_information/(?P<voltage_type>[0-2]{1})', http_request.get_type_possible_information, name="get_type_possible_information"),
    url(r'^get_type_details/(?P<what_type>\S+)/(?P<type_id>\S+)', http_request.get_type_details, name="get_type_details"),
    url(r'^get_compute_network/(?P<etude_id>\S+)', http_request.get_compute_network, name="get_compute_network"),
    url(r'^save/(?P<study_id>\S+)', http_request.save_study, name="save_study"),
]
