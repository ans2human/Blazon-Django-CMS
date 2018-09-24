from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from blazon.resources import ProjectResource

project_resource = ProjectResource()



urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^blazon/', include('blazon.urls')),
    url(r'^', include('blazon.urls')),
    url(r'^mailapp/', include('mailapp.urls')),
    url(r'^blazona/', include(project_resource.urls)),
    url(r'^auth/', include('social_django.urls', namespace='social')),  # <- Here

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
