from django import template
from customerservice.models import Thread, Bulletin
import json
register = template.Library()


def get_thread_count(status):
    thread_count = Thread.objects.filter(status=status).count()
    return thread_count

def get_messages_since_last_login(user):
    last_login = user.last_login
    threads = Thread.objects.filter(message__date_created__lte=last_login).distinct()
    return threads


def get_thread_chart(status):
    open_t = {
        'value': Thread.objects.filter(status='OP').count(),
        'color': "#46BFBD",
        'highlight': "#5AD3D1",
        'label': "OPEN"
    }
    closed_t = {
        'value': Thread.objects.filter(status='CL').count(),
        'color': "#F7464A",
        'highlight': "#FF5A5E",
        'label': "CLOSED"
    }
    pending_t = {
        'value': Thread.objects.filter(status='PE').count(),
        'color': "#FDB45C",
        'highlight': "#FFC870",
        'label': "PENDING"
    }
    return json.dumps([open_t, closed_t, pending_t])



def get_lastest_bulletins(user):
    return Bulletin.objects.filter(date_created__lte=user.last_login)

def get_important_bulletins(user):
    return Bulletin.objects.filter(important=True)

def get_user_ticket_quantity(user):
    users = dict(nadie=0)
    for thread in Thread.objects.filter(status='OP'):
        if thread.assigned_to:
            if not users.get(thread.assigned_to.username):
                users[thread.assigned_to.username] = 1
            else:
                users[thread.assigned_to.username] += 1
        else:
            users['nadie'] += 1
    return users


register.filter('get_thread_count', get_thread_count)
register.filter('get_messages_since_last_login', get_messages_since_last_login)
register.filter('get_thread_chart', get_thread_chart)
register.filter('get_lastest_bulletins', get_lastest_bulletins)
register.filter('get_important_bulletins', get_important_bulletins)
register.filter('get_user_ticket_quantity', get_user_ticket_quantity)
