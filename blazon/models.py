from __future__ import unicode_literals
from django.contrib.auth.models import Permission, User
from django.db import models
from django_countries.fields import CountryField
from django.core.urlresolvers import reverse



class PersonalDetail(models.Model):
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    contactNo = models.CharField(max_length=50)
    gender = models.CharField(max_length=10,
                           choices=(
                                    ('M', 'Male'),  
                                    ('F', 'Female')
                           )
                           )
    dateOfBirth = models.DateField()
    spouseName = models.CharField(max_length=20)
    spouseDOB = models.DateField()
    anniversary = models.DateField(max_length=50)
    address = models.CharField(max_length=500)
    address2 = models.CharField(max_length=500)
    country = CountryField(blank_label='(select country)')
    city = models.CharField(max_length=50)
    zipcode = models.IntegerField()
    list_display_links = (None,)

    def __str__(self):
        return self.firstName

class Client(models.Model):
    personaldetail = models.ForeignKey(PersonalDetail, on_delete=models.CASCADE)
    isdeleted = models.BooleanField(default=False)
    isdisabled = models.BooleanField(default=False)
    objects = models.Manager()
#    def get_absolute_url(self):
#        return reverse('blazon:clients')  
        
    def __str__(self):
        return self.personaldetail.firstName

    

class Employee(models.Model):
    PersonalDetail = models.ForeignKey(PersonalDetail, on_delete=models.CASCADE)
    employeeid = models.IntegerField()
    joiningdate = models.DateField(max_length=20)
    designation = models.CharField(max_length=50)
    salary = models.IntegerField()
    isdeleted = models.BooleanField(default=False)
    isdisabled = models.BooleanField(default=False)
    objects = models.Manager()
#    def get_absolute_url(self):
#        return reverse('blazon:employees') 
    
    def __str__(self):
        return self.PersonalDetail.firstName

class Technologies(models.Model):
    techname = models.CharField(max_length=20)
    isdeleted = models.BooleanField(default=False)
    isdisabled = models.BooleanField(default=False)

    def __str__(self):
        return self.techname

class Project(models.Model):
    user = models.ForeignKey(User, default=1)
    project_title = models.CharField(max_length=250)
    description = models.TextField(max_length=1500)
    startdate = models.DateField()
    enddate = models.DateField()
    cost = models.IntegerField()
    project_type = models.CharField(max_length=1, 
                                  choices=(
                                           ('1', 'webforms'),  
                                           ('2', 'winforms'),
                                           ('3', 'Native mobile APPS'),
                                           ('4', 'Hybrid mobile APPS')
                                  )
                                  )
                         
    employeeid = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name="Project Resource")
    technologies = models.ManyToManyField(Technologies)
    clientid = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="Client")
    document = models.FileField()
    isdeleted = models.BooleanField(default=False)
    isdisabled = models.BooleanField(default=False)
    is_favorite = models.BooleanField(default=False)
    objects = models.Manager()

#    def get_absolute_url(self):
#        return reverse('Blazon:detail', kwargs={'pk': self.pk}) 

    def __str__(self):
        return self.project_title


class StatusReport(models.Model):
    user = models.ForeignKey(User, default=1)
    projectname = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name="project")
    statusreport_title = models.CharField(max_length=50)
    report = models.TextField(max_length=1500)
    reportdate = models.DateTimeField()
    timedurfrom = models.TimeField(verbose_name="Duration from-")
    timedurto = models.TimeField(verbose_name="To:")
    objects = models.Manager()
    is_favorite = models.BooleanField(default=False)


#    def get_absolute_url(self):
#        return reverse('Blazon:detail') 



    def __str__(self):
        return self.statusreport_title   
    
    
    
class DevSkill(models.Model):
    title = models.CharField(max_length=150)
    devskillsid = models.IntegerField()
    techid = models.ForeignKey(Technologies, on_delete=models.CASCADE)
    employeeid = models.ForeignKey(Employee, on_delete=models.CASCADE)
    def __str__(self):
        return self.title

class ProjectTeam(models.Model):
    title = models.CharField(max_length=150)
    ProjectTeamId = models.IntegerField()
    projectid = models.ForeignKey(Project, on_delete=models.CASCADE)
    employeeid = models.ForeignKey(Employee, on_delete=models.CASCADE,)



    def __str__(self):
        return self.title



class Invoice(models.Model):
    InvoiceMastersId = models.IntegerField()
    clientid = models.ForeignKey(Client, on_delete=models.CASCADE)
    projectid = models.ForeignKey(Project, on_delete=models.CASCADE)
    invoicedate = models.DateField()
    invoiceamount = models.IntegerField()
    services = models.CharField(max_length=500)
    tax = models.IntegerField()
    discount = models.CharField(max_length=50)
    workhours = models.IntegerField()
    hourlyrate = models.IntegerField()
    objects = models.Manager()
#    def get_absolute_url(self):
#        return reverse('blazon:invoice') 
    
 
    def __str__(self):
        return self.services





















