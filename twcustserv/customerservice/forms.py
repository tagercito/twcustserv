from django import forms
from .models import Contact, EnquiryResponse
import email
from django.core.mail import EmailMessage


class BulkSendEnquiryForm(forms.Form):

    message = forms.CharField(widget=forms.Textarea)

    def send(self, ids):
        ids = ids.split(",")
        for contact in Contact.objects.filter(pk__in=ids, type=Contact.ENQUIRY):
            try:
                message_id = email.utils.make_msgid()
                em = EmailMessage(
                    'Respuesta Atencion al cliente',
                    self.cleaned_data['message'],
                    'ayuda@ticketek.com.ar',
                    [contact.email],
                    headers={'Message-ID': message_id}
                )
                em.send()
            except:
                pass
            else:
                EnquiryResponse.objects.create(
                    contact=contact,
                    message=self.cleaned_data['message'],
                    message_id=message_id
                )
