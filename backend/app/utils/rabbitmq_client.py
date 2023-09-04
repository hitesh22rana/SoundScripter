import json
from typing import Callable

import pika

from app.config import settings


class RabbitMQClient:
    host: str = settings.rabbitmq_host
    port: int = settings.rabbitmq_port

    def __init__(self, queue_name: str) -> None:
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=RabbitMQClient.host, port=RabbitMQClient.port
            )
        )
        self.channel = self.connection.channel()
        self.queue_name = queue_name
        self.channel.queue_declare(queue=queue_name)

    def publish(self, data: dict) -> None:
        self.channel.basic_publish(
            exchange="", routing_key=self.queue_name, body=json.dumps(data)
        )
        self.channel.close()

    def consume(self, callback: Callable) -> None:
        self.channel.basic_consume(queue=self.queue_name, on_message_callback=callback)
        self.channel.start_consuming()
