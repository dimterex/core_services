import functools
import threading
import time

import pika

from modules.core.log_service.log_service import Logger_Service, INFO_LOG_LEVEL, DEBUG_LOG_LEVEL, ERROR_LOG_LEVEL, \
    WARNING_LOG_LEVEL
from modules.core.rabbitmq.api_controller import Api_Controller


class ExampleConsumer(object):

    def __init__(self, amqp_url, queue, apiController: Api_Controller, logger_service: Logger_Service):
        self.logger_service = logger_service
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
        self.logger_service.info(self.__class__.__name__, f'Connecting to {self._url}')
        return pika.SelectConnection(
            parameters=pika.URLParameters(self._url),
            on_open_callback=self.on_connection_open,
            on_open_error_callback=self.on_connection_open_error,
            on_close_callback=self.on_connection_closed)

    def close_connection(self):
        self._consuming = False
        if self._connection.is_closing or self._connection.is_closed:
            self.logger_service.info(self.__class__.__name__, 'Connection is closing or already closed')
        else:
            self.logger_service.info(self.__class__.__name__, 'Closing connection')
            self._connection.close()

    def on_connection_open(self, _unused_connection):
        self.logger_service.debug(self.__class__.__name__, 'Connection opened')
        self.open_channel()

    def on_connection_open_error(self, _unused_connection, err):
        self.logger_service.error(self.__class__.__name__, f'Connection open failed: {err}')
        self.reconnect()

    def on_connection_closed(self, _unused_connection, reason):
        self._channel = None
        if self._closing:
            self._connection.ioloop.stop()
        else:
            self.logger_service.debug(self.__class__.__name__, f'Connection closed, reconnect necessary: {reason}')
            self.reconnect()

    def reconnect(self):
        self.should_reconnect = True
        self.stop()

    def open_channel(self):
        self.logger_service.debug(self.__class__.__name__, 'Creating a new channel')
        self._connection.channel(on_open_callback=self.on_channel_open)

    def on_channel_open(self, channel):
        self.logger_service.debug(self.__class__.__name__, 'Channel opened')
        self._channel = channel
        self.add_on_channel_close_callback()
        self.setup_queue(self.queue)

    def add_on_channel_close_callback(self):
        self.logger_service.debug(self.__class__.__name__, 'Adding channel close callback')
        self._channel.add_on_close_callback(self.on_channel_closed)

    def on_channel_closed(self, channel, reason):
        self.logger_service.debug(self.__class__.__name__, f'Channel {channel} was closed: {reason}')
        self.close_connection()

    def setup_queue(self, queue_name):
        self.logger_service.debug(self.__class__.__name__, f'Declaring queue {queue_name}')
        self._channel.queue_declare(queue=queue_name)
        self.start_consuming()

    def start_consuming(self):
        self.logger_service.info(self.__class__.__name__, 'Issuing consumer related RPC commands')
        self.add_on_cancel_callback()
        on_message_callback = functools.partial(self.on_message, args=(self._connection))
        self._consumer_tag = self._channel.basic_consume(self.queue, on_message_callback)
        self.was_consuming = True
        self._consuming = True

    def add_on_cancel_callback(self):
        self.logger_service.debug(self.__class__.__name__, 'Adding consumer cancellation callback')
        self._channel.add_on_cancel_callback(self.on_consumer_cancelled)

    def on_consumer_cancelled(self, method_frame):
        self.logger_service.debug(self.__class__.__name__, f'Consumer was cancelled remotely, shutting down: {method_frame}')
        if self._channel:
            self._channel.close()

    def ack_message(self, ch, delivery_tag):
        """Note that `ch` must be the same pika channel instance via which
        the message being ACKed was retrieved (AMQP protocol constraint).
        """
        if ch.is_open:
            ch.basic_ack(delivery_tag)
            self.logger_service.debug(self.__class__.__name__, f'Send ask for {delivery_tag}')
        else:
            # Channel is already closed, so we can't ACK this message;
            # log and/or do something that makes sense for your app in this case.
            self.logger_service.debug(self.__class__.__name__, f'We cant ACK {delivery_tag} message')
            pass

    def do_work(self, conn, ch, delivery_tag, body):
        thread_id = threading.get_ident()
        raw_body = body.decode()
        self.logger_service.debug(self.__class__.__name__, f'Thread id: {thread_id} Delivery tag: {delivery_tag} Message body: {raw_body}')
        self.apiController.received(raw_body)
        self.ack_message(ch, delivery_tag)

    def on_message(self, ch, method_frame, _header_frame, body, args):
        (conn) = args
        delivery_tag = method_frame.delivery_tag
        t = threading.Thread(target=self.do_work, args=(conn, ch, delivery_tag, body))
        t.start()

    def stop_consuming(self):
        if self._channel:
            self.logger_service.debug(self.__class__.__name__, 'Sending a Basic.Cancel RPC command to RabbitMQ')
            cb = functools.partial(
                self.on_cancelok, userdata=self._consumer_tag)
            self._channel.basic_cancel(self._consumer_tag, cb)

    def on_cancelok(self, _unused_frame, userdata):
        self._consuming = False
        self.logger_service.debug(self.__class__.__name__, f'RabbitMQ acknowledged the cancellation of the consumer: {userdata}')
        self.close_channel()

    def close_channel(self):
        self.logger_service.debug(self.__class__.__name__, 'Closing the channel')
        self._channel.close()

    def run(self):
        self._connection = self.connect()
        self._connection.ioloop.start()

    def stop(self):
        if not self._closing:
            self._closing = True
            self.logger_service.info(self.__class__.__name__, 'Stopping')
            if self._consuming:
                self.stop_consuming()
                self._connection.ioloop.start()
            else:
                self._connection.ioloop.stop()
            self.logger_service.info(self.__class__.__name__, 'Stopped')


class ReconnectingExampleConsumer(object):
    def __init__(self, amqp_url, queue, apiController: Api_Controller, logger_service: Logger_Service):
        self.logger_service = logger_service
        self.apiController = apiController
        self._reconnect_delay = 0
        self._amqp_url = amqp_url
        self.queue = queue
        self._consumer = ExampleConsumer(self._amqp_url, self.queue, self.apiController, self.logger_service)

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
            self.logger_service.warning(self.__class__.__name__, f'Reconnecting after {reconnect_delay} seconds')
            time.sleep(reconnect_delay)
            self._consumer = ExampleConsumer(self._amqp_url, self.queue, self.apiController, self.logger_service)

    def _get_reconnect_delay(self):
        if self._consumer.was_consuming:
            self._reconnect_delay = 0
        else:
            self._reconnect_delay += 1
        if self._reconnect_delay > 30:
            self._reconnect_delay = 30
        return self._reconnect_delay
    

class Consumer:
    def __init__(self, amqp_url: str, queue: str, api_controller: Api_Controller, logger_service: Logger_Service):
        self.logger_service = logger_service
        self.amqp_url = amqp_url
        self.queue = queue
        self.api_controller = api_controller

    def start(self):
        def run():
            consumer = ReconnectingExampleConsumer(self.amqp_url, self.queue, self.api_controller, self.logger_service)
            consumer.run()

        th = threading.Thread(target=run, name='receive', daemon=True)
        th.start()
