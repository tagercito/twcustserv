from django.contrib import admin
from django.conf import settings
# Register your models here.
from django.forms import TextInput, Textarea
from django.db import models
from customerservice.models import Thread, Message , Bulletin, Topic, TopicField, TopicForm, Enquiry, EnquiryResponse
from django.conf import settings
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect
import twitter
import email
from django.conf.urls import patterns, include, url

def split(s, signature, l=[]): #funcion recursiva que parte el texto en strings de 140 caracteres
    if len(s) < 140-len(signature):
        l.append(s+signature)
        return l
    l.append(s[:140-len(settings.CONTINUA)]+settings.CONTINUA)
    return split(s[140-len(settings.CONTINUA):], signature,  l)


class MessageStackedInline(admin.StackedInline):
    exclude = ('creator', 'sender', 'message_id')
    readonly_fields = ('user',)
    model = Message
    extra = 1
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 6, 'cols': 40, 'style': 'width: 600px;'})},
    }
    suit_classes = 'suit-tab suit-tab-msgs'


class ThreadAdmin(admin.ModelAdmin):
    inlines = [MessageStackedInline, ]
    list_filter = ('status', 'assigned_to' )
    readonly_fields = ['screen_name', 'user_id', 'date_created']
    list_display = ('screen_name', 'date_created')
    
    def get_readonly_fields(self, request, obj=None):
        user_group = request.user.groups.all()[0]
        if 'Administrador' == user_group.name or 'Supervisor' in user_group.name:
            return self.readonly_fields
        return self.readonly_fields + ['assigned_to']

    def suit_row_attributes(self, Thread, request):
        css_class = {
            settings.CLOSED: 'error',
            settings.PENDING: 'warning',
            settings.OPEN: 'success'}.get(Thread.status)
        if css_class:
            return {'class': css_class, 'data': Thread}

    def has_add_permission(self, request):
        return False

    def save_formset(self, request, form, formset, change):
        api = twitter.Api(consumer_key=settings.CONSUMER_KEY, consumer_secret=settings.CONSUMER_SECRET,
                          access_token_key=settings.ACCESS_TOKEN_KEY, access_token_secret=settings.ACCESS_TOKEN_SECRET)
        formset.save()
        if change:
            for f in formset.forms:
                if f.changed_data:
                    obj = f.instance
                    obj.user = request.user
                    signature = ' - ' + ''.join(request.user.first_name[0]+request.user.last_name[0])
                    for message in split(obj.message, signature):
                        try:
                            own_msg = api.PostDirectMessage(message, obj.thread.user_id)
                            print message
                        except:
                            pass
                    if own_msg:
                        obj.message_id = str(own_msg.id)
                        obj.creator = True
                    obj.save()

    fieldsets = [
        (None, {
            'classes': ('suit-tab', 'suit-tab-general',),
            'fields': ['screen_name', 'uer_id', 'date_created', 'status', 'assigned_to', 'email']
        }),

    ]
    suit_form_tabs = (('general', 'General'), ('msgs', 'Mensajes') , ('info', 'Info de la cuenta'))

    suit_form_includes = (
        ('enq_user_info.html', '', 'info'),
    )


class BulletinAdmin(admin.ModelAdmin):
    list_display = ('user', 'text')
    fields = ('text', 'important')

    def save_model(self, request, obj, form, change):
        if not obj.user:
            obj.user = request.user
        obj.save()

class TopicFieldInLine(admin.StackedInline):
    model = TopicField
    extra = 1

class TopicFormAdmin(admin.ModelAdmin):
    inlines = [TopicFieldInLine,]

class TopicInline(admin.StackedInline):
    model = Topic
    extra = 1

class TopicAdmin(admin.ModelAdmin):
    inlines = [TopicInline]

class EnquiryMessageInline(admin.StackedInline):
    model = EnquiryResponse
    exclude = ['creator', 'sender', 'user', 'message_id']
    extra = 1
    suit_classes = 'suit-tab suit-tab-msgs'

def bulk_send(modeladmin, request, queryset):
    ids = [str(obj.pk) for obj in queryset]
    return HttpResponseRedirect("bulk_send/%s/" % (",".join((ids))))

bulk_send.short_description = 'Bulk Send'

from django.views.generic.edit import FormView
from .forms import BulkSendEnquiryForm

class BulkSend(FormView):
    template_name = 'bulk_send_enquiry.html'
    form_class = BulkSendEnquiryForm
    success_url = '/admin/customerservice/enquiry/'

    def form_valid(self, form):
        form.send(self.kwargs['ids'])
        return HttpResponseRedirect(self.success_url)

class EnquiryAdmin(admin.ModelAdmin):
    list_display = ('topic', 'date', 'status')
    readonly_fields = ['topic', 'date', 'email', 'file', 'enquiry']
    inlines = [EnquiryMessageInline]
    actions = [bulk_send]

    def has_add_permission(self, request):
        return False

    def get_urls(self):
        urls = super(EnquiryAdmin, self).get_urls()
        my_urls = patterns('',
            (r'bulk_send/(?P<ids>.+)/$', self.admin_site.admin_view(BulkSend.as_view())),
        )
        return my_urls + urls

    def save_formset(self, request, form, formset, change):
        formset.save()
        if change:
            for f in formset.forms:
                if f.changed_data:
                    obj = f.instance
                    obj.user = request.user
                   # signature = ' - ' + ''.join(request.user.first_name[0]+request.user.last_name[0])
                    try:
                        message_id = email.utils.make_msgid()
                        em = EmailMessage('Respuesta Atencion al cliente', obj.message,
                                             'ayuda@ticketek.com.ar', [obj.thread.email],
                                             headers={'Message-ID': message_id})
                        em.send()
                    except:
                        pass
                    else:
                        obj.message_id = message_id
                    obj.save()

    fieldsets = [
        (None, {
            'classes': ('suit-tab', 'suit-tab-general',),
            'fields': ['topic', 'enquiry', 'email', 'file', 'status']
        }),

    ]
    suit_form_tabs = (('general', 'General'), ('msgs', 'Mensajes') , ('info', 'Info de la cuenta'))

    suit_form_includes = (
        ('enq_user_info.html', '', 'info'),
    )


admin.site.register(Bulletin, BulletinAdmin)
admin.site.register(Thread, ThreadAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(TopicForm, TopicFormAdmin)
admin.site.register(Enquiry, EnquiryAdmin)


