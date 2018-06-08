from django.contrib import admin



from .models import PersonalDetail
from .models import Client
from .models import Employee
from .models import Technologies
from .models import Project
from .models import StatusReport
from .models import DevSkill
from .models import ProjectTeam
from .models import Invoice


class TechnologiesAdmin(admin.ModelAdmin):
    list_display = ('technologies',)

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('technologies',)
    filter_horizontal = ('technologies',)


admin.site.register(PersonalDetail)
admin.site.register(Client)
admin.site.register(Employee)
admin.site.register(Technologies)
admin.site.register(Project)
admin.site.register(DevSkill)
admin.site.register(StatusReport)
admin.site.register(ProjectTeam)
admin.site.register(Invoice)



