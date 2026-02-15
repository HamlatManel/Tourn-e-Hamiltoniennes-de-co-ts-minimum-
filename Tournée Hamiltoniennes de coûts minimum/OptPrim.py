import heapq
from utils import calculer_matrice_distances, calculer_longueur_cycle, generer_points, afficher_tournee

def OptPrim(points, D, depart=0):
    """
    Implémentation de la stratégie par l'arbre couvrant de poids minimum (Section 2.3).
    Prend en entrée la liste des points et la matrice de distances D.
    Retourne le cycle hamiltonien et sa longueur.
    """
    n = len(points)

    # --- PARTIE 1 : Algorithme de Prim (Version efficace avec file de priorité) ---
    # On construit une liste d'adjacence pour stocker l'arbre
    acm = {i: [] for i in range(n)}
    visites = [False] * n
    # File de priorité : (poids_arete, sommet_actuel, sommet_parent)
    file_prio = [(0, depart, -1)]

    while file_prio:
        poids, u, parent = heapq.heappop(file_prio)

        if visites[u]:
            continue

        visites[u] = True
        if parent != -1:
            # On ajoute l'arête à notre arbre couvrant
            acm[parent].append(u)
            acm[u].append(parent)

        # On regarde les voisins non visités
        for v in range(n):
            if not visites[v]:
                heapq.heappush(file_prio, (D[u, v], v, u))

    # --- PARTIE 2 : Parcours préfixe (DFS) ---
    # Le parcours préfixe de l'ACM donne le cycle hamiltonien (2-approximation)
    cycle = []
    deja_dans_cycle = [False] * n

    def dfs(u):
        deja_dans_cycle[u] = True
        cycle.append(u)
        for voisin in acm[u]:
            if not deja_dans_cycle[voisin]:
                dfs(voisin)

    dfs(depart)

    # Calcul de la longueur totale avec la fonction commune de utils.py
    longueur = calculer_longueur_cycle(cycle, D)

    return cycle, longueur

# --- Zone de test pour Pyzo ---
if __name__ == "__main__":
    # Test sur 10 points
    n_test = 10
    mes_points = generer_points(n_test)
    matrice_D = calculer_matrice_distances(mes_points)

    print(f"Exécution de OptPrim sur {n_test} points...")
    mon_cycle, ma_longueur = OptPrim(mes_points, matrice_D)

    print(f"Cycle trouvé : {mon_cycle}")
    print(f"Longueur totale : {ma_longueur:.4f}")

    # Optionnel : Afficher le résultat si vous avez ajouté la fonction à utils.py
    from utils import afficher_tournee
    afficher_tournee(mes_points, mon_cycle, "Approximation par Prim (OptPrim)")