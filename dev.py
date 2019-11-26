from wsgiref import simple_server
from mal import create_app

api = create_app()

if __name__ == "__main__":
    server = simple_server.make_server("127.0.0.1", 5000, api)
    server.serve_forever()
