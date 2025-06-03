from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from infrastructure.brokers.broker import Broker
from infrastructure.brokers.kafka.kafka import Kafka
from infrastructure.brokers.kafka.kafka_consumer import KafkaConsumer
from infrastructure.infrastructure import Infrastructure
from infrastructure.repositories.database import Database
from infrastructure.repositories.movements_repository import MovementsRepository
from infrastructure.repositories.repository import Repository
from infrastructure.repositories.warehouses_repository import WarehousesRepository
from services.movements_service import MovementsService
from services.service import Service
from services.warehouses_service import WarehousesService
from settings import settings


class BaseContainer(DeclarativeContainer):
    # repository
    engine = providers.Resource(settings.get_repository)
    database = providers.Singleton(Database, engine=engine)

    movements_repository = providers.Singleton(MovementsRepository, database=database)
    warehouses_repository = providers.Singleton(WarehousesRepository, database=database)
    repository = providers.Singleton(
        Repository,
        database=database,
        movements_repository=movements_repository,
        warehouses_repository=warehouses_repository,
    )

    # services
    movements_service = providers.Singleton(MovementsService, repository=movements_repository)
    warehouses_service = providers.Singleton(WarehousesService, repository=warehouses_repository)


class ViewContainer(BaseContainer):
    # infra
    infra = providers.Singleton(Infrastructure, repository=BaseContainer.repository)

    # service
    service = providers.Singleton(
        Service,
        infrastructure=infra,
        movements_service=BaseContainer.movements_service,
        warehouse_service=BaseContainer.warehouses_service,
    )


class DaemonContainer(BaseContainer):
    # kafka
    kafka_consumer_client = providers.Resource(settings.get_kafka_consumer)
    kafka_consumer = providers.Singleton(KafkaConsumer, kafka_consumer_client)
    kafka = providers.Singleton(Kafka, kafka_consumer)

    # broker
    broker = providers.Singleton(Broker, kafka)

    # infra
    infra = providers.Singleton(
        Infrastructure,
        repository=BaseContainer.repository,
        broker=broker,
    )

    # service
    service = providers.Singleton(
        Service,
        infrastructure=infra,
        movements_service=BaseContainer.movements_service,
        warehouse_service=BaseContainer.warehouses_service,
    )

    # Daemons
    _daemon_starting_saving_events = providers.MethodCaller(service.provided.starting_saving_events)

    daemons = providers.Resource(
        providers.List(
            _daemon_starting_saving_events,
        )
    )
