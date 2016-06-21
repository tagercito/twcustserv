from django import template
from customerservice.models import Contact, Bulletin
import json
register = template.Library()


def get_thread_count(status):
    thread_count = Contact.objects.filter(type=Contact.THREAD,
                                          status=status).count()
    return thread_count

def get_messages_since_last_login(user):
    last_login = user.last_login
    threads = Contact.objects.filter(
        type=Contact.THREAD,
        thread_messages__date_created__lte=last_login
    ).distinct().order_by("-thread_messages__date_created")
    return threads


def get_thread_chart(status):
    open_t = {
        'value': Contact.objects.filter(type=Contact.THREAD,
                                        status='OP').count(),
        'color': "#46BFBD",
        'highlight': "#5AD3D1",
        'label': "OPEN"
    }
    closed_t = {
        'value': Contact.objects.filter(type=Contact.THREAD,
                                        status='CL').count(),
        'color': "#F7464A",
        'highlight': "#FF5A5E",
        'label': "CLOSED"
    }
    pending_t = {
        'value': Contact.objects.filter(type=Contact.THREAD,
                                        status='PE').count(),
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
    for thread in Contact.objects.filter(type=Contact.THREAD,
                                         status='OP'):
        if thread.assigned_to:
            if not users.get(thread.assigned_to.username, None):
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
