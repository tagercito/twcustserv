import poplib
import re
from email import parser
from .models import Enquiry, EnquiryResponse

class EmailClient(object):

    def __init__(self, user, password):
        self.user = user
        self.password = password

    def connect(self):
        self.pop_conn = poplib.POP3_SSL('pop.gmail.com')
        self.pop_conn.user(self.user)
        self.pop_conn.pass_(self.password)
        print self.pop_conn.getwelcome()
        print self.pop_conn.stat()

    def get_emails(self):
        messages = [self.pop_conn.retr(i) for i in range(1, len(self.pop_conn.list()[1]) + 1)]
        messages = ["\n".join(mssg[1]) for mssg in messages]
        return [parser.Parser().parsestr(mssg) for mssg in messages]

    def parse_emails(self):
        messages = self.get_emails()
        for message in messages:
            self.parse_message(message)
        self.disconnect()

    def get_header(self, message, header_type):
        for header in message._headers:
            if header[0] == header_type:
                return header[1]
        return False

    def get_payload(self, message):
        if message.is_multipart():
            for payload in message.get_payload():
                return payload.get_payload()
        else:
            return message.get_payload()

    def parse_message(self, message):
        message_id = self.get_header(message, 'In-Reply-To')
        if message_id:
            try:
                enq = EnquiryResponse.objects.get(message_id=message_id)
            except:
                print 'invalid enquiry'
                return
            else:
                payload = self.get_payload(message)
                message = EnquiryResponse.objects.create(contact=enq.contact,
                                                         message=payload,
                                                         message_id=self.get_header(message, 'Message-ID'))

    def disconnect(self):
        self.pop_conn.quit()

