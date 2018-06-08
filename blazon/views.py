import requests
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from .forms import ProjectForm, StatusReportForm, UserForm, ClientForm, EmployeeForm
from .models import Project, StatusReport, Client, Employee, StatusReport, Invoice

IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']


def create_project(request):
    if not request.user.is_authenticated():
        return render(request, 'blazon/login.html')
    else:
        form = ProjectForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = request.user
            project.document = request.FILES['document']
            file_type = project.document.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type not in IMAGE_FILE_TYPES:
                context = {
                    'project': project,
                    'form': form,
                    'error_message': 'Image file must be PNG, JPG, or JPEG',
                }
                return render(request, 'blazon/create_project.html', context)
            project.save()
            return render(request, 'blazon/detail.html', {'project': project})
        context = {
            "form": form,
        }
        return render(request, 'blazon/create_project.html', context)

def create_clients(request):
    
    if not request.user.is_authenticated():       
        return render(request, 'blazon/login.html')
    else:
        form = ClientForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            client = form.save(commit=False) 
            client.save()
            return redirect('/blazon/clients/all')
        return render(request, 'blazon/create_clients.html', {"form": form,})


def create_employee(request):
    
    if not request.user.is_authenticated():       
        return render(request, 'blazon/login.html')
    else:
        form = EmployeeForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            employee = form.save(commit=False) 
            employee.save()
            return redirect('/blazon/employees/all')
        return render(request, 'blazon/create_employee.html', {"form": form,})
    
   
    
     


def create_statusreport(request, project_id):
    if not request.user.is_authenticated():       
        return render(request, 'blazon/login.html')
    else:
        form = StatusReportForm(request.POST or None, request.FILES or None)
        project = get_object_or_404(Project, pk=project_id)
        if form.is_valid():
            projects_statusreports = project.statusreport_set.all()
            for s in projects_statusreports:
                if s.statusreport_title == form.cleaned_data.get("statusreport_title"):
                    context = {
                        'project': project,
                        'form': form,
                        'error_message': 'You already added that song',
                    }
                    return render(request, 'blazon/create_statusreport.html', context)
            statusreport = form.save(commit=False)
            statusreport.project = project
            
            statusreport.save()
            return render(request, 'blazon/detail.html', {'project': project})
        context = {
            'project': project,
            'form': form,
        }
        return render(request, 'blazon/create_statusreport.html', context)
    

def delete_project(request, project_id):
    project = Project.objects.get(pk=project_id)
    project.delete()
    projects = Project.objects.filter(user=request.user)
    return render(request, 'blazon/projects.html', {'projects': projects})


def delete_statusreport(request, project_id, statusreport_id):
    project = get_object_or_404(Project, pk=project_id)
    statusreport = StatusReport.objects.get(pk=statusreport_id)
    statusreport.delete()
    return render(request, 'blazon/detail.html', {'project': project})

def delete_employee(request, employee_id):
    employee = Employee.objects.get(pk=employee_id)
    employee.delete()
    employees = Employee.objects.all()
    return render(request, 'blazon/employees.html', {'employees': employees})

def detail(request, project_id):
    if not request.user.is_authenticated():
        return render(request, 'blazon/login.html')
    else:
        user = request.user
        project = get_object_or_404(Project, pk=project_id)
        return render(request, 'blazon/detail.html', {'project': project, 'user': user})


def favorite(request, statusreport_id):
    statusreport = get_object_or_404(StatusReport, pk=statusreport_id)
    try:
        if statusreport.is_favorite:
            statusreport.is_favorite = False
        else:
            statusreport.is_favorite = True
        statusreport.save()
    except (KeyError, statusreport.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})


def favorite_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    try:
        if project.is_favorite:
            project.is_favorite = False
        else:
            project.is_favorite = True
        project.save()
    except (KeyError, Project.DoesNotExist):
        return render(request, 'blazon/index.html')
    else:
        return JsonResponse({'success': True})
    return render(request, 'blazon/index.html')


def location(request):
    ip_address = request.META.get('HTTP_X_FORWARDED_FOR', '')
    response = requests.get('http://freegeoip.net/json/%s' % ip_address)
    geodata = response.json()
    return render(request, 'blazon/location.html', {
        'ip': geodata['ip'],
        'country': geodata['country_name'],
        'city' : geodata['region_name'],
        'latitude': geodata['latitude'],
        'longitude': geodata['longitude'],
        'api_key': 'AIzaSyB4RsrXfB_lwR4L6LiMRQGkpMKQE0SIEro'  
    })


def index(request):
    if not request.user.is_authenticated():
        return render(request, 'blazon/login.html')
    else:
        all_projects = Project.objects.all()
        numall_projects = Project.objects.filter().count()
        projects = Project.objects.filter(user=request.user)
        clients = Client.objects.all()
        num_projects = Project.objects.filter(user=request.user).count()
        num_clients = Client.objects.filter().count()
        employees = Employee.objects.all()
        num_employees = Employee.objects.filter().count()
        statusreport_ids = []
        for project in Project.objects.filter(user=request.user):
            for statusreport in project.statusreport_set.all():
                statusreport_ids.append(statusreport.pk)
                users_statusreports = StatusReport.objects.filter(pk__in=statusreport_ids).count()
        # all_staturreports = StatusReport.objects.all()
        statusreport_results = StatusReport.objects.all()
        # num_reports = StatusReport.objects.filter(pk__in=statusreport_ids).count()
        query = request.GET.get("q")
        if query:
            projects = projects.filter(
                Q(project_title__icontains=query)
            ).distinct()
            statusreport_results = statusreport_results.filter(
                Q(statusreport_title__icontains=query)
            ).distinct()
            return render(request, 'blazon/index.html', {
                'projects': projects,
                'statusreports': statusreport_results,
            })
        else:
            return render(request, 'blazon/index.html', {'projects': projects,
                                                        'all_projects': all_projects,
                                                        'numall_project': numall_projects, 
                                                        'clients': clients,
                                                        'employees': employees,
                                                        'num_clients': num_clients,
                                                        'num_employees': num_employees,
                                                        'num_projects': num_projects,
                                                        'users_statusreports': users_statusreports,
                                                        
                                                        })

def projects(request, filter_by):
    if not request.user.is_authenticated():
        return render(request, 'blazon/login.html')
    else:
        allproject = Project.objects.all()
        projects = Project.objects.filter(user=request.user)

        query = request.GET.get("q")
        if query:
            projects = projects.filter(
                Q(project_title__icontains=query)
            ).distinct()
            return render(request, 'blazon/projects.html', {
                'projects': projects,
            })
        else:
            return render(request, 'blazon/projects.html', {'allproject': allproject,
                                                           'projects': projects,})


def employees(request, filter_by):
    if not request.user.is_authenticated():
        return render(request, 'blazon/login.html')
    else:
        employees = Employee.objects.all()
        #['employees'].append(Employee.objects.all()) 
        query = request.GET.get("q")
        if query:
            employees = employees.filter(
                Q(PersonalDetail__icontains=query)
            ).distinct()
            return render(request, 'blazon/employees.html', {
                'employees': employees,
                
            })
        else:
            return render(request, 'blazon/employees.html', {'employees': employees,})

def clients(request, filter_by):
    if not request.user.is_authenticated():
        return render(request, 'blazon/login.html')
    else:
        clients = Client.objects.all()
        query = request.GET.get("q")
        if query:
            clients = clients.filter(
                Q(personalDetail__icontains=query)
            ).distinct()
            return render(request, 'blazon/clients.html', {
                'clients': clients,
            })
        else:
            return render(request, 'blazon/clients.html', {'clients': clients,})


def invoice(request, filter_by):
    if not request.user.is_authenticated():
        return render(request, 'blazon/login.html')
    else:
        invoice = Invoice.objects.all()
        projects = Project.objects.filter(user=request.user)
        query = request.GET.get("q")
        if query:
            invoice = invoice.filter(
                Q(services__icontains=query)
            ).distinct()
            return render(request, 'blazon/invoice.html', {
                'invoice': invoice,
            })
        else:
            return render(request, 'blazon/invoice.html', {'invoice': invoice,
                                                          'projects':projects           
                                                          })

def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'blazon/login.html', context)


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                
                messages.success(request, 'Your password was successfully updated!')                
                return redirect('blazon:index')
                # return render(request, 'blazon/index.html', {'projects': projects})
            else:
                return render(request, 'blazon/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'blazon/login.html', {'error_message': 'Invalid login'})
    return render(request, 'blazon/login.html')


def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                projects = Project.objects.filter(user=request.user)
                return render(request, 'blazon/index.html', {'projects': projects})
    context = {
        "form": form,
    }
    return render(request, 'blazon/register.html', context)

        
    
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('blazon:login_user')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'blazon/change_password.html', {
        'form': form
    })


def statusreports(request, filter_by):
    if not request.user.is_authenticated():
        return render(request, 'blazon/login.html')
    else:
        try:
            statusreport_ids = []
            for project in Project.objects.filter(user=request.user):
                for statusreport in project.statusreport_set.all():
                    statusreport_ids.append(statusreport.pk)
            users_statusreports = StatusReport.objects.filter(pk__in=statusreport_ids)
            if filter_by == 'favorites':
                users_statusreports = users_statusreports.filter(is_favorite=True)
        except Project.DoesNotExist:
            users_statusreports = []
        return render(request, 'blazon/statusreports.html', {
            'statusreport_list': users_statusreports,
            'filter_by': filter_by,
        })
from django.shortcuts import render

# Create your views here.
