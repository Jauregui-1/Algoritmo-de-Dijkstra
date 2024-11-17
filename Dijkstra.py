# RODRIGUEZ JAUREGUI JARED

# Importación de librerías necesarias
import heapq  # Librería para trabajar con colas de prioridad (útil en Dijkstra)
import networkx as nx  # Librería para crear y trabajar con grafos
import matplotlib.pyplot as plt  # Librería para graficar el grafo

# Función que implementa el algoritmo de Dijkstra para encontrar las rutas más cortas
def dijkstra(grafo, inicio):
    # Inicializa un diccionario con distancias infinitas para todos los nodos
    distancias = {nodo: float('inf') for nodo in grafo}
    distancias[inicio] = 0  # La distancia al nodo inicial es 0
    
    # Cola de prioridad que almacena los nodos a explorar, ordenada por la distancia mínima
    cola_prioridad = [(0, inicio)]  # Inicia con el nodo de inicio y su distancia 0
    camino_corto = {}  # Diccionario para almacenar el nodo anterior en el camino más corto
    
    # Mientras haya nodos en la cola de prioridad
    while cola_prioridad:
        # Extrae el nodo con la menor distancia acumulada
        distancia_actual, nodo_actual = heapq.heappop(cola_prioridad)
        
        # Si la distancia extraída es mayor a la registrada, continúa con el siguiente nodo
        if distancia_actual > distancias[nodo_actual]:
            continue
        
        # Imprime el nodo que está siendo explorado y su distancia acumulada
        print(f"Explorando nodo {nodo_actual} con distancia acumulada {distancia_actual}")
        
        # Recorre los vecinos del nodo actual y actualiza las distancias si se encuentra una mejor ruta
        for vecino, peso in grafo[nodo_actual].items():
            distancia = distancia_actual + peso  # Distancia total al vecino
            # Si la nueva distancia es menor, actualiza la distancia y la ruta más corta
            if distancia < distancias[vecino]:
                distancias[vecino] = distancia
                camino_corto[vecino] = nodo_actual  # Guarda el nodo anterior en la ruta más corta
                heapq.heappush(cola_prioridad, (distancia, vecino))  # Agrega el vecino a la cola de prioridad
                # Imprime la nueva distancia para el vecino
                print(f"  - Vecino {vecino} actualizado con nueva distancia {distancia}")
    
    return distancias, camino_corto  # Devuelve las distancias mínimas y la ruta más corta

# Grafo con nodos y aristas (los costos de las aristas están representados por los valores)
grafo = {
    'A': {'B': 4, 'C': 8,'D':2,'E':6},  # Nodo A 
    'B': {'C': 2, 'D': 6, 'E': 3},  # Nodo B 
    'C': {'F': 9, 'D': 3},  # Nodo C 
    'D': {'E': 1, 'G': 4, 'H': 7},  # Nodo D 
    'E': {'F': 5, 'H': 3},  # Nodo E 
    'F': {'I': 2},  # Nodo F 
    'G': {'H': 1, 'J': 5},  # Nodo G 
    'H': {'I': 4, 'J': 6},  # Nodo H 
    'I': {'J': 3},  # Nodo I 
    'J': {'A':2}  # Nodo J 
}

# Ciudad de inicio
ciudad_inicio = 'C'

# Ejecuta el algoritmo de Dijkstra para obtener las distancias y la ruta más corta
distancias, camino_corto = dijkstra(grafo, ciudad_inicio)

# Función que reconstruye la ruta más corta y calcula su costo acumulado
def reconstruir_camino(camino_corto, distancias, inicio, fin):
    camino = []  # Lista para almacenar la ruta más corta
    actual = fin  # Comienza desde el nodo final
    costo_total = distancias[fin]  # El costo total es la distancia del nodo final
    
    # Mientras no se llegue al nodo inicial
    while actual != inicio:
        camino.append(actual)  # Añade el nodo actual a la ruta
        actual = camino_corto.get(actual)  # Obtiene el nodo anterior en la ruta
    camino.append(inicio)  # Añade el nodo inicial
    return camino[::-1], costo_total  # Devuelve la ruta invertida (de inicio a fin) y el costo total

# Función para graficar el grafo y la ruta más corta
def graficar_grafo(grafo, camino_corto, distancias, inicio, fin):
    G = nx.DiGraph()  # Crea un grafo dirigido
    # Añade las aristas del grafo (nodos y pesos de las aristas)
    for nodo, vecinos in grafo.items():
        for vecino, peso in vecinos.items():
            G.add_edge(nodo, vecino, peso=peso)
    
    pos = nx.spring_layout(G)  # Determina las posiciones de los nodos para la visualización
    plt.figure(figsize=(12, 8))  # Ajusta el tamaño de la figura para la visualización

    # Dibuja todos los nodos y aristas del grafo
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=1500, font_size=10)
    etiquetas = nx.get_edge_attributes(G, 'peso')  # Obtiene los pesos de las aristas
    nx.draw_networkx_edge_labels(G, pos, edge_labels=etiquetas)  # Dibuja los pesos de las aristas

    # Resalta la ruta más corta en rojo y los nodos en naranja
    camino, costo_total = reconstruir_camino(camino_corto, distancias, inicio, fin)
    aristas_en_camino = [(camino[i], camino[i+1]) for i in range(len(camino) - 1)]  # Aristas en la ruta más corta
    nx.draw_networkx_edges(G, pos, edgelist=aristas_en_camino, edge_color='red', width=2.5)  # Resalta las aristas de la ruta
    nx.draw_networkx_nodes(G, pos, nodelist=camino, node_color='orange')  # Resalta los nodos de la ruta más corta

    # Muestra el título con el costo total
    plt.title("Ruta más corta de " + inicio + " a " + fin + " (Costo acumulado: " + str(costo_total) + ")")
    plt.show()  # Muestra el grafo

# Ejemplo: Mostrar la ruta más corta de INICIO a una desdeada de A a J
ciudad_fin = 'I'  # Nodo final
graficar_grafo(grafo, camino_corto, distancias, ciudad_inicio, ciudad_fin)  # Llama a la función para graficar el grafo

# Mostrar la ruta más corta y su costo acumulado
camino, costo_total = reconstruir_camino(camino_corto, distancias, ciudad_inicio, ciudad_fin)
print("\nRuta más corta de " + ciudad_inicio + " a " + ciudad_fin + ": " + " -> ".join(camino))  # Imprime la ruta
print("Costo acumulado: " + str(costo_total))  # Imprime el costo total
