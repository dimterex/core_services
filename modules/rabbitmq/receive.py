import functools
import threading
import time

import pika


from modules.rabbitmq.messages.api_controller import Api_Controller

class ExampleConsumer(object):

    def __init__(self, amqp_url, queue, apiController: Api_Controller):
        self.apiController = apiController
        self.should_reconnect = False
        self.was_consuming = False
        self.queue = queue
        self._connection = None
        self._channel = None
        self._closing = False
        self._consumer_tag = None
        self._url = amqp_url
        self._consuming = False
        self._prefetch_count = 1

    def connect(self):
        print('Connecting to %s', self._url)
        return pika.SelectConnection(
            parameters=pika.URLParameters(self._url),
            on_open_callback=self.on_connection_open,
            on_open_error_callback=self.on_connection_open_error,
            on_close_callback=self.on_connection_closed)

    def close_connection(self):
        self._consuming = False
        if self._connection.is_closing or self._connection.is_closed:
            print('Connection is closing or already closed')
        else:
            print('Closing connection')
            self._connection.close()

    def on_connection_open(self, _unused_connection):
        print('Connection opened')
        self.open_channel()

    def on_connection_open_error(self, _unused_connection, err):
        print('Connection open failed: %s', err)
        self.reconnect()

    def on_connection_closed(self, _unused_connection, reason):
        self._channel = None
        if self._closing:
            self._connection.ioloop.stop()
        else:
            print('Connection closed, reconnect necessary: %s', reason)
            self.reconnect()

    def reconnect(self):
        self.should_reconnect = True
        self.stop()

    def open_channel(self):
        print('Creating a new channel')
        self._connection.channel(on_open_callback=self.on_channel_open)

    def on_channel_open(self, channel):
        print('Channel opened')
        self._channel = channel
        self.add_on_channel_close_callback()
        self.setup_queue(self.queue)

    def add_on_channel_close_callback(self):
        print('Adding channel close callback')
        self._channel.add_on_close_callback(self.on_channel_closed)

    def on_channel_closed(self, channel, reason):
        print('Channel %i was closed: %s', channel, reason)
        self.close_connection()

    def setup_queue(self, queue_name):
        print('Declaring queue %s', queue_name)
        self._channel.queue_declare(queue=queue_name)
        self.start_consuming()

    def start_consuming(self):
        print('Issuing consumer related RPC commands')
        self.add_on_cancel_callback()
        self._consumer_tag = self._channel.basic_consume(self.queue, self.on_message, auto_ack=True)
        self.was_consuming = True
        self._consuming = True

    def add_on_cancel_callback(self):
        print('Adding consumer cancellation callback')
        self._channel.add_on_cancel_callback(self.on_consumer_cancelled)

    def on_consumer_cancelled(self, method_frame):
        print('Consumer was cancelled remotely, shutting down: %r', method_frame)
        if self._channel:
            self._channel.close()

    def on_message(self, _unused_channel, basic_deliver, properties, body):
        print('Rabbit received message # %s from %s: %s', basic_deliver.delivery_tag, properties.app_id, body)
        self.apiController.received(body)

    def stop_consuming(self):
        if self._channel:
            print('Sending a Basic.Cancel RPC command to RabbitMQ')
            cb = functools.partial(
                self.on_cancelok, userdata=self._consumer_tag)
            self._channel.basic_cancel(self._consumer_tag, cb)

    def on_cancelok(self, _unused_frame, userdata):
        self._consuming = False
        print(
            'RabbitMQ acknowledged the cancellation of the consumer: %s',
            userdata)
        self.close_channel()

    def close_channel(self):
        print('Closing the channel')
        self._channel.close()

    def run(self):
        self._connection = self.connect()
        self._connection.ioloop.start()

    def stop(self):
        if not self._closing:
            self._closing = True
            print('Stopping')
            if self._consuming:
                self.stop_consuming()
                self._connection.ioloop.start()
            else:
                self._connection.ioloop.stop()
            print('Stopped')


class ReconnectingExampleConsumer(object):
    def __init__(self, amqp_url, queue, apiController: Api_Controller):
        self.apiController = apiController
        self._reconnect_delay = 0
        self._amqp_url = amqp_url
        self.queue = queue
        self._consumer = ExampleConsumer(self._amqp_url, self.queue, self.apiController)

    def run(self):
        while True:
            try:
                self._consumer.run()
            except KeyboardInterrupt:
                self._consumer.stop()
                break
            self._maybe_reconnect()

    def _maybe_reconnect(self):
        if self._consumer.should_reconnect:
            self._consumer.stop()
            reconnect_delay = self._get_reconnect_delay()
            print('Reconnecting after %d seconds', reconnect_delay)
            time.sleep(reconnect_delay)
            self._consumer = ExampleConsumer(self._amqp_url, self.queue, self.apiController)

    def _get_reconnect_delay(self):
        if self._consumer.was_consuming:
            self._reconnect_delay = 0
        else:
            self._reconnect_delay += 1
        if self._reconnect_delay > 30:
            self._reconnect_delay = 30
        return self._reconnect_delay
    

class Consumer:
    def __init__(self, host: str, port: int, queue: str, api_controller: Api_Controller):
        self.port = port
        self.host = host
        self.amqp_url = f'amqp://guest:guest@{self.host}:{self.port}'
        self.queue = queue
        self.api_controller = api_controller

    def start(self):
        def run():
            consumer = ReconnectingExampleConsumer(self.amqp_url, self.queue, self.api_controller)
            consumer.run()

        th = threading.Thread(target=run, name='receive', daemon=True)
        th.start()
