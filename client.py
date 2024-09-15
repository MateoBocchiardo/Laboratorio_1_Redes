import socket
import json

# Defino una clase Client que se conecta a un servidor en la dirección y puerto especificados
class Client:

    # Constructor de la clase, recibe la dirección y puerto del servidor
    def __init__(self, address, port):
        self.address = address
        self.port = port
        # Atributo para otorgar un id único a cada petición
        self.request_id = 0

    # Metodo para reconectar al servidor
    def _setup_connection(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.connect((self.address, self.port))
        except socket.error as e:
            raise RuntimeError("Conexión fallida")

    # Método para interceptar los métodos que se llaman en el cliente
    def __getattr__(self, name):
        # Nota: notify es un argumento opcional que se usa para enviar una notificación al servidor
        def method(*args, notify=False, **kwargs):

            if args and kwargs:
                print('Error: No se pueden pasar argumentos posicionales y argumentos con nombre al mismo tiempo')
                self._close()
                return

            self.request_id += 1
            request = {
                "jsonrpc": "2.0",
                "method": name,
                "params": list(args) if not kwargs else {**kwargs},
                "id": None if notify else self.request_id
            }
            self._send_request(request)
            if not notify:
                return self._receive_response()
            else:
                self._close()
        return method

    # Método para enviar una petición al servidor
    def _send_request(self, request):
        try:
            print(f'Client Request:\n{request}')
            message = json.dumps(request).encode('utf-8')

            self._setup_connection()

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
        except Exception as e:
            self._close()
            # Intenta reconectarse si falla la conexion
            self._setup_connection()
            self._send_request(request)

    # Método para recibir la respuesta del servidor
    def _receive_response(self):
        # Utilizo un buffer de 4096 bytes, se puede ajustar según sea necesario
        buffer_size = 10
        response_chunks = []

        while True:
            # Recibe los datos del servidor en fragmentos
            chunk = self.sock.recv(buffer_size)
            response_chunks.append(chunk)
            data = b''.join(response_chunks).decode('utf-8')

            # Chequea si la respuesta esta completa
            if data.count('{') == data.count('}') and data.count('{') > 0:
                try:
                    json_data = json.loads(data)
                    break
                except json.JSONDecodeError:
                    raise RuntimeError("Error de análisis: JSON inválido recibido")
            else:
                continue

        response = json_data
        print(f'Server response:\n{response}')
        # Verifica si hay un error en la respuesta
        if 'error' in response:
            return {
            "Error": {
                "code": response['error'].get('code', 'Unknown code'),
                "message": response['error'].get('message', 'Unknown error')
                }
            }

        self._close()
        return response.get('result')

    # Método para cerrar la conexión con el servidor
    def _close(self):
        self.sock.close()

# Función para crear una instancia de la clase Client
def connect(address, port):
    return Client(address, port)

