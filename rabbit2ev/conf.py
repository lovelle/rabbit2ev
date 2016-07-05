from log import setup_log_handlers
from ConfigParser import RawConfigParser


class Config(object):
    rabbitmq_user = 'guest'
    rabbitmq_pass = 'guest'
    rabbitmq_host = 'localhost'
    rabbitmq_port = 5672
    rabbitmq_queue = 'default'
    log = None
    log_name = 'rabbit2ev'
    log_level = 'DEBUG'
    log_handler = 'console'
    log_args = 'FileHandler'
    log_class = 'StreamHandler'
    log_format = None
    log_datefmt = None

    def __init__(self, conf):
        self.config = conf
        self.parser = RawConfigParser()
        self.log = None
        self.load()
        self.set_conf()
        self.set_logger()

    def load(self):
        self.parser.read(self.config)

    def set_conf(self):
        self.rabbitmq_user = self.parser.get('rabbitmq', 'user')
        self.rabbitmq_pass = self.parser.get('rabbitmq', 'pass')
        self.rabbitmq_host = self.parser.get('rabbitmq', 'host')
        self.rabbitmq_port = int(self.parser.get('rabbitmq', 'port'))
        self.rabbitmq_queue = self.parser.get('rabbitmq', 'queue')
        self.rabbit2ev_plugin = self.parser.get('rabbit2ev', 'plugin')
        self.rabbit2ev_domain = self.parser.get('rabbit2ev', 'domain')
        self.log_name = self.parser.get('loggers', 'name')
        self.log_level = self.parser.get('loggers', 'level')
        self.log_handler = self.parser.get('loggers', 'handler')
        self.handler = "loggers:handler_%s" % self.log_handler
        self.log_args = self.parser.get(self.handler, 'args')
        self.log_class = self.parser.get(self.handler, 'class')
        self.log_format = self.parser.get('loggers:formatter', 'format')
        self.log_datefmt = self.parser.get('loggers:formatter', 'datefmt')

    def set_logger(self):
        self.log = setup_log_handlers(
            level=self.log_level, name=self.log_name,
            log_args=self.log_args, log_class=self.log_class,
            datefmt=self.log_datefmt, formfmt=self.log_format
        )
