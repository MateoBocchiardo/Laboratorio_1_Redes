from client import connect


if __name__ == '__main__':

    client_1 = connect('localhost', 5000)
    client_2 = connect('localhost', 5001)

    print(client_1.suma(9, 5))  # Debería imprimir 14

    print(client_2.concatenar(',','Hola',' buen día')) #Debería imprimir Hola, buen día

    print(client_1.resta(11, 3))  # Debería imprimir 8

    print(client_2.multiplicacion(2,8)) # Debería imprimir 16

    print(client_1.string_mas_largo('Hola', 'Uruguay', 'No')) # Debería imprimir Uruguay

    print(client_2.maximo_comun_divisor(12, 18)) # Debería imprimir 6

    print(client_2.reordenar('a', 'b', 'c', 'd')) # Debería imprimir d, c, b, a


    client_1.close()
    client_2.close()
