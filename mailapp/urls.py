from django.conf.urls import url
from . import views

app_name = 'mailapp'


urlpatterns = [

    url(r'^$', views.index, name='index'),
    url(r'^mail/$', views.mail, name='mail'),
    url(r'^dynamic-mail/$', views.dynamicmail, name='dynamicmail'),
    url(r'^dynamic-mail/(?P<pk>\d+)$', views.dynamicmail, name='dynamicmail'),
    url(r'create-mail/$', views.mailpage, name='mailpage'),
    url(r'create-template/$', views.create_template, name='create-template'),
    url(r'edit/(?P<pk>[0-9]+)/$', views.update_template, name='update-template'),
    url(r'delete-template/(?P<pk>\d+)$', views.delete_template, name='delete-template'),
    url(r'^speedtest/$', views.netspeedtest, name='netspeedtest'),

]