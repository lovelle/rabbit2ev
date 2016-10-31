Rabbit2Ev
=========
Receive messages from RabbitMQ and bind them to an event handler.

Rabbit2ev is a python daemon, listening for json formatted events to process them.
e.g sending emails asynchronous.

The main purpose of this daemon is to have a simple and unified set of workers ready
to process incoming events using RabbitMQ as a message interface for receiving
the event binded to any plugin available.

Nowadays, the only one plugin developed is for sending mails, but, others plugins with
differents protocols could be implemented.

`json` is the only allowed format for processing events.

## Install

To run rabbit2ev from source, clone this repo to your machine, compile and test it:
By default, Makefile will attempt to build a virtualenv folder with dependencies in `venv`.

```sh
$ git clone https://github.com/lovelle/rabbit2ev.git
$ cd rabbit2ev
$ make
```

## Testing

Before running the tests, make sure you have your settings in config file.
(config file format and structure will be tested too)

```sh
$ cp conf/rabbit2ev.sample.ini conf/rabbit2ev.ini
$ make test
```

## Running the default server

You can either choose to run the server standalone
or with a process manager like [supervisor](http://supervisord.org/)

Remember to edit your config file with your custom settings.

```sh
$ editor conf/rabbit2ev.ini
# Standalone run
$ make run
```

## Starting custom server plugin

To start your own server with your custom plugin (event handler), just
need import the lib, set the config and start it and thats' all ;).

```python
from rabbit2ev.rabbitmq import RabbitHandler

mail = RabbitHandler()
mail.config = 'conf/rabbit2mail.ini' # configure the plugin you need
mail.start()
```

Since the idea is to have multiple server instances running with each
configuration and with his own queue, if you want to have multiple
server instances, supervisor process manager is the recommended way.


## 1. Plugins (mail)

For now, the only one handler is [nullmailer](https://github.com/bruceg/nullmailer)
client file generator.

### 1.1 Mail plugin usage

rabbit2ev will be listen in a queue in RabbitMq, so you can send an email,
publishing a message into the proper queue.

The data format to send an email is **JSON**.

The only mandatory keys you need to define an email structure in json, are
**to** and **body**, wheter you don't define the rest of the keys, will be
setted by default.

e.g: If you dont specify the key **from**, this one will be "no-reply@_{domain.ltd}_"
_{domain.ltd}_ will be replace with whatever you have in your config in "domain" config parameter.

e.g how send email:

```json
{"body": "Hallo mein Freund, das ist nur ein Test", "to": "Leiter@berlin.de", "subject": "Hallo"}
```

e.g how send email with attachment:

**Warn:** __body__ key is mandatory in order to send an attachment.

```json
{"body": "Hello my friend, this is just a test", "to": "test@example.com", "subject": "Hallo", "attachment": [{"body": "file content", "filename": "test.txt"}] }
```

To set multiple addresses, the format could be string or a list, both cases are valid:

```json
{ "cc": "alice@example.com, bob@example.com" }
{ "cc": ["alice@example.com", "bob@example.com"] }
```

To send whatever mail you want, just publish the json in the queue of RabbitMQ you
have configured in you configuration file, e.g `conf/rabbit2ev.ini`.

The currently allowed keys to compose emails are (mandatory in bold):

**`to`** `cc` `bcc` `from` `subject` **`body`** `attachment`


## Contributing

Of course, please don't be shy.
