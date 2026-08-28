from caos.api_app import create_server
from caos.http_api import PlanningAPI
from caos.planning_service import PlanningService


def main() -> None:
    service = PlanningService()
    api = PlanningAPI(service)
    server = create_server(api)
    print("CAOS server listening on http://127.0.0.1:8080")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
