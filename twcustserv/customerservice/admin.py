from django.contrib import admin

# Register your models here.

from customerservice.models import Thread, Message 



class MessageStackedInline(admin.StackedInline):
	model = Message
	extra = 1

class ThreadAdmin(admin.ModelAdmin):
	inlines = [MessageStackedInline,]

admin.site.register(Thread, ThreadAdmin)
admin.site.register(Message) 