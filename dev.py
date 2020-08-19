from wsgiref import simple_server
from mal import create_app


def main() -> None:
    """Here where it all began"""
    api = create_app()
    addr, port = "127.0.0.1", 5000
    print(f"Running on {addr}:{port}")
    server = simple_server.make_server(addr, port, api)
    server.serve_forever()


if __name__ == "__main__":
    main()
