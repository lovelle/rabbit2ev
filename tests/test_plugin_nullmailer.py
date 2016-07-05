"""Tests for nullmailer"""

import os
import unittest

import uuid
import shutil

from rabbit2ev.plugins.nullmailer import NullMailer
from rabbit2ev.exception import NullMailerErrorPipe, NullMailerErrorPool

UID = uuid.uuid4()


class ConfigLogCheck(unittest.TestCase):

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
    test_dir = "/tmp/test-rabbit2ev-%s" % str(UID)

    def __init__(self, *args, **kwargs):
        super(ConfigLogCheck, self).__init__(*args, **kwargs)
        self.nullmailer = NullMailer()
        self.nullmailer.tmp = "%s/tmp" % self.test_dir
        self.nullmailer.queue = "%s/queue" % self.test_dir

    def setUp(self):
        if not os.path.isdir(self.nullmailer.tmp):
            os.makedirs(self.nullmailer.tmp)

        if not os.path.isdir(self.nullmailer.queue):
            os.makedirs(self.nullmailer.queue)

    def test_nullmailer_tmp(self):
        self.assertTrue(isinstance(self.nullmailer.tmp, str))
        self.checkFile(self.nullmailer.tmp, 'isabs')

    def test_nullmailer_queue(self):
        self.assertTrue(isinstance(self.nullmailer.queue, str))
        self.checkFile(self.nullmailer.queue, 'isabs')

    def test_nullmailer_trigger(self):
        self.assertTrue(isinstance(self.nullmailer.trigger, str))
        self.checkFile(self.nullmailer.trigger, 'isabs')

    def test_nullmailer_fsync_pool(self):
        self.assertIsNone(self.nullmailer.fsync_pool())

    def test_nullmailer_trigger_pipe(self):
        with self.assertRaises(NullMailerErrorPipe):
            self.nullmailer.trigger_pipe()

    def test_nullmailer_fsync_pool_fail_queue(self):
        self.nullmailer.queue = "invalid"
        with self.assertRaises(NullMailerErrorPool):
            self.nullmailer.fsync_pool()

    def test_nullmailer_sendmail(self):
        with self.assertRaises(NullMailerErrorPipe):
            self.nullmailer.sendmail(self.data)

        for f in os.listdir(self.nullmailer.queue):
            self.checkFile(self.nullmailer.queue + "/" + f, 'isfile')

    def checkFile(self, file, action):
        if not getattr(os.path, action)(file):
            raise AssertionError("'%s' not exist nor readable" % file)

    def tearDown(self):
        shutil.rmtree(self.test_dir)


if __name__ == "__main__":
    unittest.main()
