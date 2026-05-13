from prometheus_client import Counter

orders_created_counter = Counter(
    "api_orders_created_total",
    "Total number of orders created through the FastAPI application",
)
