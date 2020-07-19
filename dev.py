from wsgiref import simple_server
from mal import create_app

api = create_app()

if __name__ == "__main__":
    ip = "127.0.0.1"
    port = 5000
    print(f"Running on {ip}:{port}")
    server = simple_server.make_server(ip, port, api)
    server.serve_forever()
