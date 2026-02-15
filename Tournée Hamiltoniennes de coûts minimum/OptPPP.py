from utils import calculer_longueur_cycle

def opt_ppp(cycle, D):
    """
    OptPPP : amélioration possible du cout
    du cycle obtenu par la procedure PPP 
    par décroisement des arêtes qui se croisent
    """
    # n est le nombre de sommets dans le cycle
    n = len(cycle)

    if n <= 3:
    # Le cycle trop court pour appliquer le décroisement
        return cycle, float(calculer_longueur_cycle(cycle, D))
    else:
        while True:  
            changement = False

            for i in range(n - 2):
                for j in range(i + 2, n - 1):
                # On compare le coût actuel et le coût si on décroise les arêtes
                    if D[cycle[i], cycle[i + 1]] + D[cycle[j], cycle[j + 1]] > \
                        D[cycle[i], cycle[j]] + D[cycle[i + 1], cycle[j + 1]]:
                    
                        # On inverser [i+1 .. j] 
                        PLi1 = i + 1
                        PLj = j
                        while PLi1 < PLj:
                            temp = cycle[PLi1]      
                            cycle[PLi1] = cycle[PLj]  
                            cycle[PLj] = temp     
                            PLi1 += 1
                            PLj -= 1
                            
                        changement = True 
                        break  

            # Si aucune amélioration n'est possible on sort de la boucle while
            if changement == False:
                break
    
    return cycle, float(calculer_longueur_cycle(cycle, D))