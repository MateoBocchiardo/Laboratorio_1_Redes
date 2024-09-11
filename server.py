import socket
import json
import threading

#Defino una clase Server




class Server:


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

            if not isinstance(json_data, dict) or 'jsonrpc' not in json_data or json_data['jsonrpc'] != '2.0' or 'method' not in json_data or not isinstance(json_data['method'], str):
                # Si la solicitud no es un JSON-RPC válido, se envía un mensaje de error
                response = {
                    "jsonrpc": "2.0",
                    "error": {
                        "code": -32600,
                        "message": "Invalid Request"
                    },
                    "id": json_data.get('id', None)  # Usa el id de la solicitud si está presente
                }
                self._send_response(response, conn)

            # Busca el método solicitado en el diccionario de métodos
            method = self.methods.get(request['method'])

            # Chequea si es notificación
            is_notification = 'id' not in request or request['id'] is None

            if not is_notification:
                # Si no es notificación, se envía una respuesta
                if method:
                    try:
                        # Si el método es encontrado, se ejecuta. CASO DE ÉXITO
                        result = method(*request['params'])
                        response = {
                            "jsonrpc": "2.0",
                            "result": result,
                            "id": request['id']
                        }
                    except TypeError:
                        # Si los parámetros son inválidos, se envía un mensaje de error
                        response = {
                        "jsonrpc": "2.0",
                        "error": {
                            "code": -32602,
                            "message": "Invalid params"
                        },
                        "id": request['id']
                        }
                    except Exception as e:
                        # Si ocurre un error inesperado, se envía un mensaje de error
                        response = {
                            "jsonrpc": "2.0",
                            "error": {
                                "code": -32603,
                                "message": "Internal error"
                            },
                            "id": request['id']
                        }
                else:
                    # Si el método no es encontrado, se envía un mensaje de error
                    response = {
                        "jsonrpc": "2.0",
                        "error": {
                            "code": -32601,
                            "message": "Method not found"
                        },
                        "id": request['id']
                    }

                self._send_response(response, conn)


        conn.close()

    def _send_response(self, response, conn):

        total_sent = 0
        # Codifica la respuesta en un JSON y la envía
        message = json.dumps(response).encode('utf-8')
        while total_sent < len(message):
            sent = conn.send(message[total_sent:])
            if sent == 0:
                raise RuntimeError("Conexión cerrada")
            total_sent += sent



    def close(self):
        self.sock.close()

