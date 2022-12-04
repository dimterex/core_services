import pika

class Publisher:
    def __init__(self, url: str):
        self._url = url

    def send_message(self, queue: str, message: str):
        connection = pika.BlockingConnection(parameters=pika.URLParameters(self._url))
        channel = connection.channel()
        channel.queue_declare(queue=queue)
        channel.basic_publish(exchange='', routing_key=queue, body=message)
        connection.close()

