import random as rd
import numpy as np

def afficherMatrice(P:list):
    """
    fonction d'affichage d'une matrice numpy
    """
    for i in P:
        print(i)

def Carto(n:int):
    """
    fonction de génération d'une matrice aléatoire
    à diagonale vide des distances entre n villes
    """
    mat = np.zeros([n,n])   # on génère une matrice de zéros n*n
    for i in range(len(mat)):
        for j in range(i):
            if(i!=j):
                distance = rd.randrange(0,1000)
                mat[i,j] = distance     # la distance entre i et j est égale à celle entre j et i
                mat[j,i] = distance
    return mat

def Populat(n:int, m:int):
    """
    fonction prenant comme paramètres d'entrée le nombre n de villes et le
    nombre 2m de solutions (individus) que l'on souhaite générer et qui renvoie une matrice P
    de solutions aléatoires. Utilisée pour la population de départ
    """
    P = []
    villes = [i+1 for i in range(n)] # liste croissante des numéros de villes

    for i in range(m):
        solution = []
        solution.append(villes[0]) # on ajoute la ville numéro 1
        nb = rd.randint(1, n-1)

        for j in range(n-1):
            if villes[nb] not in solution :
                solution.append(villes[nb])
            else :
                while (villes[nb] in solution):
                    nb = rd.randint(1, n-1)
                solution.append(villes[nb])
        if solution in P:
            i -= 1
        P.append(solution)
    return P

def CalculAdapt(chemin:list, distances:list):
    """
    fonction qui prend comme paramètre d'entrée une solution (un individu)
    et la matrice des distances entre les villes et qui renvoie la distance
    totale parcourue si l'on suit ce trajet.
    """
    somme = 0
    for etape in range(len(chemin)-1):
        noeud1 = chemin[etape]
        noeud2 = chemin[etape+1]
        somme += distances[noeud1-1, noeud2-1]
    somme += distances[chemin[len(chemin)-1]-1, 0]
    return somme

def SelectElit(P:list, distances:list):
    """
    fonction qui prend en paramètre une population P de 2m individus
    et la matrice des distances entre les villes
    et qui renvoie les m meilleures solutions.
    Il s'agit d'une sélection élitiste
    """
    classement = {}
    for i in range(len(P)):
        classement[i] = CalculAdapt(P[i],distances)  # on ajoute l'index de chaque individu avec le trajet dans un dictionnaire
    # on trie le dictionnnaire sur la valeur (le trajet), les meilleurs individus se retrouvent à la 1ère moitié qu'on garde
    dictTrie = sorted(classement.items(), key=lambda x:x[1])[0:int(len(classement)/2)]
    res =[]
    for value in dictTrie:
        res.append(P[value[0]])    # on ajoute les individus via leur indice dans P
    return res

def SelectTourn(P:list, distances:list):
    """
    fonction qui prend en paramètre une population P de 2m individus
    et la matrice des distances entre les villes et qui renvoie m solutions.
    Il s'agit d'une sélection par tournoi
    """
    liste = []   # liste modifiable identique à la population
    for i in P:
        liste.append(i)
    res = []
    for i in range(len(P)//2):
        elem1 = liste.pop(rd.randrange(0,len(liste)))
        elem2 = liste.pop(rd.randrange(0,len(liste)))
        if(CalculAdapt(elem1, distances) < CalculAdapt(elem2, distances)):
            res.append(elem1)
        else:
            res.append(elem2)
    
    return res

def CroisementBis(p1, p2, i, j):
    """
    Cette fonction prend en parametre deux individus et deux indices, la valeur de debut i de croisement
    et la largeur j du croisement. Les j valeurs de p2 d'indice i seront croisé avec la liste p1
    """
    fils = list() #enfant temporaire
    fils.append(p1[0]) #on ajoute la premiere ville
    i-= 1 #parce qu'on commence a l'indice 0
    for deb in p1[:i-1]: #Ajout des valeurs avant le croisement
        fils.append(deb)

    for larg in p2[i:i+j] : #Ajout des valeurs a croiser
        fils.append(larg)

    for fin in p1[i+j:]: #Ajout des dernieres valeurs
        fils.append(fin)

    #liste qui va stocker les valeurs sans les doublons, ils seront remplacer par 'X' en cas de doublons
    tempin = list()

    for elem in fils : #parcours de fils pour faire des comparaisons
        if elem not in tempin : #si il n'est pas, on l'ajoute
            tempin.append(elem)
        else : #cas du doublon, on le remplace par 'X'
            tempin.append('X')

    #liste temp avec les valeurs non présente dans fils
    tempout = list()
    for doublon in p1:
        if doublon not in fils: #si pas présent dans fils, on l'ajoute a la liste tempout
            tempout.append(doublon)

    compteur_tempout = 0 #compteur d'indice pour tempout
    for ind in range(len(tempin)): # on parcours tempin
        if tempin[ind] == 'X': #case "vide", on la remplace avec les valeurs de tempout
            tempin[ind] = tempout[compteur_tempout]
            compteur_tempout+=1 #incrementation du compteur

    return tempin

def Croisement(p1, p2, i, j):
    """
    Cette fonction prend en parametre deux individus et deux indices, la valeur de debut i de croisement
    et la largeur j du croisement. Elle fait appel a la fonction CroisementBis 2 fois pour les deux listes
    en inversant l'ordre des parametres
    """
    #croisement de p1 avec les valeurs de p2
    fils1 = CroisementBis(p1,p2,i,j)
    #croisement de p2 avec les valeurs de p1
    fils2 = CroisementBis(p2,p1,i,j)

    return fils1, fils2

def Mutation(individu):
    """
    Cette fonction prend en parametre un individu et retourne ce meme individu avec
    deux indices permuté aléatoirement
    """
    # on genere deux nombres aléatoire entre 1 et n
    i = rd.randrange(1, len(individu))
    j = rd.randrange(1, len(individu))
    #on inverse les valeurs pour les deux indices
    individu[i], individu[j] = individu[j], individu[i]

    return individu

def SelectBest(P:list, distances:list):
    """
    fonction qui prend en paramètre une population P de 2m individus
    et la matrice des distances entre les villes
    et qui renvoie la meilleure de ces solutions
    Il s'agit d'une sélection élitiste
    """
    classement = {}
    for i in range(len(P)):
        classement[i] = CalculAdapt(P[i],distances)  # on ajoute l'index de chaque individu avec le trajet dans un dictionnaire
    # on trie le dictionnnaire sur la valeur (le trajet), les meilleurs individus se retrouvent à la 1ère moitié qu'on garde
    dictTrie = sorted(classement.items(), key=lambda x:x[1])[0:int(len(classement)/2)]
    return P[dictTrie[0][0]]

def Genetiq(n:int, m:int, t:int, c:str, iters:int):
    """
    fonction prend en entrée un entier n (nombre de villes), le nombre d'individus, m,
    dans la population initiale, le taux t de la population subissant une mutation à chaque itération,
    la méthode de sélection c choisie (élitiste ou par tournoi) et le nombre iters d'itérations.
    Cette fonction donne en sortie la meilleure des solutions.
    """
    # on initialise la population de départ et la matrice puis on calcule le nombre d'individus à muter
    P = Populat(n,m)
    carte = Carto(n)
    pourcentage = int(t*m/100)

    for iteration in range(iters):
        # Sélection
        if(c=="élitiste"):
            P = SelectElit(P,carte)
        elif(c=="par tournoi"):
            P = SelectTourn(P,carte)
        # Croisement
        for i in range(len(P)//2):
            fils = Croisement(P[i], P[-(i+1)], 2, 3)    # on ajoute les fils générés à la population
            P.append(fils[0])
            P.append(fils[1])
        if( (m%2==0 and len(P)%2!=0) or (m%2!=0 and len(P)%2==0)):    # cas d'une population à effectif impair
            index_milieu = int(len(P)/2-0.5)
            index_random = rd.randrange(0,len(P))
            fils = Croisement(P[index_milieu],P[index_random],2,3)
            P.append(fils[1]) # on ajout un fils sur les 2 pour avoir le même nombre d'individus
        # Mutation
        for i in range(pourcentage):
            index = rd.randrange(0,len(P))     # mutation aléatoire de t% des individus
            P[index] = Mutation(P[index])
    return SelectBest(P,carte)

if __name__ == '__main__':
    distance = Carto(5)
    print("Carto : ")
    afficherMatrice(distance)
    pop = Populat(5,6)
    print("Populat : ",pop)
    print("CalculAdapt : ", CalculAdapt(pop[0],distance))
    print("SelectElit : ", SelectElit(pop,distance))
    print("SelectTourn : ", SelectTourn(pop,distance))
    print("Croisement et CroisementBis : ", Croisement(pop[0],pop[1],2,3))
    print("Mutation : ", Mutation(pop[0]))
    print("Genetiq et SelectBest élitiste : ",Genetiq(5,6,50,"élitiste",10))
    print("Genetiq et SelectBest par tournoi : ",Genetiq(5,6,50,"par tournoi",10))