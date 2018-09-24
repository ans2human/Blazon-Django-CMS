from django.db import models
from django import template
from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives
from django.db import models
from django.template import Context


class EmailTemplate(models.Model):
    """
    Email templates get stored in database so that admins can
    change emails on the fly
    """
    logo = models.FileField(upload_to='images/')
    html_template = models.TextField(blank=True, null=True)
    plain_text = models.TextField(blank=True, null=True)
    is_html = models.BooleanField(default=False)
    is_text = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    # unique identifier of the email template
    template_key = models.CharField(max_length=255, unique=True)

    def get_rendered_template(self, tpl, context):
        return self.get_template(tpl).render(context)

    # def get_template(self, tpl):
    #     return template.Template(tpl)

    # def get_subject(self, subject, context):
    #     return subject or self.get_rendered_template(self.subject, context)

    # def get_body(self, body, context):
    #     return body or self.get_rendered_template(self._get_body(), context)

    # def get_sender(self):
    #     return self.from_email or settings.DEFAULT_FROM_EMAIL

    # def get_recipient(self, emails, context):
    #     return emails or [self.get_rendered_template(self.to_email, context)]

    # @staticmethod
    # def send(*args, **kwargs):
    #     EmailTemplate._send(*args, **kwargs)

    # @staticmethod
    # def _send(template_key, context, subject=None, body=None, sender=None,
    #           emails=None, bcc=None, attachments=None):
    #     mail_template = EmailTemplate.objects.get(template_key=template_key)
    #     context = Context(context)

    #     subject = mail_template.get_subject(subject, context)
    #     body = mail_template.get_body(body, context)
    #     sender = sender or mail_template.get_sender()
    #     emails = mail_template.get_recipient(emails, context)

    #     if mail_template.is_text:
    #         return send_mail(subject, body, sender, emails, fail_silently=not
    #         settings.DEBUG)

    #     msg = EmailMultiAlternatives(subject, body, sender, emails,
    #                                  alternatives=((body, 'text/html'),),
    #                                  bcc=bcc
    #                                  )
    #     if attachments:
    #         for name, content, mimetype in attachments:
    #             msg.attach(name, content, mimetype)
    #     return msg.send(fail_silently=not (settings.DEBUG or settings.TEST))

    # def _get_body(self):
    #     if self.is_text:
    #         return self.plain_text

    #     return self.html_template

    # def __str__(self):
    #     return "<{}> {}".format(self.template_key, self.subject)