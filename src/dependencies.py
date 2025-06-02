from dependency_injector.containers import DeclarativeContainer


class BaseContainer(DeclarativeContainer): ...


class ViewContainer(BaseContainer): ...


class DaemonContainer(BaseContainer): ...
