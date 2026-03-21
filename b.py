import numpy as np

def algoritmo_banquero(procesos, recursos_existentes, asignados, necesidades):
    n_procesos = len(procesos)
    disponibles = np.array(recursos_existentes) - np.sum(asignados, axis=0)
    
    finalizado = [False] * n_procesos
    secuencia_segura = []
    trabajo = np.array(disponibles)

    print(f"Recursos Disponibles Iniciales: {trabajo}\n")

    while len(secuencia_segura) < n_procesos:
        for i in range(n_procesos):
            if not finalizado[i] and all(necesidades[i] <= trabajo):
                print(f"-> Proceso {procesos[i]} ejecuta. Libera recursos: {trabajo + asignados[i]}\n")
                trabajo += asignados[i]
                finalizado[i] = True
                secuencia_segura.append(procesos[i])
                break
        else:
            break

    if len(secuencia_segura) == n_procesos:
        print(f"ESTADO SEGURO: {' -> '.join(secuencia_segura)}")
    else:
        print("ESTADO INSEGURO: Interbloqueo posible.")

# Test
procesos = ["A", "B", "C", "D", "E"]
E = [6, 3, 4, 2]
asignado = np.array([[3, 0, 1, 1], [0, 1, 0, 0], [1, 1, 1, 0], [1, 1, 0, 1], [0, 0, 0, 0]])
necesidad = np.array([[1, 1, 0, 0], [0, 1, 1, 2], [3, 1, 0, 0], [0, 0, 1, 0], [2, 1, 1, 0]])

algoritmo_banquero(procesos, E, asignado, necesidad)
