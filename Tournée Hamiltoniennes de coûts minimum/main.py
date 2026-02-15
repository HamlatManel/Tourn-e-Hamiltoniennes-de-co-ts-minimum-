import numpy as np
import matplotlib.pyplot as plt

from utils import (
    generer_points,
    calculer_matrice_distances,
    calculer_longueur_cycle,
    afficher_tournee,
    charger_points_fichier,
)

from ppp import ppp    
from hds import hds            
from OptPPP import opt_ppp          
from OptPrim import OptPrim         


def executer_sur_points(points, titre_prefix=""):
    """
    Lance PPP, OptPPP, OptPrim (et HDS si possible) sur un tableau de points.
    Retourne un dictionnaire des longueurs.
    """
    n = len(points)
    D = calculer_matrice_distances(points)

    # 1) PPP
    cycle_ppp, longueur_ppp = ppp(D, depart=0)

    # 2) OptPPP
    cycle_opt, longueur_opt = opt_ppp(cycle_ppp.copy(), D)

    # 3) OptPrim
    cycle_prim, longueur_prim = OptPrim(points, D, depart=0)

    resultats = {
        "n": n,
        "points": points,
        "D": D,
        "cycle_ppp": cycle_ppp,
        "longueur_ppp": float(longueur_ppp),
        "cycle_opt": cycle_opt,
        "longueur_opt": float(longueur_opt),
        "cycle_prim": cycle_prim,
        "longueur_prim": float(longueur_prim),
        "cycle_hds": None,
        "longueur_hds": None,
    }

    # 4) HDS (exact)
    if n <= 11:
        cycle_hds, longueur_hds = hds(D, depart=0, utiliser_ppp_comme_borne_sup=True)
        resultats["cycle_hds"] = cycle_hds
        resultats["longueur_hds"] = float(longueur_hds)

    # Vérifications 
    check_ppp = calculer_longueur_cycle(cycle_ppp, D)
    check_opt = calculer_longueur_cycle(cycle_opt, D)
    check_prim = calculer_longueur_cycle(cycle_prim, D)

    print("\n--- Résultats individuels {}(n={}, départ=0) ---".format(titre_prefix, n))
    print("Longueur PPP     : {:.4f}  (check {:.4f})".format(resultats["longueur_ppp"], check_ppp))
    print("Longueur OptPPP  : {:.4f}  (check {:.4f})".format(resultats["longueur_opt"], check_opt))
    print("Longueur OptPrim : {:.4f}  (check {:.4f})".format(resultats["longueur_prim"], check_prim))

    gain_opt = ((resultats["longueur_ppp"] - resultats["longueur_opt"]) / resultats["longueur_ppp"]) * 100.0
    gain_prim = ((resultats["longueur_opt"] - resultats["longueur_prim"]) / resultats["longueur_opt"]) * 100.0
    print("Gain OptPPP vs PPP     : {:.2f} %".format(gain_opt))
    print("Gain OptPrim vs OptPPP : {:.2f} %".format(gain_prim))

    if resultats["longueur_hds"] is not None:
        check_hds = calculer_longueur_cycle(resultats["cycle_hds"], D)
        print("Longueur HDS (exact)   : {:.4f}  (check {:.4f})".format(resultats["longueur_hds"], check_hds))

    # Affichages
    afficher_tournee(points, cycle_ppp, "{}Cycle PPP".format(titre_prefix))
    afficher_tournee(points, cycle_opt, "{}Cycle OptPPP".format(titre_prefix))
    afficher_tournee(points, cycle_prim, "{}Cycle OptPrim".format(titre_prefix))
    if resultats["cycle_hds"] is not None:
        afficher_tournee(points, resultats["cycle_hds"], "{}Cycle HDS (exact)".format(titre_prefix))
    else:
        print("HDS non exécuté ici (n trop grand).")

    return resultats


def etude_statistique(nb_essais=100, n=30, comparer_hds=False):
    """
    Étude statistique sur des points générés aléatoirement :
    - À chaque essai : on génère de nouveaux points, on calcule D, puis on lance PPP / OptPPP / OptPrim.
    - On calcule lp, lop, lpr + gains.
    - Optionnel : comparaison avec HDS si n petit.
    """
    longueurs_ppp = np.zeros(nb_essais, dtype=float)
    longueurs_opt = np.zeros(nb_essais, dtype=float)
    longueurs_prim = np.zeros(nb_essais, dtype=float)
    longueurs_hds = np.zeros(nb_essais, dtype=float) if comparer_hds else None

    for i in range(nb_essais):
        points = generer_points(n)
        D = calculer_matrice_distances(points)

        depart_hasard = np.random.randint(0, n)

        c_p, l_p = ppp(D, depart=depart_hasard)
        c_o, l_o = opt_ppp(c_p.copy(), D)
        c_pr, l_pr = OptPrim(points, D, depart=depart_hasard)

        longueurs_ppp[i] = float(l_p)
        longueurs_opt[i] = float(l_o)
        longueurs_prim[i] = float(l_pr)

        if comparer_hds:
            
            c_h, l_h = hds(D, depart=depart_hasard, utiliser_ppp_comme_borne_sup=True)
            longueurs_hds[i] = float(l_h)

    lp = float(np.mean(longueurs_ppp))
    lop = float(np.mean(longueurs_opt))
    lpr = float(np.mean(longueurs_prim))

    gain_opt_ppp = ((lp - lop) / lp) * 100.0
    gain_prim_opt = ((lop - lpr) / lop) * 100.0

    print("\n--- Étude statistique finale ({} essais, n={}) ---".format(nb_essais, n))
    print("lp  (moyenne PPP)     : {:.4f}".format(lp))
    print("lop (moyenne OptPPP)  : {:.4f}".format(lop))
    print("lpr (moyenne OptPrim) : {:.4f}".format(lpr))
    print("Gain moyen OptPPP vs PPP     : {:.2f} %".format(gain_opt_ppp))
    print("Gain moyen OptPrim vs OptPPP : {:.2f} %".format(gain_prim_opt))

    if comparer_hds:
        lhds = float(np.mean(longueurs_hds))
        print("lhds (moyenne HDS exact)      : {:.4f}".format(lhds))

    # Représentation visuelle 
    etiquettes = ["PPP", "OptPPP", "OptPrim"]
    valeurs = [lp, lop, lpr]
    if comparer_hds:
        etiquettes.append("HDS")
        valeurs.append(float(np.mean(longueurs_hds)))

    plt.figure()
    plt.bar(etiquettes, valeurs)
    plt.title("Longueurs moyennes sur {} essais (n={})".format(nb_essais, n))
    plt.ylabel("Longueur moyenne")
    plt.grid(True, axis="y", linestyle="--", alpha=0.6)
    plt.show()

    return lp, lop, lpr


def main():
       
    # Fichier de points (mode fichier)
    fichier_points = "10 points.txt" 

    # Taille utilisée pour l’étude statistique (random)
    n_stats = 10
    nb_essais = 100

    # 1) MODE FICHIER (si le fichier existe)
    points_fichier = charger_points_fichier(fichier_points)
    if points_fichier is not None:
        executer_sur_points(points_fichier, titre_prefix="[FICHIER] ")

    # 2) MODE RANDOM 
    points_rand = generer_points(n_stats)
    executer_sur_points(points_rand, titre_prefix="[RANDOM] ")

    # 3) Étude statistique sur 100 essais 
    comparer_hds = (n_stats <= 11)
    etude_statistique(nb_essais=nb_essais, n=n_stats, comparer_hds=comparer_hds)


if __name__ == "__main__":
    main()
