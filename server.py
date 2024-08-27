import socket
import json
import threading

#Defino una clase Server
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
        self.sock.listen() # No se especifica el número de conexiones en la cola

    def add_method(self, func):
        # Añade el método al diccionario de métodos
        self.methods[func.__name__] = func

    def serve(self):
        # Muestra la dirección y puerto en los que se está esperando conexiones
        print(f"Serving: {self.address}:{self.port}")
        while True:
            # Acepta una conexión entrante y crea un hilo para manejarla
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
                #conn.sendall(json.dumps(response).encode('utf-8')) NO SE PUEDE USAR sendall

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


    """
    # Funcion anterior
    def serve(self):
        #Socket IPv4 y TCP
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(self.host, self.port) #Asocio puerto y direccion al socket
            s.listen() #Se escuchan conexiones entrantes
            conn, addr = s.accept() #Bloquea ejecuiones y espera a una conexion
            with conn:
                print(f"Conexion establecida desde {addr}")
                while True:
                    data = conn.recv(1024) #si es vacio, se cierra la conexion
                    if not data:
                        break
                    conn.sendall(data)
    """
