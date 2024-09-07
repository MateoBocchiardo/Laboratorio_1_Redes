import socket
import json
import threading

#Defino una clase Server

# TO DO: Implementar respeustas de array a funciones


class Server:

    #Constructor de la clase (Falta terminar)
    #def __init__(self, adress, port):
     #   self.address = address
      #  self.port = port
       # self.methods = {} #Definicion de un diccionario para guardar los procedimientos.

    def __init__(self, address, port):
        self.address = address
        self.port = port
        # Diccionario para guardar los métodos
        self.methods = {}
        # Crea un socket IPv4 y TCP
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.address, self.port))

    def add_method(self, func):
        # Añade el método al diccionario de métodos
        self.methods[func.__name__] = func

    def serve(self):
        # Se dispone a escuchar conexiones entrantes
        self.sock.listen() # No se especifica el número de conexiones en la cola
        # Muestra la dirección y puerto en los que se está esperando conexiones
        print(f"Serving: {self.address}:{self.port}")
        while True:
            # Acepta una conexión entrante y crea un hilo para manejarla
            conn, _ = self.sock.accept()
            threading.Thread(target=self._handle_client, args=(conn,)).start()

    def _handle_client(self, conn):

        buffer_size = 10

        while True:
            response_chunks = []

            while True:
                # Recibe los datos del servidor en fragmentos
                chunk = conn.recv(buffer_size)
                response_chunks.append(chunk)

                # Chequea si la respuesta es un JSON válido
                try:
                    data = b''.join(response_chunks).decode('utf-8')
                    json_data = json.loads(data)
                    break
                except json.JSONDecodeError:
                    # Si no es completo cointinuar recibiendo datos
                    continue

            if not json_data:
                break

            request = json_data
            method = self.methods.get(request['method'])
            if method:
                result = method(*request['params'])
                response = {
                    "jsonrpc": "2.0",
                    "result": result,
                    "id": request['id']
                }

                total_sent = 0
                message = json.dumps(response).encode('utf-8')
                while total_sent < len(message):
                    sent = conn.send(message[total_sent:])

                    if sent == 0:
                        raise RuntimeError("Conexión cerrada")

                    total_sent += sent


        conn.close()

    def close(self):
        self.sock.close()

