# PPP = Point le Plus Proche
from utils import calculer_longueur_cycle


def ppp(D, depart=0):
    """
    Retourne (cycle, longueur).
    - D : matrice des distances (n x n)
    - depart : sommet de depart (0..n-1)
    """

    n = int(D.shape[0])

    if n == 0:
        return [], 0.0
    if n == 1:
        return [0], 0.0
    if n == 2:
        cycle = [depart, 1 - depart] if depart in (0, 1) else [0, 1]
        return cycle, float(calculer_longueur_cycle(cycle, D))

    cycle = [depart]
    non_visites = set(range(n))
    non_visites.remove(depart)

    while non_visites:
        # 1) Choisir le point "q" hors cycle le plus proche du cycle
        meilleur_q = None
        meilleure_distance = float("inf")
        ancre = None  # sommet du cycle le plus proche de q

        for q in non_visites:
            distance_q_cycle = float("inf")
            sommet_proche = None
            for v in cycle:
                d = D[q, v]
                if d < distance_q_cycle:
                    distance_q_cycle = d
                    sommet_proche = v

            if distance_q_cycle < meilleure_distance:
                meilleure_distance = distance_q_cycle
                meilleur_q = q
                ancre = sommet_proche

        q = meilleur_q

        # 2) Inserer q au meilleur endroit autour de l'ancre
        m = len(cycle)
        indice_ancre = cycle.index(ancre)

        if m == 1:
            cycle.append(q)
        else:
            precedent = cycle[(indice_ancre - 1) % m]
            suivant = cycle[(indice_ancre + 1) % m]

            # Gain si on insere entre precedent -- ancre
            gain_precedent = (D[precedent, q] + D[q, ancre]) - D[precedent, ancre]

            # Gain si on insere entre ancre -- suivant
            gain_suivant = (D[ancre, q] + D[q, suivant]) - D[ancre, suivant]

            if gain_precedent <= gain_suivant:
                # on met q avant l'ancre
                cycle.insert(indice_ancre, q)
            else:
                # on met q apres l'ancre
                cycle.insert(indice_ancre + 1, q)

        non_visites.remove(q)

    longueur = float(calculer_longueur_cycle(cycle, D))
    return cycle, longueur
