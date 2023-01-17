import random as rd
import numpy as np

def afficherMatrice(P):
    for i in P:
        print(i)

def Carto(n):
    mat = np.zeros([n,n])
    for i in range(len(mat)):
        for j in range(i):
            if(i!=j):
                distance = rd.randrange(0,1000)
                mat[i,j] = distance
                mat[j,i] = distance
    return mat

def Populat(n, m):
    P = []
    villes = [i+1 for i in range(n)]

    for i in range(m):
        solution = []
        solution.append(villes[0])
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

def CalculAdapt(chemin):
    somme = 0
    for etape in range(len(chemin)-1):
        noeud1 = chemin[etape]
        noeud2 = chemin[etape+1]
        somme += distances[noeud1-1, noeud2-1]
    somme += distances[chemin[len(chemin)-1]-1, 0]
    return somme

def SelectElit(P):
    classement = {}
    for i in P:
        classement[CalculAdapt(i)] = i
    dictTrie = (sorted(classement.items())[0:int(len(classement)/2)])
    res =[]
    for value in dictTrie:
        res.append(value[1])
    return res

def SelectTourn(P):
    liste = P
    res = []
    print(3//2)
    for i in range(len(P)//2):
        elem1 = liste.pop(rd.randrange(0,len(liste)))
        elem2 = liste.pop(rd.randrange(0,len(liste)))
        if(CalculAdapt(elem1) < CalculAdapt(elem2)):
            res.append(elem1)
        else:
            res.append(elem2)
    return res

def CroisementBis(p1, p2, i, j):
    
    fils = list()
    fils.append(p1[0])
    i-= 1
    for k in p2[i:i+j] :
        fils.append(k)
        
    for j in p1[i+j:]:
        fils.append(j)
    
    tempin = list()
    for elem in fils :
        if elem not in tempin :
            tempin.append(elem)
    
    for elem2 in p1:
        if elem2 not in tempin:
            tempin.append(elem2) 
    
    return tempin

def Croisement(p1, p2, i, j):
    fils1 = CroisementBis(p1,p2,i,j)
    fils2 = CroisementBis(p2,p1,i,j)

    return fils1, fils2

distances = Carto(5)

if __name__ == '__main__':
    print(distances)
    solution = [[1,2,3,4,5],[1,5,3,2,4]]
    print(SelectTourn(solution))
