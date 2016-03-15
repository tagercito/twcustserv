from django import forms
from .models import Enquiry, EnquiryResponse
import email
from django.core.mail import EmailMessage


class BulkSendEnquiryForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea)

  #  def clean(self):
  #      import pdb;pdb.set_trace()
#
    def send(self, ids):
        ids = ids.split(",")
        for enq in Enquiry.objects.filter(pk__in=ids):
            try:
                message_id = email.utils.make_msgid()
                # import pdb;pdb.set_trace()
                em = EmailMessage('Respuesta Atencion al cliente', self.cleaned_data['message'],
                                 'ayuda@ticketek.com.ar', [enq.email],
                                 headers={'Message-ID': message_id})
                em.send()
            except:
                pass
            else:
                EnquiryResponse.objects.create(thread=enq, message=self.cleaned_data['message'],
                                                  message_id=message_id)
