"""Tests for config and logging"""

import os
import unittest
from rabbit2ev.conf import Config


class ConfigLogCheck(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(ConfigLogCheck, self).__init__(*args, **kwargs)
        conf_file = "conf/rabbit2ev.sample.ini"
        self.conf = Config(conf_file) if self.check_conf(conf_file) else None
        self.level = ("DEBUG", "INFO", "WARN", "ERROR")

    def test_rabbitmq_user(self):
        self.assertIsNotNone(self.conf.rabbitmq_user)
        self.assertTrue(isinstance(self.conf.rabbitmq_user, str))

    def test_rabbitmq_pass(self):
        self.assertIsNotNone(self.conf.rabbitmq_pass)
        self.assertTrue(isinstance(self.conf.rabbitmq_pass, str))

    def test_rabbitmq_host(self):
        self.assertIsNotNone(self.conf.rabbitmq_host)
        self.assertTrue(isinstance(self.conf.rabbitmq_host, str))

    def test_rabbitmq_port(self):
        self.assertIsNotNone(self.conf.rabbitmq_port)
        self.assertTrue(isinstance(self.conf.rabbitmq_port, int))
        self.assertFalse(isinstance(self.conf.rabbitmq_port, str))

    def test_rabbitmq_queue(self):
        self.assertIsNotNone(self.conf.rabbitmq_queue)
        self.assertTrue(isinstance(self.conf.rabbitmq_queue, str))

    def test_log_level(self):
        self.assertIsNotNone(self.conf.log_level)
        self.assertTrue(isinstance(self.conf.log_level, str))
        self.assertIsNotNone(self.conf.log_level in self.level)

    def test_log_name(self):
        self.assertIsNotNone(self.conf.log_name)
        self.assertTrue(isinstance(self.conf.log_name, str))

    def test_log_handler(self):
        self.assertIsNotNone(self.conf.log_handler)
        self.assertTrue(isinstance(self.conf.log_handler, str))
        self.assertIsNotNone(self.conf.handler)

    def test_log_args(self):
        self.assertIsNotNone(self.conf.log_args)
        self.assertTrue(isinstance(self.conf.log_args, str))

    def test_log_class(self):
        self.assertIsNotNone(self.conf.log_class)
        self.assertTrue(isinstance(self.conf.log_class, str))

    def test_log_format(self):
        self.assertIsNotNone(self.conf.log_format)
        self.assertTrue(isinstance(self.conf.log_format, str))

    def test_log_datefmt(self):
        self.assertIsNotNone(self.conf.log_datefmt)
        self.assertTrue(isinstance(self.conf.log_datefmt, str))

    def check_conf(self, conf_file):
        if not os.path.isfile(conf_file) or not os.access(conf_file, os.R_OK):
            raise AssertionError(
                "File '%s' not exist nor readable" % conf_file)
        return True


if __name__ == "__main__":
    unittest.main()
