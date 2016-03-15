from django.views.generic import TemplateView, View
from django.shortcuts import render
from .models import Topic, Enquiry
from django.http import HttpResponse
import json


class TopicTemplateView(TemplateView):
    template_name = 'enquiry.html'


class FileUploadView(View):

    def post(self, request):
        try:
            enq = Enquiry.objects.get(pk=request.POST['enquiry'])
        except:
            raise
        else:
            enq.file = request.FILES['file']
            enq.save()
        return HttpResponse(1)

class TopicView(View):

    def get_subtopics(self, topic):
        topic_info = {"pk": topic.pk,
                      "title": topic.title,
                      "body": topic.body,
                      "children": []}

        for children in topic.topic_child.all():
            topic_info['children'].append(self.get_subtopics(children))

        if topic.form:
            topic_info['form'] = topic.form.get_form()

        return topic_info


    def get(self, request):
        parent_topics = Topic.objects.filter(topic=None)
        response = []
        for topic in parent_topics:
            topic_info = self.get_subtopics(topic)
            response.append(topic_info)
        return HttpResponse(json.dumps(response))

    def parse_request(self, data):
        res = ''
        for key, value in data.iteritems():
            if str(key) != 'topic' or str(key) != 'email':
                res += ' = '.join((key, value)) + '\n'
        return res


    def post(self, request):
        text = self.parse_request(request.POST)
        enq = Enquiry.objects.create(topic=Topic.objects.get(pk=request.POST['topic']),
                                     enquiry=text,
                                     email=request.POST['email'])
        return HttpResponse(enq.pk)