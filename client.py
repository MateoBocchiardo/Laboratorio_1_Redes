import socket
import json

# Defino una clase Client que se conecta a un servidor en la dirección y puerto especificados
class Client:

    # Constructor de la clase, recibe la dirección y puerto del servidor
    def __init__(self, address, port):
        self.address = address
        self.port = port
        # Utiliza IPv4 y TCP (¿podría usarse IPv6?)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.address, self.port))
        # Atributo para otorgar un id único a cada petición
        self.request_id = 0

    # Método para interceptar los métodos que se llaman en el cliente
    def __getattr__(self, name):
        # Nota: notify es un argumento opcional que se usa para enviar una notificación al servidor
        def method(*args, notify=False):
            self.request_id += 1
            request = {
                "jsonrpc": "2.0",
                "method": name,
                "params": args,
                "id": None if notify else self.request_id
            }
            self._send_request(request)
            if not notify:
                return self._receive_response()
        return method

    # Método para enviar una petición al servidor
    def _send_request(self, request):
        message = json.dumps(request)
        self.sock.sendall(message.encode('utf-8'))

    # Método para recibir la respuesta del servidor
    def _receive_response(self):
        # Recibe la respuesta del servidor (4096 bytes, se puede cambiar) y la convierte a un diccionario
        response = self.sock.recv(4096)
        return json.loads(response.decode('utf-8'))['result']

    # Método para cerrar la conexión con el servidor
    def close(self):
        self.sock.close()

# Función para crear una instancia de la clase Client
def connect(address, port):
    return Client(address, port)

