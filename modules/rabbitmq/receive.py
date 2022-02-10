import pika

from threading import Thread

from modules.rabbitmq.messages.api_controller import Api_Controller


class Consumer:
    def __init__(self, host: str, port: int, queue: str, api_controller: Api_Controller):
        self.api_controller = api_controller
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host, port=port))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=queue)
        self.channel.basic_consume(queue=queue, on_message_callback=self.callback, auto_ack=True)

    def callback(self, channel, method, properties, body):
        self.api_controller.received(body)

    def start(self):
        def run():
            self.channel.start_consuming()

        thread = Thread(target=run)
        thread.start()


