import socket
import json

# Defino una clase Client que se conecta a un servidor en la dirección y puerto especificados
class Client:

    # Constructor de la clase, recibe la dirección y puerto del servidor
    def __init__(self, address, port):
        self.address = address
        self.port = port
        # Utiliza IPv4 y TCP
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
        message = json.dumps(request).encode('utf-8')

        # Inicializar un contador para llevar la cuenta de los bytes enviados
        total_sent = 0

        # Continuar enviando hasta que se hayan enviado todos los bytes del mensaje
        while total_sent < len(message):
            # Enviar los bytes restantes del mensaje, comenzando desde donde se quedó en la iteración anterior
            sent = self.sock.send(message[total_sent:])

            # Si no se envía ningún byte, significa que la conexión se ha cerrado inesperadamente
            if sent == 0:
                raise RuntimeError("Conexión cerrada")

            # Actualizar el total de bytes enviados
            total_sent += sent


    # Método para recibir la respuesta del servidor
    def _receive_response(self):
        # Utilizo un buffer de 4096 bytes, se puede ajustar según sea necesario
        buffer_size = 10
        response_chunks = []

        while True:
            # Recibe los datos del servidor en fragmentos
            chunk = self.sock.recv(buffer_size)
            if not chunk:
                # Si no hay más datos, salir del bucle
                break
            response_chunks.append(chunk)

            # Chequea si la respuesta es un JSON válido
            try:
                response_data = json.loads(b''.join(response_chunks).decode('utf-8'))
                break
            except json.JSONDecodeError:
                # Si no es completo cointinuar recibiendo datos
                continue

        response = response_data
        # Verifica si hay un error en la respuesta
        if 'error' in response:
            return {
            "error": {
                "code": response_data['error'].get('code', 'Unknown code'),
                "message": response_data['error'].get('message', 'Unknown error'),
                "data": response_data['error'].get('data', None)
                }
            }

        return response.get('result')

    # Método para cerrar la conexión con el servidor
    def close(self):
        self.sock.close()

# Función para crear una instancia de la clase Client
def connect(address, port):
    return Client(address, port)

