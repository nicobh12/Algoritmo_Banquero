def mostrar_estado(titulo, trabajo, asignados, necesidades, procesos, indice_proceso=None):
    print(titulo)
    if indice_proceso is not None and "DURANTE" in titulo:
        recursos_mostrados = restar_vectores(trabajo, necesidades[indice_proceso])
    else:
        recursos_mostrados = trabajo

    print(f"Recursos disponibles: {recursos_mostrados}")

    if indice_proceso is not None:
        print(f"Proceso en ejecucion: {procesos[indice_proceso]}")

    print("Matriz de asignados:")
    print(asignados)
    print("Matriz de necesidades:")
    print(necesidades)
    print()


def sumar_vectores(v1, v2):
    return [a + b for a, b in zip(v1, v2)]


def restar_vectores(v1, v2):
    return [a - b for a, b in zip(v1, v2)]


def necesidades_caben(necesidad, trabajo):
    return all(necesidad[j] <= trabajo[j] for j in range(len(trabajo)))


def construir_matriz_asignados_durante(asignados, necesidades, indice_proceso):
    matriz_durante = [fila[:] for fila in asignados]
    matriz_durante[indice_proceso] = sumar_vectores(
        asignados[indice_proceso], necesidades[indice_proceso]
    )
    return matriz_durante

def algoritmo_banquero(procesos, recursos_existentes, asignados, necesidades):

    n_procesos = len(procesos)
    disponibles = [recursos_existentes[j] - sum(fila[j] for fila in asignados) for j in range(len(recursos_existentes))]
    
    finalizado = [False] * n_procesos
    secuencia_segura = []
    trabajo = disponibles[:]

    mostrar_estado("ESTADO INICIAL", trabajo, asignados, necesidades, procesos)

    iteracion = 1

    while len(secuencia_segura) < n_procesos:
        indice_ejecutable = None
        for i in range(n_procesos):
            if not finalizado[i] and necesidades_caben(necesidades[i], trabajo):
                indice_ejecutable = i
                break

        if indice_ejecutable is None:
            mostrar_estado(f"ITERACION {iteracion} - DURANTE", trabajo, asignados, necesidades, procesos)
            mostrar_estado(f"ITERACION {iteracion} - DESPUES", trabajo, asignados, necesidades, procesos)
            break

        asignados_durante = construir_matriz_asignados_durante(
            asignados, necesidades, indice_ejecutable
        )

        mostrar_estado(
            f"ITERACION {iteracion} - DURANTE",
            trabajo,
            asignados_durante,
            necesidades,
            procesos,
            indice_ejecutable,
        )

        recursos_liberados = asignados[indice_ejecutable][:]
        print(
            f"-> Proceso {procesos[indice_ejecutable]} ejecuta. Libera recursos: "
            f"{sumar_vectores(trabajo, recursos_liberados)}\n"
        )
        trabajo = sumar_vectores(trabajo, recursos_liberados)
        asignados[indice_ejecutable] = [0] * len(asignados[indice_ejecutable])
        necesidades[indice_ejecutable] = [0] * len(necesidades[indice_ejecutable])
        finalizado[indice_ejecutable] = True
        secuencia_segura.append(procesos[indice_ejecutable])

        mostrar_estado(
            f"ITERACION {iteracion} - DESPUES",
            trabajo,
            asignados,
            necesidades,
            procesos,
            indice_ejecutable,
        )
        iteracion += 1

    if len(secuencia_segura) == n_procesos:
        print(f"ESTADO SEGURO: {' -> '.join(secuencia_segura)}")
    else:
        print("ESTADO INSEGURO: Interbloqueo posible.")

# Test
procesos = ["A", "B", "C", "D", "E"]
E = [6, 3, 4, 2]
asignado = [[3, 0, 1, 1], [0, 1, 0, 0], [1, 1, 1, 0], [1, 1, 0, 1], [0, 0, 0, 0]]
necesidad = [[1, 1, 0, 0], [0, 1, 1, 2], [3, 1, 0, 0], [0, 0, 1, 0], [2, 1, 1, 0]]

algoritmo_banquero(procesos, E, asignado, necesidad)
