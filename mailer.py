import signal
from rabbit2ev.rabbitmq import RabbitHandler


def main():
    def signal_handler(signal, frame):
        server.stop()

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    server = RabbitHandler()
    server.config = 'conf/rabbit2mail.ini'
    server.start()

if __name__ == '__main__':
    main()
