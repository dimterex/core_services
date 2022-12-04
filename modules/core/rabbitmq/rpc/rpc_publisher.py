import json

import pika
import uuid


class RpcPublisher(object):
    def __init__(self, url: str):
        self.url = url
        self.responses: {str, str} = {}

    def call(self, routing_key: str, message: str) -> str:
        connection = pika.BlockingConnection(parameters=pika.URLParameters(self.url))
        channel = connection.channel()
        result = channel.queue_declare(queue='', exclusive=True)
        callback_queue = result.method.queue
        corr_id = str(uuid.uuid4())

        def on_response(ch, method, props, body):
            if corr_id == props.correlation_id:
                self.responses[corr_id] = body

        channel.basic_consume(
            queue=callback_queue,
            on_message_callback=on_response,
            auto_ack=True)

        channel.basic_publish(
            exchange='',
            routing_key=routing_key,
            properties=pika.BasicProperties(
                reply_to=callback_queue,
                correlation_id=corr_id,
            ),
            body=message)
        connection.process_data_events(time_limit=None)
        connection.close()
        response = self.responses[corr_id]
        self.responses.pop(corr_id)
        return json.loads(response)


