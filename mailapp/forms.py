from django import forms
from django.core.validators import RegexValidator
from .models import EmailTemplate


# validators = {
#     'alphanumeric': RegexValidator(
#         r'^[a-zA-Z]*$', 'Only alphanumeric characters are allowed.'),
# }

# class MailForm(forms.Form):

#     query = forms.CharField(
#         validators=[validators['alphanumeric']]
# )


class TemplateForm(forms.ModelForm):
    class Meta:
        model = EmailTemplate
        fields = ['html_template', 'plain_text', 'is_html', 'is_text', 'template_key', 'logo']

