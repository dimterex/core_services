import threading

import pika

from modules.core.rabbitmq.rpc.rcp_api_controller import RpcApiController


class RpcConsumer:
    def __init__(self, url: str, queue: str, api_controller: RpcApiController):
        self._url = url
        self.TAG = self.__class__.__name__
        connection = pika.BlockingConnection(parameters=pika.URLParameters(self._url))
        self.channel = connection.channel()
        self.channel.queue_declare(queue=queue)

        def on_request(ch, method, props, body):
            response = api_controller.received(body)

            ch.basic_publish(exchange='',
                             routing_key=props.reply_to,
                             properties=pika.BasicProperties(correlation_id=props.correlation_id),
                             body=str(response))
            ch.basic_ack(delivery_tag=method.delivery_tag)

        self.channel.basic_consume(queue=queue, on_message_callback=on_request)

    def start(self):
        def run():
            self.channel.start_consuming()

        th = threading.Thread(target=run, name=self.TAG, daemon=True)
        th.start()






