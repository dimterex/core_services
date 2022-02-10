import pika

class Publisher:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    def send_message(self, queue: str, message: str):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host, port=self.port))
        channel = connection.channel()
        channel.queue_declare(queue=queue)
        channel.basic_publish(exchange='', routing_key=queue, body=message)
        connection.close()

    def close(self):
        pass

