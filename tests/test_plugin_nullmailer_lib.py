"""Tests for libs"""

import unittest

from rabbit2ev.plugins.nullmailer_lib import Mail, BasicMail

import uuid
from base64 import b64encode


class MailTest(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(MailTest, self).__init__(*args, **kwargs)
        self.mail = Mail()

    def test_libs_mail_crlf(self):
        self.assertEqual(self.mail.crlf, "\n")

    def test_libs_mail_slice(self):
        self.assertEqual(self.mail.slice, ",")

    def test_libs_mail_domain(self):
        self.assertEqual(self.mail.domain, "@example.com")

    def test_libs_mail_unique(self):
        self.assertIsInstance(self.mail.unique, uuid.UUID)


class BasicMailTest(unittest.TestCase):

    file = "/var/tmp/test_%s" % str(uuid.uuid4())
    data = {
        "body": "This is just a test",
        "to": "me@example.com",
        "cc": "alice@example.com, bob@example.com",
        "bcc": ["hiden@info.com", "soviet@union.com"],
        "subject": "Hallo",
        "attachment": {
            "body": "file content",
            "filename": "test.txt"
        }
    }

    def __init__(self, *args, **kwargs):
        super(BasicMailTest, self).__init__(*args, **kwargs)
        self.basicmail = BasicMail(self.data, self.file)

    # def test_lib_basicmail_rfc2822(self):
    #     x = self.basicmail.rfc2822()

    def test_lib_basicmail_mailer(self):
        self.assertEqual(self.basicmail.mailer(), "rabbit2ev")

    def test_lib_basicmail_uid(self):
        self.assertTrue(len(self.basicmail.uid()) == 20)

    def test_lib_basicmail_subject(self):
        self.assertEqual(self.basicmail.subject(), self.data.get('subject'))
        del self.data['subject']
        self.assertEqual(self.basicmail.subject(), "No subject")

    def test_lib_basicmail_subject_encoded(self):
        self.assertEqual(
            self.basicmail.subject_encoded(),
            "Subject: =?UTF-8?B?%s?=" % b64encode(
                self.data.get('subject', "No subject")
            )
        )

    def test_lib_basicmail_attachment(self):
        self.assertEqual(self.basicmail.attachment(), dict(
            body=self.data['attachment']['body'],
            filename=self.data['attachment']['filename'])
        )

    def test_lib_basicmail_attachment_content(self):
        self.assertEqual(
            self.basicmail.attachment_content(),
            self.data['attachment']['body'])

    def test_lib_basicmail_attachment_file(self):
        self.assertEqual(
            self.basicmail.attachment_file(),
            self.data['attachment']['filename'])

    def test_lib_basicmail_content(self):
        self.assertEqual(self.basicmail.content(), self.data['body'])

    def test_lib_basicmail_to(self):
        self.assertTrue(isinstance(self.basicmail.to(), list))
        self.assertTrue(len(self.basicmail.to()) == 1)

    def test_lib_basicmail_cc(self):
        self.assertTrue(isinstance(self.basicmail.cc(), list))
        self.assertTrue(len(self.basicmail.cc()) == 2)

    def test_lib_basicmail_bcc(self):
        self.assertTrue(isinstance(self.basicmail.bcc(), list))
        self.assertTrue(len(self.basicmail.bcc()) == 2)

    def test_lib_basicmail_formatter_recv_str(self):
        self.assertTrue(
            len(self.basicmail.formatter('foo,bar,baz')) == 3)
        self.assertTrue(isinstance(
            self.basicmail.formatter('foo,bar,baz'), list)
        )

    def test_lib_basicmail_formatter_recv_list(self):
        self.basicmail.formatter(['foo', 'bar', 'baz'])
        self.assertTrue(
            len(self.basicmail.formatter(['foo', 'bar', 'baz'])) == 3)
        self.assertTrue(isinstance(
            self.basicmail.formatter(['foo', 'bar', 'baz']), list)
        )


if __name__ == "__main__":
    unittest.main()
