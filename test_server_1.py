from server import Server

def devolver_uno():
    return 1

def resta(x, y):
    return x - y

def suma(*args):
    return sum(args)

def string_mas_largo(*strings):
    if not strings:
        return None
    return max(strings, key=len)



if __name__ == '__main__':

    # Terminales locales
    #server = Server(('localhost', 5000))

    server = Server(('200.0.0.10', 5000))
    server.add_method(suma)
    server.add_method(resta)
    server.add_method(string_mas_largo)
    server.add_method(devolver_uno)
    server.serve()
