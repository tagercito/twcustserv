from django.db import models
from django.db.models.signals import post_save
import twitter
from django.conf import settings

api = twitter.Api(consumer_key=settings.CONSUMER_KEY, consumer_secret=settings.CONSUMER_SECRET, access_token_key=settings.ACCESS_TOKEN_KEY, access_token_secret=settings.ACCESS_TOKEN_SECRET)  


#create a choice field inside the class
OPEN = 'OP'
PENDING = 'PE'       
CLOSED = 'CL' 

TICKET_STATUS_CHOICES = (
    (OPEN,'Open'),
    (PENDING,'Pending'),
    (CLOSED,'Closed'),
)



class Thread(models.Model):
    screen_name = models.CharField(max_length=100)
    user_id = models.CharField(max_length=140)
    date_created = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=TICKET_STATUS_CHOICES, default=OPEN)
    assigned_to = models.ForeignKey('auth.User', null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Tweets'
        verbose_name_plural = 'Tweets'

    def __unicode__(self):
        return self.screen_name

class Message(models.Model):
    creator = models.BooleanField(default=False)
    thread = models.ForeignKey(Thread, related_name="thread_messages")
    message = models.TextField()
    sender = models.CharField(max_length=140, null=True, blank=True)
    message_id = models.CharField(max_length=20, null=True, blank=True)
    date_created = models.DateTimeField(auto_now=True)
    user = models.ForeignKey('auth.User', null=True, blank=True)

    def __unicode__(self):
        return self.message_id if self.message_id else ''

class Bulletin(models.Model):
    user = models.ForeignKey('auth.User', null=True, blank=True)
    text = models.TextField()
    date_created = models.DateTimeField(auto_now=True)
    important = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Noticias'
        verbose_name_plural = 'Noticias'

    def __unicode__(self):
        return u'%s-%s' % (self.user, self.important)


class Pull(models.Model):
    date = models.DateTimeField(auto_now=True)
    message_id = models.CharField(max_length=255)

    def __unicode__(self):
        return u'%s - %s' % (str(self.date), str(self.message_id))



FIELD_TYPE_CHOICES = (
    ("email", "email"),
    ("text", "text"),
    ("file", "file"),
)

class Topic(models.Model):
    topic = models.ForeignKey('Topic', null=True, blank=True, related_name="topic_child")
    title = models.CharField(max_length=255)
    body = models.TextField()
    form = models.ForeignKey('TopicForm', null=True, blank=True)

    def __str__(self):
        return '%s' % self.title


class TopicForm(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    def get_form(self):
        res = []
        for field in self.form_fields.all():
            data = {
                "name": field.name,
                "field_type": field.field_type
            }
            res.append(data)
        return res

class TopicField(models.Model):
    name = models.CharField(max_length=255)
    field_type = models.CharField(max_length=50, choices=FIELD_TYPE_CHOICES)
    form = models.ForeignKey("TopicForm", related_name="form_fields")

    def __str__(self):
        return self.name

class Enquiry(models.Model):
    topic = models.ForeignKey("Topic")
    enquiry = models.TextField()
    email = models.CharField(max_length=255)
    file = models.FileField(upload_to='enquiry', null=True, blank=True)
    date = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=False)
    user_id = models.CharField(max_length=255)


    def image_thumb(self):
        return '<img src="/media/%s" width="100" height="100" />' % (self.file)

    image_thumb.allow_tags = True

class EnquiryResponse(models.Model):
    creator = models.BooleanField(default=False)
    thread = models.ForeignKey(Enquiry)
    message = models.TextField()
    sender = models.CharField(max_length=140, null=True, blank=True)
    date_created = models.DateTimeField(auto_now=True)
    user = models.ForeignKey('auth.User', null=True, blank=True)
    message_id = models.CharField(max_length=255, null=True, blank=True)
    user = models.ForeignKey('auth.User', null=True, blank=True)


    def __unicode__(self):
        return u'%s' % str(self.date_created)
