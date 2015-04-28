from django.contrib import admin
from django.conf import settings
# Register your models here.
from django.forms import TextInput, Textarea
from django.db import models
from customerservice.models import Thread, Message , Bulletin

=======
import twitter
from django.conf import settings



def split(s, signature, l=[]): #funcion recursiva que parte el texto en strings de 140 caracteres
    if len(s) < 140-len(signature):
        l.append(s+signature)
        return l
    l.append(s[:140-len(settings.CONTINUA)]+settings.CONTINUA)
    return split(s[140-len(settings.CONTINUA):], signature,  l)


>>>>>>> 2957113fc789f4ca0b1f0cdb3a2c9b6d91ce8d35

class MessageStackedInline(admin.StackedInline):
    exclude = ('creator', 'sender', 'message_id')
    readonly_fields = ('user',)
    model = Message
    extra = 1
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 6, 'cols': 40, 'style': 'width: 600px;'})},
    }
   

class ThreadAdmin(admin.ModelAdmin):
    inlines = [MessageStackedInline, ]
     
=======
    list_filter = ('status', 'assigned_to' )
    readonly_fields = ['screen_name', 'user_id', 'date_created']
>>>>>>> 2957113fc789f4ca0b1f0cdb3a2c9b6d91ce8d35
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





