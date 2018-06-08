# api/resources.py
from tastypie.resources import ModelResource
from blazon.models import Project



class ProjectResource(ModelResource):
    class Meta:
        queryset = Project.objects.all()
        resource_name = 'proj'
        