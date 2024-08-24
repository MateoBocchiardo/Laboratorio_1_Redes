import socket
import json

#Defino una clase Server 
class Server:
    
    #Constructor de la clase (Falta terminar)
    #def __init__(self, adress, port):
     #   self.address = address
      #  self.port = port
       # self.methods = {} #Definicion de un diccionario para guardar los procedimientos.
    
    
    
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
    