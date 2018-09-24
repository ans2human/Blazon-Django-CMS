from django.conf.urls import url
from . import views

app_name = 'blazon'


urlpatterns = [
    url(r'^register/$', views.register, name='register'),
    url(r'^password/$', views.change_password, name='change_password'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^$', views.index, name='index'),
    url(r'^$', views.location, name='location'),
    url(r'^location/(?P<filter_by>[a-zA_Z]+)/$', views.location, name='location'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    url(r'^(?P<project_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<statusreport_id>[0-9]+)/favorite/$', views.favorite, name='favorite'),
    url(r'^projects/(?P<filter_by>[a-zA_Z]+)/$', views.projects, name='projects'),
    url(r'^employees/(?P<filter_by>[a-zA_Z]+)/$', views.employees, name='employees'),
    url(r'^clients/(?P<filter_by>[a-zA_Z]+)/$', views.clients, name='clients'),

    url(r'^userprofile/$', views.userprofile, name='userprofile'),
    url(r'^userprofile/edit/(?P<pk>[0-9]+)/$', views.create_userprofile, name='create_userprofile'),
    # url(r'^userprofile/(?P<pk>[0-9])+/$', views.userprofile, name='userprofile'),
    # url(r'^userprofile/edit/(?P<pk>\d+)/$', views.create_userprofile, name='create_userprofile'),

    url(r'^invoice/(?P<filter_by>[a-zA_Z]+)/$', views.invoice, name='invoice'),
    url(r'^statusreports/(?P<filter_by>[a-zA_Z]+)/$', views.statusreports, name='statusreports'),
    url(r'^create_project/$', views.create_project, name='create_project'),
    url(r'^create_clients/$', views.create_clients, name='create_clients'),
    url(r'^create_employee/$', views.create_employee, name='create_employee'),
    url(r'^(?P<project_id>[0-9]+)/create_statusreport/$', views.create_statusreport, name='create_statusreport'),
    url(r'^(?P<project_id>[0-9]+)/delete_statusreport/(?P<statusreport_id>[0-9]+)/$', views.delete_statusreport, name='delete_statusreport'),
    url(r'^(?P<project_id>[0-9]+)/favorite_project/$', views.favorite_project, name='favorite_project'),
    url(r'^(?P<project_id>[0-9]+)/delete_project/$', views.delete_project, name='delete_project'),
    url(r'^(?P<employee_id>[0-9]+)/delete_employee/$', views.delete_employee, name='delete_employee'),

]
