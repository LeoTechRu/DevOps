from celery import Celery

celery_app = Celery(
    "homework_12",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/1",
)


@celery_app.task
def log_new_product(product_name: str) -> None:
    """Log information about a newly added product."""
    print(f"Новый товар добавлен: {product_name}")
