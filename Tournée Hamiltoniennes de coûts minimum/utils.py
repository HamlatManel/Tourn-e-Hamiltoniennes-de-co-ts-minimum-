import numpy as np
import matplotlib.pyplot as plt

def generer_points(n):
    """Génère n points aléatoires dans le carré [0, 1] x [0, 1]"""
    return np.random.rand(n, 2)

def calculer_matrice_distances(points):
    """
    Calcule la matrice D de dimension n x n où
    D[i, j] contient la distance euclidienne entre le point i et le point j.
    """
    n = len(points)
    D = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            # Utilisation de la norme euclidienne de numpy
            dist = np.linalg.norm(points[i] - points[j])
            D[i, j] = D[j, i] = dist
    return D

def calculer_longueur_cycle(cycle, D):
    """
    Calcule la longueur totale d'une tournée (cycle).
    Le cycle est une liste d'indices, ex: [0, 3, 1, 2]
    """
    longueur = 0
    n = len(cycle)
    for i in range(n - 1):
        longueur += D[cycle[i], cycle[i+1]]

    # Très important : on ajoute le retour du dernier point au premier
    longueur += D[cycle[-1], cycle[0]]
    return longueur

def charger_points_fichier(nom_fichier):
    """
    Charge des points depuis un fichier texte.
    Format attendu par ligne : (x, y)
    """
    points = []
    try:
        with open(nom_fichier, 'r') as f:
            for ligne in f:
                # Nettoyage de la ligne pour extraire x et y
                s = ligne.strip().replace('(', '').replace(')', '')
                if s:
                    coords = s.split(',')
                    points.append([float(coords[0]), float(coords[1])])
        return np.array(points)
    except FileNotFoundError:
        print(f"Erreur : Le fichier {nom_fichier} n'a pas été trouvé.")
        return None

def afficher_tournee(points, cycle, titre="Tournée Hamiltonienne"):
    """
    Affiche graphiquement les points et le chemin parcouru.
    """
    plt.figure(figsize=(10, 7))

    # On réordonne les points selon le cycle pour le tracé
    # On ajoute le premier point à la fin pour fermer le cycle sur le graphe
    X = [points[i][0] for i in cycle] + [points[cycle[0]][0]]
    Y = [points[i][1] for i in cycle] + [points[cycle[0]][1]]

    # Tracé des points et des lignes
    plt.plot(X, Y, 'ro-', markersize=8, label="Chemin")

    # Ajout des étiquettes (P0, P1, etc.)
    for i, p in enumerate(points):
        plt.annotate(f" P{i}", (p[0], p[1]), fontsize=12, color='blue')

    plt.title(titre)
    plt.xlabel("Coordonnée X")
    plt.ylabel("Coordonnée Y")
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend()
    plt.show()

# ==========================================
# EXEMPLES DE TESTS (S'exécute seulement si on lance ce fichier)
# ==========================================
if __name__ == "__main__":
    print("--- Test de la génération de points ---")
    n_test = 5
    mes_points = generer_points(n_test)
    print(f"Points générés :\n{mes_points}\n")

    print("--- Test de la matrice de distances ---")
    D_test = calculer_matrice_distances(mes_points)
    print(f"Matrice D (5x5) :\n{D_test}\n")

    print("--- Test du calcul de longueur ---")
    # On crée un cycle simple 0 -> 1 -> 2 -> 3 -> 4 (et retour à 0 automatique)
    mon_cycle = [0, 1, 2, 3, 4]
    longueur = calculer_longueur_cycle(mon_cycle, D_test)
    print(f"Longueur du cycle [0,1,2,3,4] : {longueur:.4f}")

    print("\n--- Test de l'affichage ---")
    print("Fermez la fenêtre du graphique pour arrêter le test.")
    afficher_tournee(mes_points, mon_cycle, "Test de visualisation")