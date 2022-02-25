import pika

from threading import Thread

from modules.rabbitmq.messages.api_controller import Api_Controller


class Consumer:
    def __init__(self, host: str, port: int, queue: str, api_controller: Api_Controller):
        self.queue = queue
        self.api_controller = api_controller
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host, port=port, heartbeat=0))

    def callback(self, channel, method, properties, body):
        self.api_controller.received(body)

    def start(self):
        def run():
            channel = self.connection.channel()
            channel.queue_declare(queue=self.queue)
            channel.basic_consume(queue=self.queue, on_message_callback=self.callback, auto_ack=True)
            channel.start_consuming()

        thread = Thread(target=run)
        thread.start()


