# HDS = Branch & Bound (exact) avec borne inferieure "demi-somme"

import heapq
from utils import calculer_longueur_cycle
from ppp import ppp


def pre_calcul_voisins_tries(D):
    """Pour chaque sommet v, renvoie les autres sommets tries par distance croissante."""
    n = int(D.shape[0])
    voisins_tries = []
    for v in range(n):
        liste = list(range(n))
        liste.remove(v)
        liste.sort(key=lambda u: D[v, u])
        voisins_tries.append(liste)
    return voisins_tries


def borne_demi_somme(D, voisins_tries, chemin, cout_partiel):
    """
    Borne inferieure demi-somme :
    - Dans un cycle hamiltonien, chaque sommet a degre 2.
    - On complete les degres manquants avec les plus petites aretes possibles.
    - On divise par 2 car chaque arete est comptee deux fois.
    """
    n = int(D.shape[0])
    m = len(chemin)

    # degre_utilise[v] = nombre d'aretes deja imposees autour de v par le chemin partiel
    degre_utilise = [0] * n

    # voisins_fixes[v] = sommets deja relies a v par une arete imposee (dans le chemin)
    voisins_fixes = [set() for _ in range(n)]

    # On ajoute les aretes du chemin partiel (chemin[i] -> chemin[i+1])
    if m >= 2:
        for i in range(m - 1):
            a = chemin[i]
            b = chemin[i + 1]
            degre_utilise[a] += 1
            degre_utilise[b] += 1
            voisins_fixes[a].add(b)
            voisins_fixes[b].add(a)

    # manque[v] = combien d'aretes il manque a v pour arriver a degre 2
    manque = [2 - degre_utilise[v] for v in range(n)]

    # Si un sommet a deja degre 2, on le considere "bloque" (il ne devrait plus recevoir d'aretes)
    bloques = {v for v in range(n) if manque[v] <= 0}

    somme = 0.0

    for v in range(n):
        k = manque[v]
        if k <= 0:
            continue

        total_v = 0.0
        choisi = 0

        # On prend les k plus petites aretes possibles pour v (en evitant les aretes deja fixes)
        for u in voisins_tries[v]:
            if u in voisins_fixes[v]:
                continue
            if u in bloques:
                continue

            total_v += D[v, u]
            choisi += 1
            if choisi == k:
                break

        # Si on ne trouve pas assez d'aretes "possibles", on renvoie inf pour forcer l'elagage
        if choisi < k:
            return float("inf")

        somme += total_v

    return cout_partiel + 0.5 * somme


def hds(D, depart=0, utiliser_ppp_comme_borne_sup=True):
    """
    HDS exact : Branch & Bound (best-first) + borne demi-somme.
    Retourne (meilleur_cycle, meilleure_longueur).
    """
    n = int(D.shape[0])

    if n == 0:
        return [], 0.0
    if n == 1:
        return [0], 0.0
    if n == 2:
        cycle = [depart, 1 - depart] if depart in (0, 1) else [0, 1]
        return cycle, float(calculer_longueur_cycle(cycle, D))

    voisins_tries = pre_calcul_voisins_tries(D)

    # Borne superieure (meilleure solution complete connue)
    meilleure_longueur = float("inf")
    meilleur_cycle = None

    # On initialise souvent UB avec PPP pour elaguer plus vite
    if utiliser_ppp_comme_borne_sup:
        cycle0, l0 = ppp(D, depart=depart)
        meilleur_cycle = cycle0
        meilleure_longueur = float(l0)

    # File de priorite : on explore d'abord les noeuds ayant la plus petite borne inf
    # (borne_inf, cout_partiel, chemin, masque_visite)
    masque_depart = 1 << depart
    chemin_depart = [depart]
    cout_depart = 0.0
    borne_depart = borne_demi_somme(D, voisins_tries, chemin_depart, cout_depart)

    tas = []
    heapq.heappush(tas, (borne_depart, cout_depart, chemin_depart, masque_depart))

    while tas:
        borne, cout_partiel, chemin, masque = heapq.heappop(tas)

        # Elagage : si meme la borne inf depasse la meilleure solution, on coupe
        if borne >= meilleure_longueur:
            continue

        dernier = chemin[-1]

        # Si on a visite tous les sommets, on ferme le cycle
        if len(chemin) == n:
            total = cout_partiel + D[dernier, depart]
            if total < meilleure_longueur:
                meilleure_longueur = float(total)
                meilleur_cycle = list(chemin)
            continue

        # Brancher : on tente d'ajouter un sommet non visite
        # On prend les candidats dans l'ordre des plus proches (souvent efficace)
        for prochain in voisins_tries[dernier]:
            if (masque >> prochain) & 1:
                continue

            nouveau_cout = cout_partiel + D[dernier, prochain]
            if nouveau_cout >= meilleure_longueur:
                continue

            nouveau_chemin = chemin + [prochain]
            nouveau_masque = masque | (1 << prochain)

            nouvelle_borne = borne_demi_somme(D, voisins_tries, nouveau_chemin, nouveau_cout)
            if nouvelle_borne >= meilleure_longueur:
                continue

            heapq.heappush(tas, (nouvelle_borne, nouveau_cout, nouveau_chemin, nouveau_masque))

    if meilleur_cycle is None:
        meilleur_cycle, meilleure_longueur = ppp(D, depart=depart)

    return meilleur_cycle, float(meilleure_longueur)
