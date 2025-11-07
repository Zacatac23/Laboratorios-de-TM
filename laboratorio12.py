# ============================================================
# Universidad del Valle de Guatemala
# Facultad de Ingeniería
# Ingeniería en Ciencia de la Computación y TI
# Autor: Jonathan Josué Zacarias Bances
# Carné: 231104
# Laboratorio No. 12 - Programación Funcional en Python
# ============================================================

# Este laboratorio demuestra el uso de funciones lambda
# en Python para realizar operaciones comunes:
# 1. Ordenar una lista de diccionarios.
# 2. Calcular la potencia n-ésima de cada elemento en una lista.
# 3. Calcular la matriz transpuesta.
# 4. Eliminar elementos de una lista según otra lista dada.

# ------------------------------------------------------------
# Ejercicio 1: Ordenar una lista de diccionarios
# ------------------------------------------------------------
def ejercicio1():
    print("\n=== Ejercicio 1: Ordenar lista de diccionarios ===")
    autos = [
        {'marca': 'Toyota', 'modelo': 'Corolla', 'año': 2020},
        {'marca': 'Honda', 'modelo': 'Civic', 'año': 2019},
        {'marca': 'Mazda', 'modelo': 'CX5', 'año': 2021}
    ]

    # Ordenar por la key 'modelo'
    autos_ordenados = sorted(autos, key=lambda x: x['modelo'])

    print("Lista ordenada por 'modelo':")
    for a in autos_ordenados:
        print(a)


# ------------------------------------------------------------
# Ejercicio 2: Potencia n-ésima de cada elemento de una lista
# ------------------------------------------------------------
def ejercicio2():
    print("\n=== Ejercicio 2: Potencia n-ésima de una lista ===")
    lista = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    n = int(input("Ingrese la potencia n (entero positivo): "))

    resultado = list(map(lambda x: x ** n, lista))
    print(f"Lista elevada a la potencia {n}: {resultado}")


# ------------------------------------------------------------
# Ejercicio 3: Matriz transpuesta usando lambda
# ------------------------------------------------------------
def ejercicio3():
    print("\n=== Ejercicio 3: Matriz transpuesta ===")
    X = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]

    print("Matriz original:")
    for fila in X:
        print(fila)

    # Transpuesta usando zip y lambda
    XT = list(map(lambda *fila: list(fila), *X))

    print("\nMatriz transpuesta:")
    for fila in XT:
        print(fila)


# ------------------------------------------------------------
# Ejercicio 4: Eliminar elementos de una lista
# ------------------------------------------------------------
def ejercicio4():
    print("\n=== Ejercicio 4: Eliminar elementos de una lista ===")
    colores = ['rojo', 'verde', 'azul', 'amarillo', 'gris', 'blanco', 'negro']
    eliminar = ['amarillo', 'café', 'blanco']

    print("Lista original:", colores)
    print("Elementos a eliminar:", eliminar)

    # Filtrar usando lambda y filter()
    resultado = list(filter(lambda c: c not in eliminar, colores))

    print("Lista después de eliminar:", resultado)


# ------------------------------------------------------------
# Programa principal
# ------------------------------------------------------------
def main():
    print("===========================================")
    print("Laboratorio No. 12 - Programación Funcional")
    print("Autor: Jonathan Josué Zacarias Bances")
    print("Carné: 231104")
    print("===========================================")

    while True:
        print("\nSeleccione el ejercicio a ejecutar:")
        print("1. Ordenar lista de diccionarios")
        print("2. Potencia n-ésima de una lista")
        print("3. Matriz transpuesta")
        print("4. Eliminar elementos de una lista")
        print("5. Salir")

        opcion = input("Opción: ")

        if opcion == '1':
            ejercicio1()
        elif opcion == '2':
            ejercicio2()
        elif opcion == '3':
            ejercicio3()
        elif opcion == '4':
            ejercicio4()
        elif opcion == '5':
            print("\nSaliendo del programa...")
            break
        else:
            print("Opción inválida. Intente nuevamente.")


if __name__ == "__main__":
    main()
