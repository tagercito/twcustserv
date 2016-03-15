from django.conf.urls import patterns, include, url
from .views import TopicTemplateView, TopicView, FileUploadView

urlpatterns = patterns('',
    url(r'^$', TopicTemplateView.as_view(), name="topic_template_view"),
    url(r'^topics/$', TopicView.as_view(), name="topic_view"),
    url(r'^file/$', FileUploadView.as_view(), name="file_view"),
)


