class WarehouseBaseError(Exception):
    message: str = "Happened error"

    def __init__(self, message: str | None = None):
        if not message:
            return

        self.message = message.message if isinstance(message, WarehouseBaseError) else message

    def __str__(self):
        return self.message
