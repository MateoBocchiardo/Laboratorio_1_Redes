import socket
import json
import threading

class Server:
    def __init__(self, address, port):
        self.address = address
        self.port = port
        self.methods = {}
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.address, self.port))
        self.sock.listen() # No se especifica el número de conexiones en la cola

    def add_method(self, func):
        self.methods[func.__name__] = func

    def serve(self):
        print(f"Serving on {self.address}:{self.port}")
        while True:
            conn, _ = self.sock.accept()
            threading.Thread(target=self._handle_client, args=(conn,)).start()

    def _handle_client(self, conn):
        while True:
            data = conn.recv(4096)
            if not data:
                break
            request = json.loads(data.decode('utf-8'))
            method = self.methods.get(request['method'])
            if method:
                result = method(*request['params'])
                response = {
                    "jsonrpc": "2.0",
                    "result": result,
                    "id": request['id']
                }
                conn.sendall(json.dumps(response).encode('utf-8'))
        conn.close()

    def close(self):
        self.sock.close()
