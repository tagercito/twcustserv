from django.db import models
from django.db.models.signals import post_save
import twitter
from django.conf import settings
from django.contrib.auth.models import User

api = twitter.Api(consumer_key=settings.CONSUMER_KEY,
                  consumer_secret=settings.CONSUMER_SECRET,
                  access_token_key=settings.ACCESS_TOKEN_KEY,
                  access_token_secret=settings.ACCESS_TOKEN_SECRET)  


#create a choice field inside the class
OPEN = 'OP'
PENDING = 'PE'
CLOSED = 'CL' 

TICKET_STATUS_CHOICES = (
    (OPEN, 'Open'),
    (PENDING, 'Pending'),
    (CLOSED, 'Closed'),
)


class Contact(models.Model):

    OPEN = 'OP'
    PENDING = 'PE'
    CLOSED = 'CL' 

    TICKET_STATUS_CHOICES = (
        (OPEN, 'Open'),
        (PENDING, 'Pending'),
        (CLOSED, 'Closed'),
    )

    THREAD = 0
    ENQUIRY = 1
    CONTACT_TYPE_CHOICES = (
        (THREAD, 'Twitter'),
        (ENQUIRY, 'Enquiry')
    )

    # common fields
    email = models.EmailField(null=True, blank=True)
    status = models.CharField(max_length=2, choices=TICKET_STATUS_CHOICES,
                              default=OPEN)
    created = models.DateTimeField(auto_now=True)
    user = models.ForeignKey('auth.User', null=True, blank=True)

    # non common fields topic
    topic = models.ForeignKey("Topic")
    enquiry = models.TextField()
    file = models.FileField(upload_to='enquiry', null=True, blank=True)

    # non common fields thread
    screen_name = models.CharField(max_length=100)
    user_id = models.CharField(max_length=140)
    assigned_to = models.ForeignKey('auth.User', null=True, blank=True,
                                    related_name="threads_assigned")

    # type of contact
    type = models.PositiveSmallIntegerField(choices=CONTACT_TYPE_CHOICES)

    def save(self, *args, **kwargs):
        if self.email:
            try:
                self.user = User.objects.get(email=self.email)
            except:
                pass
        super(Contact, self).save(*args, **kwargs)

    def image_thumb(self):
        if self.file is not None:
            path = "/media/{}".format(self.file)
        else:
            path = ""
        return '<img src="{}" width="100" height="100" />'.format(path)

    image_thumb.allow_tags = True


class Thread(models.Model):

    email = models.EmailField(null=True, blank=True)
    status = models.CharField(max_length=2, choices=TICKET_STATUS_CHOICES,
                              default=OPEN)
    date_created = models.DateTimeField(auto_now=True)
    w_user = models.ForeignKey('auth.User', null=True, blank=True,
                               related_name="tweet_user")
    screen_name = models.CharField(max_length=100)
    user_id = models.CharField(max_length=140)
    assigned_to = models.ForeignKey('auth.User', null=True, blank=True,
                                    related_name="assigned_to_thread")

    def save(self, *args, **kwargs):
        if self.email:
            try:
               user = User.objects.get(email=self.email)
            except:
                pass
            else:
                self.w_user = user

        super(Thread, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Tweets'
        verbose_name_plural = 'Tweets'

    def __str__(self):
        return self.screen_name


class Enquiry(models.Model):
    email = models.CharField(max_length=255)
    status = models.CharField(max_length=2, choices=TICKET_STATUS_CHOICES,
                              default=OPEN)
    date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey('auth.User', null=True, blank=True)
    topic = models.ForeignKey("Topic")
    enquiry = models.TextField()
    file = models.FileField(upload_to='enquiry', null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.email:
            try:
               user =  User.objects.get(email=self.email)
            except:
                pass
            else:
                self.user = user

        super(Enquiry, self).save(*args, **kwargs)

    def image_thumb(self):
        return '<img src="/media/%s" width="100" height="100" />' % (self.file)

    image_thumb.allow_tags = True


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
    topic = models.ForeignKey('Topic', null=True, blank=True,
                              related_name="topic_child")
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
