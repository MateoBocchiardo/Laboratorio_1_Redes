from server import Server

def resta(x, y):
    return x - y

def suma(*args):
    return sum(args)

def string_mas_largo(*strings):
    if not strings:
        return None
    return max(strings, key=len)



if __name__ == '__main__':

    server = Server('localhost', 5000)
    server.add_method(suma)
    server.add_method(resta)
    server.add_method(string_mas_largo)
    server.serve()
