from django.conf.urls import url
from .views import TopicTemplateView, TopicView, FileUploadView

urlpatterns = [
    url(r'^$', TopicTemplateView.as_view(), name="topic_template_view"),
    url(r'^topics/$', TopicView.as_view(), name="topic_view"),
    url(r'^file/$', FileUploadView.as_view(), name="file_view"),
]


