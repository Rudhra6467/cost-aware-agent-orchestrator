from caos.api_app import create_server
from caos.http_api import PlanningAPI
from caos.product_service import ProductService


def main() -> None:
    product = ProductService()
    api = PlanningAPI(product)
    server = create_server(api)
    print("CAOS server listening on http://127.0.0.1:8080")
    print("Paste an idea, then use SHOW ME HOW or BUILD.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
