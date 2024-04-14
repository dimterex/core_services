import json

import pika
import uuid

from core.rabbitmq.messages.base_request import BaseMessage
from core.rabbitmq.messages.status_response import ERROR_STATUS_CODE, StatusResponse


class RpcPublisher(object):
    def __init__(self, url: str):
        self.url = url
        self.responses: {str, object} = {}

    def call(self, routing_key: str, request: BaseMessage) -> StatusResponse:
        connection = pika.BlockingConnection(parameters=pika.URLParameters(self.url))
        channel = connection.channel()
        result = channel.queue_declare(queue='', exclusive=True)
        callback_queue = result.method.queue
        corr_id = str(uuid.uuid4())

        def on_response(ch, method, props, body):
            if corr_id == props.correlation_id:
                self.responses[corr_id] = body.decode('utf-8')

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
            body=json.dumps(request.serialize()))
        connection.process_data_events(time_limit=20)
        connection.close()

        if corr_id in self.responses:
            response = self.responses[corr_id]
            self.responses.pop(corr_id)
            js = json.loads(response)
            if isinstance(js, str):
                return StatusResponse.deserialize(json.loads(js))
            return StatusResponse.deserialize(js)

        return StatusResponse('Not exist response', ERROR_STATUS_CODE)
