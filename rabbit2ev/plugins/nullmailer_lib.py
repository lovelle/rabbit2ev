import os
import time

import uuid
from base64 import b64encode


class HandleRequest(object):

    def __init__(self, tmp, queue, counter):
        self.filename = "%f_%s_%d" % (
            time.time(), time.strftime("%d.%m.%Y-%H.%M.%S"), counter)
        self.tmp_file = "%s/%s" % (tmp, self.filename)
        self.spool_file = "%s/%s" % (queue, self.filename)

    def start(self, data):
        self.factory = BasicMail(data, self.tmp_file)
        self.__set_actions()
        self.factory.construct_building()

    def __set_actions(self):
        self.factory.register(1, self.factory.set_head)
        self.factory.register(2, self.factory.set_basic)
        self.factory.register(3, self.factory.set_subject)
        self.factory.register(4, self.factory.set_body)
        self.factory.register(5, self.factory.set_content)
        self.factory.register(6, self.factory.finish)

    def tearDown(self):
        pass


class Mail(object):

    crlf = "\n"
    slice = ","

    def __init__(self):
        self.unique = uuid.uuid4()
        # TODO: replace with config para
        self.domain = "@example.com"
        self.actions = dict()

    def register(self, name, method):
        self.actions[name] = method

    def set_basic(self):
        self.f.write("Date: " + self.rfc2822() + self.crlf)
        self.f.write("X-Mailer: " + self.mailer() + self.crlf)
        self.f.write(
            "Message-Id: <" + self.uid() + self.domain + ">" + self.crlf)
        self.f.write("From: <" + self.mailfrom() + ">" + self.crlf)

    def set_head(self):
        self.f = open(self.filename, "w")
        os.chmod(self.filename, 0600)
        self.f.write(self.localfrom() + self.crlf)
        [self.f.write(i) for i in self.get_to()]
        [self.f.write(j) for j in self.get_cc()] if self.get_cc() else None
        [self.f.write(k) for k in self.get_bcc()] if self.get_bcc() else None
        self.f.write(self.crlf)

    def set_subject(self):
        self.f.write(self.subject_encoded() + self.crlf)

    def set_body(self):
        if self.to() and self.to() != "":
            self.f.write("To: " + ", ".join('<{0}>'.format(i)
                         for i in self.to()) + self.crlf)
        if self.cc() and self.cc() != "":
            self.f.write("Cc: " + ", ".join('<{0}>'.format(c)
                         for c in self.cc()) + self.crlf)

        self.set_attachment() if self.attachment() else self.set_standard()

    def set_attachment(self):
        self.f.write("MIME-Version: 1.0" + self.crlf)
        self.f.write("Content-Type: multipart/mixed; boundary=%s%s" %
                     (str(self.unique), self.crlf))
        self.f.write("Content-Disposition: inline" + self.crlf)
        self.spare_line()
        self.f.write("Content-Type: application/octet-stream" + self.crlf)
        self.f.write("Content-Disposition: attachment; filename=%s %s" %
                     (self.attachment_file(), self.crlf))
        self.f.write("Content-Transfer-Encoding: base64" + self.crlf)
        self.f.write(self.crlf + b64encode(self.attachment_content()))

    def set_standard(self):
        self.f.write("Content-Type: text/plain; charset=UTF-8" + self.crlf)
        self.f.write("Content-Transfer-Encoding: quoted-printable" + self.crlf)

    def set_content(self):
        if self.attachment():
            self.spare_line()
            self.f.write(
                "Content-Type: text/plain; charset=us-ascii" + self.crlf)
            self.f.write("Content-Disposition: inline" + self.crlf)

        self.f.write(self.crlf + self.content() + self.crlf)

    def finish(self):
        self.f.close()

    def spare_line(self):
        self.f.write(self.crlf + "--" + str(self.unique) + self.crlf)


class BasicMail(Mail):

    def __init__(self, data, filename):
        super(BasicMail, self).__init__()
        self.data = data
        self.filename = filename

    def construct_building(self):
        [self.actions[k]() for k in sorted(self.actions)]

    def rfc2822(self):
        return time.strftime("%a, %d %b %Y %X +0000", time.gmtime())

    def mailfrom(self):
        # TODO: replace with config param
        return self.data.get('from', 'no-reply@example.com')

    def mailer(self):
        return "rabbit2ev"

    def uid(self):
        return self.unique.bytes.encode('base64')[:20]

    def localfrom(self):
        return "%s@%s" % ('mail', os.uname()[1])

    def subject_encoded(self):
        return "Subject: =?UTF-8?B?%s?=" % b64encode(self.subject())

    def subject(self):
        return self.data.get('subject', 'No subject').encode('utf8')

    def attachment(self):
        return self.data.get('attachment')

    def attachment_content(self):
        return self.data['attachment'].get('body')

    def attachment_file(self):
        return self.data['attachment'].get('filename', 'attachment.txt')

    def content(self):
        return self.data.get('body').encode('utf8')

    def get_to(self):
        return [(str(i) + self.crlf)
                for i in self.to() if i is not None and i != ""]

    def get_cc(self):
        return [(str(i) + self.crlf)
                for i in self.cc() if i is not None and i != ""]

    def get_bcc(self):
        return [(str(i) + self.crlf)
                for i in self.bcc() if i is not None and i != ""]

    def to(self):
        return self.formatter(self.data.get('to'))

    def cc(self):
        return self.formatter(self.data.get('cc', ''))

    def bcc(self):
        return self.formatter(self.data.get('bcc', ''))

    def formatter(self, x):
        return filter(None, x.strip().split(self.slice))\
            if isinstance(x, basestring) else x
