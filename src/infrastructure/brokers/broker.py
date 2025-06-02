from infrastructure.brokers.kafka.kafka import Kafka


class Broker:
    kafka: Kafka

    def __init__(self, kafka: Kafka):
        self.kafka = kafka

    async def health(self) -> bool:
        return True  # TODO:
