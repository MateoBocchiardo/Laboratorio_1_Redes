from client import connect


if __name__ == '__main__':

    # Terminales locales
    #client_1 = connect('localhost', 5000)
    #client_2 = connect('localhost', 5001)

    client_1 = connect('200.0.0.10', 5000)
    client_2 = connect('200.100.0.15', 5001)

    print('Funcion que devuelve 1')
    print(f'Result: {client_1.devolver_uno()}\n')

    print('Funcion resta entre 10 y 5')
    print(f'Result: {client_1.resta(10, 5)}\n')

    print('Funcion suma con 1, 2, 3, 4 y 5')
    print(f'Result: {client_1.suma(1, 2, 3, 4, 5)}\n')

    print('Funcion string mas largo con hola, adios, bye y hello')
    print(f'Result: {client_1.string_mas_largo("hola", "adios", "bye", "hello")}\n')

    print('Funcion concatenar con hola, adios, bye y hello')
    print(f'Result: {client_2.concatenar(" ", "hola", "adios", "bye", "hello")}\n')

    print('Funcion logaritmo con 25 y base 5')
    print(f'Result: {client_2.logaritmo(numero=25, base=5)}\n')

    print('Funcion maximo comun divisor con 10 y 5')
    print(f'Result: {client_2.maximo_comun_divisor(10, 5)}\n')

    print('Funcion reordenar con 1, 2, 3 y 4')
    print(f'Result: {client_2.reordenar(1, 2, 3, 4)}\n')

    print('Notificacion a funcion suma')
    print(f'Result: {client_1.suma(notify=True)}\n')

    print('Notificacion a funcion concatenar con parametros')
    print(f'Result: {client_2.concatenar(" ", "hola", "adios", "bye", "hello", notify=True)}\n')

    print('Error: Metodo inexistente')
    print(f'{client_1.un_metodo_inexistente()}\n')

    print('Error: Parametro invalido')
    print(f'{client_1.suma(1, 2, 3, "4")}\n')

    print('Error: Mas parametros de los esperados')
    print(f'{client_1.devolver_uno(1)}\n')

    print('Error: Menos parametros de los esperados')
    print(f'{client_1.resta(1)}\n')

    print('Error: Keyword argument y positional arguments a la vez')
    print(f'{client_1.resta(1, y=2)}\n')

