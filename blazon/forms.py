from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from .models import Project, StatusReport, Client, Employee, UserProfile


class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ['project_title', 'description', 'startdate', 'enddate', 'cost', 'project_type',
                  'employeeid', 'technologies', 'clientid', 'document']
        widgets = {
        }


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['personaldetail', 'isdeleted', 'isdisabled']


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['PersonalDetail', 'employeeid', 'joiningdate',
                  'designation', 'salary', 'isdeleted', 'isdisabled']


class StatusReportForm(forms.ModelForm):
    class Meta:
        model = StatusReport
        fields = ['projectname', 'statusreport_title',
                  'report', 'reportdate', 'timedurfrom', 'timedurto']


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
            model = User
            fields = ['username', 'email', 'password']


# class EditProfileForm(forms.ModelForm):
#     class Meta:
#         model = UserProfile
#         fields = (
#             'user',
#             'photo',
#             'website',
#             'bio', 
#             'phone',
#             'city',
#             'country',
#             'organization',          
#         )


class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = {'first_name', 'last_name', 'email'}