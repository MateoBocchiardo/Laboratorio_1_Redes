from server import Server

def multiplicacion(*args):
    res = 1
    for arg in args:
        res *= arg
    return res


def concatenar(separador, *args):
    return separador.join(args)


def maximo_comun_divisor(a, b):
    while b:
        a, b = b, a % b
    return a



if __name__ == '__main__':

    server = Server('localhost', 5001)
    server.add_method(concatenar)
    server.add_method(multiplicacion)
    server.add_method(maximo_comun_divisor)
    server.serve()