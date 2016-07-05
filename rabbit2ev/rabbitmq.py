import time
import logging

from conf import Config

# nullmailer plugin
from plugins.nullmailer import NullMailer
# TODO: remove this
from exception import NullMailerErrorPipe

try:
    import pika
except ImportError:
    raise Exception("App requires 'pika' library installed")

try:
    import json
except ImportError:
    try:
        import simplejson as json
    except ImportError:
        raise Exception(
            "App requires the 'json' or 'simplejson' library installed")


logger = logging.getLogger(__name__)


class RabbitHandler(object):

    log = logger
    config = None
    __shutdown = False
    active_plugins = {
        "nullmailer": NullMailer()
    }

    def __init__(self):
        self.conf = None
        self.channel = None
        self.started = time.time()

    def connect(self):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=self.conf.rabbitmq_host,
                port=self.conf.rabbitmq_port,
                credentials=self.credentials(),
                ssl=False)
        )
        self.channel = connection.channel()

    def credentials(self):
        return pika.PlainCredentials(
            self.conf.rabbitmq_user, self.conf.rabbitmq_pass)

    def bind_consumers(self):
        self.log.debug("RabbitMQ connection established")
        self.channel.basic_consume(self.consume,
                                   queue=self.conf.rabbitmq_queue)

    def consume(self, channel, method, properties, data):
        self.log.info("new request received")
        try:
            self.process(json.loads(data, strict=False), method)
        except NullMailerErrorPipe as e:
            self.log.warn(
                "Cannot trigger signal, probably nullmailer is not running")
            self.do_ack(method, channel)
        except ValueError as e:
            # What can we do here? Send ack.
            # Fow now, nothing can be done here.
            self.log.error("Invalid data format: %s" % e)
            self.do_ack(method, channel)
        except Exception as e:
            self.log.error(e)
        else:
            self.do_ack(method, channel)

    def do_ack(self, method, channel):
        if self.__shutdown is not True:
            self.log.debug("rabbit sending ACK msg queued")
            channel.basic_ack(delivery_tag=method.delivery_tag)

    def set_procesor(self, callback):
        self.process = callback

    def process(self, data, method):
        self.log.debug("rabbitmq recv: %s" % data)
        self.handler[self.conf.rabbit2ev_plugin].sendmail(data)

    def channel_consume(self):
        self.log.debug("listening from queue '%s'" % self.conf.rabbitmq_queue)
        self.channel.start_consuming()

    def start_consuming(self):
        self.log.debug("connecting to RabbitMQ...")
        try:
            self.connect()
            self.bind_consumers()
            self.channel_consume()
        except pika.exceptions.ProbableAuthenticationError:
            self.log.error(
                "Client disconnected, probable authentication error")
        except pika.exceptions.AMQPError as e:
            self.log.error("%s: %s" % (e.__class__.__name__, str(e)))
        except Exception as e:
            self.log.error("Unknown Error: %s " % str(e))

    def set_handler(self):
        self.handler = self.get_plugin()

    def set_conf(self):
        self.conf = Config(self.config)
        self.log = self.conf.log

    def start(self):
        self.set_conf()
        self.set_handler()
        self.log.info("Server rabbit2ev started")
        self.start_consuming()

    def stop(self):
        self.log.warn("Signal stopped received")
        self.__shutdown = True
        self.channel.stop_consuming()

    def get_plugin(self):
        self.check_plugin()
        return {
            self.conf.rabbit2ev_plugin:
                self.active_plugins[self.conf.rabbit2ev_plugin]
        }

    def check_plugin(self):
        if self.conf.rabbit2ev_plugin not in self.active_plugins:
            raise ValueError(
                "plugin '%s' not exist" % self.conf.rabbit2ev_plugin)

    def __del__(self):
        self.log.info("Server rabbit2mq finished or destroyed")
