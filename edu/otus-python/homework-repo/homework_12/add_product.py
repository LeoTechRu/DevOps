from .tasks import log_new_product


def add_product(name: str) -> None:
    """Send a task to log information about a new product."""
    log_new_product.delay(name)


if __name__ == "__main__":
    import sys

    product_name = sys.argv[1] if len(sys.argv) > 1 else "Example Product"
    add_product(product_name)
