from django.contrib import admin
from django.conf import settings
# Register your models here.
from django.forms import TextInput, Textarea
from django.db import models
from customerservice.models import Thread, Message , Bulletin



class MessageStackedInline(admin.StackedInline):
    exclude = ('creator', 'sender', 'message_id')
    readonly_fields = ('user',)
    model = Message
    extra = 1
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows':6, 'cols':40, 'style': 'width: 800px;'})},
    }
   

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

    def save_formset(self, request, form, formset, change):
        formset.save()
        if change:
            for f in formset.forms:
                if f.changed_data:
                    obj = f.instance
                    obj.user = request.user
                    obj.save()

class BulletinAdmin(admin.ModelAdmin):
    list_display = ('user', 'text')
    fields = ('text', 'important')

    def save_model(self, request, obj, form, change):
        if not obj.user:
            obj.user = request.user
        obj.save()

admin.site.register(Bulletin, BulletinAdmin)
admin.site.register(Thread, ThreadAdmin)
#admin.site.register(Message) 