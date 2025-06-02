from prometheus_client import Counter

events_stored_counter = Counter("events_stored_counter", "Count of stored events")
