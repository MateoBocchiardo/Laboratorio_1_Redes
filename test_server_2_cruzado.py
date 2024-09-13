from jsonrpc_redes.server import Server
import math

def logaritmo(numero, base=10):
    return math.log(numero, base)


def concatenar(separador, *args):
    return separador.join(args)


def maximo_comun_divisor(a, b):
    while b:
        a, b = b, a % b
    return a

def reordenar(a, b, c, d):
    return d, c, b ,a



if __name__ == '__main__':

    # Terminales locales
    #server = Server('localhost', 5001)

    server = Server(('200.100.0.15', 5001))
    server.add_method(concatenar)
    server.add_method(logaritmo)
    server.add_method(maximo_comun_divisor)
    server.add_method(reordenar)
    server.serve()