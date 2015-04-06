from django.contrib import admin
from django.conf import settings
# Register your models here.

from customerservice.models import Thread, Message 



class MessageStackedInline(admin.StackedInline):
    exclude = ('creator','sender', 'message_id')

    model = Message
    extra = 1


class ThreadAdmin(admin.ModelAdmin):
    inlines = [MessageStackedInline, ]

    readonly_fields = ('screen_name', 'user_id', 'date_created')

    def suit_row_attributes(self, Thread, request):
        css_class = {
            settings.CLOSED: 'error',
            settings.PENDING: 'warning',
            settings.OPEN: 'success'}.get(Thread.status)
        if css_class:
            return {'class': css_class, 'data': Thread}



admin.site.register(Thread, ThreadAdmin)
admin.site.register(Message) 