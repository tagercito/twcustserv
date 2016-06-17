from django.contrib import admin
from django.conf import settings
# Register your models here.
from django.forms import TextInput, Textarea
from django.db import models
from customerservice.models import Contact, Thread, Message , Bulletin, Topic, TopicField, TopicForm, Enquiry, EnquiryResponse
from django.conf import settings
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect
import twitter
import email
from django.conf.urls import patterns, include, url
from purchase.models import Purchase, PurchaseItem
from transactions.models import Transaction
from accounts.models import Account
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.utils.translation import ugettext_lazy as _
from profiles.models import UserProfile

from django.contrib.auth.models import User

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


class EnquiryMessageInline(admin.StackedInline):
    model = EnquiryResponse
    exclude = ['creator', 'sender', 'user', 'message_id']
    extra = 1
    suit_classes = 'suit-tab suit-tab-msgs'


def bulk_send(modeladmin, request, queryset):
    ids = [str(obj.pk) for obj in queryset]
    return HttpResponseRedirect("bulk_send/%s/" % (",".join((ids))))

bulk_send.short_description = 'Bulk Send'


class ContactAdmin(admin.ModelAdmin):

    inlines = [MessageStackedInline, EnquiryMessageInline]
    actions = [bulk_send]
    list_filter = ['status', 'assigned_to', 'type']
    readonly_fields = ['screen_name', 'user_id', 'date_created', 'topic',
                       'date', 'email', 'file', 'enquiry']
    list_display = ['screen_name', 'created', 'topic', 'status']
    search_fields = ["screen_name", "user_id", "status", "thread_messages__message"]

    fieldsets = [
        (None,{
            'classes': ('suit-tab', 'suit-tab-general'),
            'fields': ['screen_name', 'user_id', 'created', 'status',
                       'assigned_to', 'topic', 'enquiry', 'email', 'file']
        }),

    ]

    suit_form_tabs = (
        ('general', 'General'),
        ('msgs', 'Mensajes'),
        ('info', 'Info de la cuenta')
    )

    suit_form_includes = (
        ('enq_user_info.html', '', 'info'),
    )


    def suit_row_attributes(self, obj, request):
        css_class = {
            Contact.CLOSED: 'error',
            Contact.PENDING: 'warning',
            Contact.OPEN: 'success'}.get(obj.status)
        if css_class:
            return {'class': css_class, 'data': obj}

    def get_readonly_fields(self, request, obj=None):
        # only apply if is Thread?
        try:
            user_groups = request.user.groups.values_list('name', flat=True)
            if 'Administrador' in user_groups or 'Supervisor' in user_groups:
                return self.readonly_fields
        except:
            pass
        return self.readonly_fields + ['assigned_to']

    def has_add_permission(self, request):
        return False

    def save_formset(self, request, form, formset, change):
        # TODO: Performance Issue/User experience
        # Many features implementend in following lines could be replaced by
        # async tasks in celery
        formset.save()
        if change:
            for f in formset.forms:
                if f.changed_data:
                    obj = f.instance
                    obj.user = request.user
                    signature = ' - ' + ''.join(request.user.first_name[0]+request.user.last_name[0])
                    if obj.type == Contact.THREAD:
                        api = twitter.Api(
                            consumer_key=settings.CONSUMER_KEY,
                            consumer_secret=settings.CONSUMER_SECRET,
                            access_token_key=settings.ACCESS_TOKEN_KEY,
                            access_token_secret=settings.ACCESS_TOKEN_SECRET
                        )
                        for message in split(obj.message, signature):
                            try:
                                own_msg = api.PostDirectMessage(message, obj.thread.user_id)
                                print(message)
                            except:
                                pass
                        if own_msg:
                            obj.message_id = str(own_msg.id)
                            obj.creator = True
                    else if obj.type == Contact.ENQUIRY:
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


class EnquiryAdmin(admin.ModelAdmin):
    list_display = ('topic', 'date', 'status')
    readonly_fields = ['topic', 'date', 'email', 'file', 'enquiry']
    inlines = [EnquiryMessageInline]
    actions = [bulk_send]

    def suit_row_attributes(self, Enquiry, request):
        css_class = {
            settings.CLOSED: 'error',
            settings.PENDING: 'warning',
            settings.OPEN: 'success'}.get(Enquiry.status)
        if css_class:
            return {'class': css_class, 'data': Thread}

    def has_add_permission(self, request):
        return False

    def get_urls(self):
        urls = super(EnquiryAdmin, self).get_urls()
        my_urls = [
            url(r'bulk_send/(?P<ids>.+)/$', self.admin_site.admin_view(BulkSend.as_view())),
        ]
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

class ThreadAdmin(admin.ModelAdmin):
    inlines = [MessageStackedInline, ]
    list_filter = ('status', 'assigned_to' )
    readonly_fields = ['screen_name', 'user_id', 'date_created']
    list_display = ('screen_name', 'date_created')
    search_fields = ("screen_name", "user_id", "status", "thread_messages__message")

    
    def get_readonly_fields(self, request, obj=None):
        try:
            user_group = request.user.groups.all()[0]
        except:
            return self.readonly_fields + ['assigned_to']
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
                            print(message)
                        except:
                            pass
                    if own_msg:
                        obj.message_id = str(own_msg.id)
                        obj.creator = True
                    obj.save()

    fieldsets = [
        (None, {
            'classes': ('suit-tab', 'suit-tab-general',),
            'fields': ['screen_name', 'user_id', 'date_created', 'status', 'assigned_to', 'email']
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

from django.views.generic.edit import FormView
from .forms import BulkSendEnquiryForm

class BulkSend(FormView):
    template_name = 'bulk_send_enquiry.html'
    form_class = BulkSendEnquiryForm
    success_url = '/admin/customerservice/enquiry/'

    def form_valid(self, form):
        form.send(self.kwargs['ids'])
        return HttpResponseRedirect(self.success_url)


class TransactionInline(admin.StackedInline):
    model = Transaction
    extra = 0
    readonly_fields = ["date", "fmj_date", "tnum", "title1", "title2", "title3",
                       "title4", "title5", "title6", "scomment", "stitle", "where", "who", "when",
                       "location", "usher1", "usher2", "account",]



class PurchaseItemInline(admin.StackedInline):
    model = PurchaseItem
    extra = 0
    readonly_fields = ['price_category', 'quantity', 'item_data']


class PurchaseAdmin(admin.ModelAdmin):
    inlines = [TransactionInline, PurchaseItemInline]
    extra = 0
    #list_filter = ['performance__show']
    search_fields = ('performance__show__name', 'performance__perf_code')

    def get_readonly_fields(self, request, obj=None):
        if self.declared_fieldsets:
            return flatten_fieldsets(self.declared_fieldsets)
        else:
            return list(set(
                [field.name for field in self.opts.local_fields] +
                [field.name for field in self.opts.local_many_to_many]
            ))

class PurchaseInLine(admin.StackedInline):
    model = Purchase
    extra = 0
    can_delete = False
    suit_classes = 'suit-tab suit-tab-purchase'

class AccountInline(admin.StackedInline):
    model = Account
    can_delete = False
    extra = 0
    suit_classes = 'suit-tab suit-tab-account'

    def get_readonly_fields(self, request, obj=None):
        if self.declared_fieldsets:
            return flatten_fieldsets(self.declared_fieldsets)
        else:
            return list(set(
                [field.name for field in self.opts.local_fields] +
                [field.name for field in self.opts.local_many_to_many]
            ))

class ProfileInLine(admin.StackedInline):
    model = UserProfile
    can_delete = False
    extra = 0
    suit_classes = 'suit-tab suit-tab-profile'

    def get_readonly_fields(self, request, obj=None):
        if self.declared_fieldsets:
            return flatten_fieldsets(self.declared_fieldsets)
        else:
            return list(set(
                [field.name for field in self.opts.local_fields] +
                [field.name for field in self.opts.local_many_to_many]))

class UserAdmin(AuthUserAdmin):
    inlines = [AccountInline, ProfileInLine, PurchaseInLine]
    suit_classes = 'suit-tab suit-tab-general'
    search_fields = ('username', 'first_name', 'last_name', 'email')


    fieldsets = (
        (None, {'fields': ('username', 'password'), 'classes': ('suit-tab', 'suit-tab-general',)}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email'), 'classes': ('suit-tab', 'suit-tab-general',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions'), 'classes': ('suit-tab', 'suit-tab-general',)}),

       # (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super(UserAdmin, self).get_fieldsets(request, obj)

    suit_form_tabs = (('general', 'Usuario'), ('account', 'Account'), ('profile', 'Profile'), ('purchase', 'Purchase'))

# unregister old user admin
admin.site.unregister(User)
# register new user admin
admin.site.register(User, UserAdmin)

admin.site.register(Bulletin, BulletinAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Thread, ThreadAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(TopicForm, TopicFormAdmin)
admin.site.register(Enquiry, EnquiryAdmin)
admin.site.register(Purchase, PurchaseAdmin)
admin.site.register(Account)