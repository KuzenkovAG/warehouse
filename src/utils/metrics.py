from prometheus_client import Counter

movements_stored_counter = Counter("events_stored_counter", "Count of stored events")
