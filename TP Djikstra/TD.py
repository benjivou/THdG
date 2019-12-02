import os
import math
import time
from tkinter import *
time_start = time.perf_counter()


file_arc = 'Arcs.csv'
file_noeuds = 'Noeuds.csv'

infinity = 99999999
infinityB = infinity +1

sommet_depart = 23160
sommet_destination = 27195
degre_version_radian = math.pi/180.0
# Read the doc
TheArcs = open(file_arc, 'r')
TheNoeuds = open(file_noeuds, 'r')

all_arcs = TheArcs.readlines()
all_noeuds = TheNoeuds.readlines()

TheNoeuds.close()

# Noeuds
Longitude = []
Latitudes = []

for un_noeud in all_noeuds:
    ce_noeud = un_noeud.split("\t")
    noeud = int(ce_noeud[0])
    Long = float(ce_noeud[1])
    Long = Long*degre_version_radian
    Longitude.append(Long)

    Lat = float(ce_noeud[2].strip("\n"))
    Lat = Lat *degre_version_radian
    Latitudes.append(Lat)

minLat = min(Latitudes)
maxLat = max(Latitudes)
minLong = min(Longitude)
maxLong = max(Longitude)
NbNoeuds = len(Longitude)

# Remove tab
Origin = []
Destination = []
Longueur = []

for arc in all_arcs:
    this_arc = arc.split("\t")
    orig = int(this_arc[0])
    dest = int(this_arc[1].strip("\n"))
    valeur = int(this_arc[2].strip("\n"))
    Origin.append(orig)
    Destination.append(dest)
    Longueur.append(valeur)
    # Create previous / after

NbVertices = max(max(Origin), max(Destination)) + 1

suiv = [[] ]*NbVertices
longSuiv = [[] ]*NbVertices

NBArcs = len(Origin)

for arc in all_arcs:
    this_arc = arc.split("\t")
    orig = int(this_arc[0])
    dest = int(this_arc[1].strip("\n"))
    valeur = int(this_arc[2].strip("\n"))
    suiv[orig].append(dest)
    longSuiv[orig].append(valeur)




def Djikstra(startpos,finpos):


    Poids= [infinity] *NbVertices  # Sauvegarde le poids le plus petit pour rejoindre les points
    PrecBlockage = [-1] *NbVertices      # Sauvegarde La precedence du plus court chemin


    # pos de départ
    Poids[startpos] = 0
    PrecBlockage[startpos] = startpos
    # Debut du code
    while True :
        # recupération de l'index du min
        debutLongueur = min(Poids)


        if (debutLongueur == infinity): break; # vérifie si le problème a une solution

        debut = Poids.index(debutLongueur)
        TraceCercle(debut, 'yellow', rayon_noeud)

        # etat final bon
        if debut == finpos:
            break;

        # On efface le poids
        Poids[debut] = infinityB

        # comparer les valeurs des arcs
        # Trouver les nouveaux arcs

        if   debut not in Origin :
            continue

        posPremArc = Origin.index(debut)
        # Nombre des valeurs origines

        count = 0
        while Origin[posPremArc + count] == debut:
            dst = Destination[posPremArc+count]
            long = Longueur[posPremArc+count]
            # modifier les sommets : sauvegarde des nouvelles distances
            nvlDistance = debutLongueur + long

            if Poids[dst] != infinityB and Poids[dst] > nvlDistance:
                Poids[dst] = nvlDistance    # sauvegarde le point le plus petit
                PrecBlockage[dst] = debut   # sauvegarde la provenance

            count += 1

    #     Recupére le plus court chemin


    if(PrecBlockage[finpos] != -1):
        currentPos = finpos

        while currentPos != startpos:
            TraceCercle(currentPos, 'purple', 2* rayon_noeud)
            currentPos = PrecBlockage[currentPos]

        TraceCercle(currentPos, 'purple', 2*rayon_noeud)

    return

def Dji2(starpos,endpos):
    #  Info par Arcs
    Origin_dec = Origin
    Destination_dec = Destination
    Longueur_dec = Longueur

    #  Info par Sommets
    Sommets_act = []
    Preced_act = []
    for i  in range(0,NbVertices):
        Sommets_act.append(i)
        Preced_act.append(i)
    print(Sommets_act[1])
    Poids_act = [infinity]*NbVertices


    # resultat final
    Sommets_fin=[]
    Poids_fin=[]
    Preced_fin=[]

    # Step 1 : initialisation
    Poids_act[starpos] = 0

    # Step 2 : Boucle

    while True :
         # Step 2.1 :Recupération du sommet et de son plus court chemin
        poids_depart = min(Poids_act)
        pos_dans_index = Poids_act.index(poids_depart)

        sommet_nom_depart = Sommets_act[pos_dans_index]
        precedence_depart = Preced_act[pos_dans_index]

        # Step 2.2 :Test des cas terminaux
        #  On a trouvé la fin
        if  sommet_nom_depart == endpos :
            Poids_fin.append(poids_depart)
            Sommets_fin.append(sommet_nom_depart)
            Preced_fin.append(precedence_depart)
            break;

        # Impossible de rejoindre le sommet
        if poids_depart == infinity :
            print("Chemin introuvable")
            return

         # Step 2.3 :Tracage du sommet
        TraceCercle(sommet_nom_depart, 'yellow', rayon_noeud)

        # Step 2.4 : Mise à jour des nouveaux sommets destinations
        if  sommet_nom_depart in Origin_dec :

             posPremArc = Origin_dec.index(sommet_nom_depart)

             while Origin[posPremArc ] == sommet_nom_depart:
                 dst = Destination_dec[posPremArc]
                 long = Longueur_dec[posPremArc]

                 #  supression du sommet
                 del Origin_dec[posPremArc]
                 del Longueur_dec[posPremArc]
                 del Destination_dec[posPremArc]

                 # modifier les sommets : sauvegarde des nouvelles distances
                 nvlDistance = poids_depart + long

                 if  dst in Sommets_act and Poids_act[Sommets_act.index(dst)] > nvlDistance:
                     Poids_act[Sommets_act.index(dst)] = nvlDistance  # sauvegarde le point le plus petit
                     Preced_act[Sommets_act.index(dst)] = sommet_nom_depart  # sauvegarde la provenance



        # On met à jour les listes act et fin
        del Poids_act[pos_dans_index]
        del Sommets_act[pos_dans_index]
        del Preced_act[pos_dans_index]

        Poids_fin.append(poids_depart)
        Sommets_fin.append(sommet_nom_depart)
        Preced_fin.append(precedence_depart)

    # on passe à la phase d'écriture dans le graphe des sommets du plus cours chemin
    current_precedence = Preced_fin[len(Preced_fin)-1]
    while current_precedence != starpos:
        TraceCercle(current_precedence, 'purple', 2 * rayon_noeud)
        current_precedence = Preced_fin[Sommets_fin.index(current_precedence)]

    TraceCercle(endpos, 'purple', 2 * rayon_noeud)
    print("chelin trouvé")
    return

def DjikstraV2(startpos,endpos):
    fini = False

    # Liste

    # Sauvegarde des potentiels
    Potentiels = [infinity] * NbVertices
    Marque = [False] * NbVertices
    SommetsPrecedents = [-1] * NbVertices
    Candidats = []

    # Initialisation
    Marque[startpos] = True
    Potentiels[startpos] = 0
    for k in suiv[startpos] :
        ind_k = suiv[startpos].index(k)
        Potentiels[k]=longSuiv[startpos][ind_k]
        Candidats.append(k)

    while fini == False:
        # Récupération des infos du sommet min
        potmin = infinity
        for j in Candidats:
            if not Marque[j] and Potentiels[j]< potmin:
                potmin = Potentiels[j]
                ce_sommet = j

        Marque[ce_sommet] = True

        # Marquage
        TraceCercle(ce_sommet,"yellow", rayon_noeud)

        if ce_sommet == endpos :
            fini = True


def TraceCercle(j,couleur,rayon):
    x=(Longitude[j]-minLong)*ratioWidth + border
    y=(Latitudes[j]-minLat)*ratioHeight+ border
    y=winHeight-y
    can.create_oval(x-rayon, y-rayon, x+rayon, y+rayon, outline = couleur, fill = couleur)

fen = Tk()
fen.title('Carte de Paris')
coul_fond = "grey"   #['purple','cyan','maroon','green','red','blue','orange','yellow']
coul_noeud = "black"

Delta_Long = maxLong-minLong
Delta_Lat = maxLat-minLat

border = 20         # taille en px des bords
winWidth_int = 900
winWidth = winWidth_int+2*border     # largeur de la fenetre
winHeight_int = Delta_Lat*(winWidth_int/0.8)/Delta_Long
winHeight = winHeight_int+2*border     # hauteur de la fenetre : recalculee en fonction de la taille du graphe
ratio= 1.0          # rapport taille graphe / taille fenetre
ratioWidth = winWidth_int/Delta_Long       #  rapport largeur graphe/ largeur de la fenetre
ratioHeight = winHeight_int/Delta_Lat       #  rapport hauteur du graphe hauteur de la fenetre

can = Canvas(fen, width = winWidth, height = winHeight, bg =coul_fond)
can.pack(padx=5,pady=5)

#  cercles
rayon_noeud = 1  # rayon pour dessin des points
rayon_od = 5     # rayon pour origine et destination

for i in range(0,NbNoeuds):
    TraceCercle(i,coul_noeud,rayon_noeud)
TraceCercle(sommet_depart,'green',rayon_od)
TraceCercle(sommet_destination,'red',rayon_od)

def Arc (i,j):
    # chercher la position de l'origine dans les arcs
    posDeb = Origin.index(i)

    # compter les positions
    count = 0
    while Origin[posDeb+count] == i :
        count+=1

    # On recherche l'Arc i,j
    iterator = 0;
    while Destination[posDeb + iterator] != j and  iterator<count :
        iterator+=1

    res = -1
    # si l'arc existe
    if iterator < count:
        res = posDeb+iterator + 1

    return res


# determine le temps de départ






DjikstraV2(sommet_depart,sommet_destination)
time_stop = time.perf_counter()
print(" le programme a été exéxté en (secondes) ", time_stop-time_start)
can.mainloop()


