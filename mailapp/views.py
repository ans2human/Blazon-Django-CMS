from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail, BadHeaderError
from django.core import mail
from django.conf import settings
from .forms import TemplateForm
from django.core.mail import EmailMessage
from django.template import Context
from django.template.loader import get_template, render_to_string
from .models import *
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.html import strip_tags
from django.contrib.auth.decorators import login_required
from django.template import Context, Template
import speedtest
def index(request):
    if not request.user.is_authenticated():
        return render(request, 'blazon/login.html')
    else:
        model = EmailTemplate.objects.all()
        context = {"msgs": "welcome to mail client",
                   'htmltemps': model}
        return render(request, 'mailapp/index.html', context)



def create_template(request):
    if not request.user.is_authenticated():
        return render(request, 'blazon/login.html')
    else:
        if request.method == 'POST':
            form = TemplateForm(request.POST or None, request.FILES or None)
            if form.is_valid():
                template = form.save(commit=False)
                template.save()
                return redirect('mailapp:index')
            return render(request, 'mailapp/create_template.html', {"form": form, })
        else:
            form = TemplateForm()
        return render(request, 'mailapp/create_template.html', {'form': form})



def delete_template(request, pk):
    postdel = get_object_or_404(EmailTemplate, pk=pk)
    postdel.delete()
    return redirect('mailapp:index')



def update_template(request, pk, template_name='mailapp/create_template.html'):
    post = get_object_or_404(EmailTemplate, pk=pk)
    form = TemplateForm(request.POST or None, instance=post)
    if form.is_valid():
        form.save()
        return redirect('mailapp:index')
    return render(request, template_name, {'form': form})



@login_required()
def mailpage(request):
    return render(request, 'mailapp/create_mail.html')



def mail(request):
    subject = 'hEllo rajeev sir'
    message = ' Test mail from blaZON'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['ans2human@gmail.com', ]
    send_mail(subject, message, email_from, recipient_list)
    return redirect('mailapp:index')



# def dynamicmail(request,pk):
#     logo = './images/mobilyte_logo.png'
#     to = 'ans2human@gmail.com'
#     dytemp = get_object_or_404(EmailTemplate, pk=pk)
#     print(dytemp.html_template)
#     subject = 'Test Mail-  Registration Successful'
#     body = 'sdfsdfsdf'
#     html_message = render_to_string( dytemp.html_template ,
#                                    {'logo':logo,'to':to, 'subject':subject, 'body':body}
#                                    )
#     plain_message = strip_tags(html_message)
#     from_email = 'From <anandanshuman95@gmail.com>'
#     send_mail(
#               dytemp.html_template, subject,
#               plain_message, from_email,
#               [to], html_message=html_message
#               )
#     return redirect('mailapp:index')


# 'mailapp/test_email.html'
# this is normal


def dynamicmail(request,pk):
    logo = './images/mobilyte_logo.png'
    to = 'ans2human@gmail.com'
    dytemp = get_object_or_404(EmailTemplate, pk=pk)
    subject = 'Test Mail-  Registration Successful'
    body = 'sdfsdfsdf'
    from_mail = request.user
    t = Template(dytemp.html_template)
    c = Context({'logo':logo,'to':to, 'subject':subject, 'body':body})
    html_message = t.render(c)
    plain_message = strip_tags(html_message)
    from_email = 'From <anandanshuman95@gmail.com>'
    send_mail(
              subject,
              plain_message, from_email,
              [to], html_message=html_message
              )
    return redirect('mailapp:index')



def netspeedtest(request):

    servers = []
    # If you want to test against a specific server
    # servers = [1234]

    s = speedtest.Speedtest()
    s.get_servers(servers)
    s.get_best_server()
    s.download()
    s.upload()
    s.results.share()

    results_dict = s.results.dict()
    return render(request, 'mailapp/speedtest.html', results_dict)