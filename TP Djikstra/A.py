from tkinter import *
import os
import math
import time

fichier_noeuds = "Noeuds.csv"
fichier_arcs = "Arcs.csv"

sommet_depart = 23160
sommet_arrivee = 27195
degre_vers_radian = math.pi / 180

############ Lecture Noeuds #############
print("Lecture Noeuds")
noeuds = open(fichier_noeuds, "r")
# format du fichier : indice \t long \t lat \n
touslesnoeuds = noeuds.readlines()
noeuds.close()

Longitude = []
Latitude = []

for un_noeud in touslesnoeuds:
    #decoupage du contenu de la ligne
    ce_noeud = un_noeud.split("\t")
    noeud = int(ce_noeud[0])
    Long = float(ce_noeud[1])
    Long = Long * degre_vers_radian #conversion en radian
    Longitude.append(Long)
    Lat = float(ce_noeud[2].strip("\n"))
    Lat = Lat * degre_vers_radian #conversion en radian
    Latitude.append(Lat)

minLat = min(Latitude)
maxLat = max(Latitude)
minLong = min(Longitude)
maxLong = max(Longitude)
NbNoeuds = len(Longitude)


############ Lecture Arcs #############
print("Lecture Arcs")
arcs = open(fichier_arcs, "r")
#format du fichier : origine \t destination \t longueur \t dangerosite \n
touslesarcs = arcs.readlines()
arcs.close()

Origine = []
Destination = []
Longueur = []
Dangerosite = []
suiv = [[] for j in range(NbNoeuds)]
suivLong = [[] for j in range(NbNoeuds)]

for un_arc in touslesarcs:
    cet_arc = un_arc.split("\t")
    Orig = int(cet_arc[0])
    Origine.append(Orig)

    Dest = int(cet_arc[1])
    Destination.append(Dest)

    Long = int(cet_arc[2])
    Longueur.append(Long)

    Dang = int(cet_arc[3].strip("\n"))
    Dangerosite.append(Dang)

    suiv[Orig].append(Dest)
    suivLong[Orig].append(Long)

NbArcs = len(Origine)
print('NbArcs=', NbArcs)


# permet d'inseré de manière ordonnée dans une liste
def insertion_ordonnée(list,newElement):
    i = 0

    while i < len(list) :
        if  newElement < list[i]:
            break
        i+=1

    list.insert(i,newElement)
    return i

def refresh(Pot,Num,Prec,Pic,sommet,potentiel,prec):
    modifiable = True
    dstVol = Distance_vol_oiseau(sommet) +potentiel ;
    # on cherche si le sommet est bien dans la liste
    try :

        pos = Num.index(sommet);

    #     On oublie pas de le retirer dans les 2 listes
        if dstVol < Pil_B[pos] :
            Pot.pop(pos)
            Num.pop(pos)
            Pil_B.pop(pos)
        else:
            modifiable = False

    # Le sommet n'était pas dans la liste
    except ValueError:
        pass
    finally:
        if not modifiable:
            return
        pos = insertion_ordonnée(Pil_B,dstVol)
        Num.insert(pos ,sommet)
        Pot.insert(pos,potentiel)
        Prec[sommet] = prec
        Pic[sommet] = potentiel


############ Dijkstra #############
time_start = time.clock()

def Distance_vol_oiseau(villeA):
    xA = Longitude[villeA]
    xB = Longitude[sommet_arrivee]
    yA = Latitude[villeA]
    yB = Latitude[sommet_arrivee]
    R=6372795.477598
    AB = R*math.acos((math.sin(yA)*math.sin(yB)) + math.cos(yA)*math.cos(yB)*math.cos(xA-xB))
    return AB;

def Arc(i,j):
    for index in range(len(Origine)):
        if(Origine[index] == i and Destination[index] == j):
            return index
    return -1

infini = 99999
Pi = [infini for j in range(NbNoeuds)]
Marque = [False for j in range(NbNoeuds)]
LePrec = [-1 for j in range(NbNoeuds)]
Pi[sommet_depart] = 0;
Marque[sommet_depart] = True;

fini = False

progression = 1
ancienIndex = sommet_depart
Candidat = []
Potentiel = []
Pil_B= []
for dest in suiv[sommet_depart]:

    if not (Marque[dest]):
        newPot = Longueur[sommet_arrivee] + Pi[ancienIndex]
        # print(dest, "dazldihazo", Marque[dest], newPot, Pi[dest])
        refresh(Potentiel,Candidat,LePrec,Pi,dest,newPot,sommet_depart)


while len(Candidat) > 0 :
    sommetPlusPetit = Candidat.pop(0)
    currentPotentiel = Potentiel.pop(0)
    Pil_B.pop(0)
    Marque[sommetPlusPetit] = True

    # On a trouvé le sommet d'arrivée
    if sommetPlusPetit == sommet_arrivee:
        fini = True
        break

    else:
        for indexDest in range(len(suiv[sommetPlusPetit])):
            dest = suiv[sommetPlusPetit][indexDest]
            if not (Marque[dest]):
                newPot = suivLong[sommetPlusPetit][indexDest] + Pi[sommetPlusPetit]
                refresh(Potentiel,Candidat,LePrec,Pi,dest,newPot,sommetPlusPetit)



time_end = time.clock()
print(time_end - time_start)
ce_sommet = sommet_arrivee
Chemin = []
while ce_sommet != sommet_depart:
    ce_sommet = LePrec[ce_sommet]
    Chemin.append(ce_sommet)
Chemin.pop(-1)

############ Dessin graphe #############
print('*** Dessin du graphe ***')

def TraceCercle(j,couleur,rayon):
    x=(Longitude[j]-minLong)*ratioWidth + border
    y=(Latitude[j]-minLat)*ratioHeight+ border
    y=winHeight-y
    can.create_oval(x-rayon, y-rayon, x+rayon, y+rayon, outline = couleur, fill = couleur)

def TraceArcs(j1, j2, couleur, ep):
    x1 = (Longitude[j1] - minLong) * ratioWidth + border
    y1 = (Latitude[j1] - minLat) * ratioHeight + border
    y1 = winHeight - y1
    x2 = (Longitude[j2] - minLong) * ratioWidth + border
    y2 = (Latitude[j2] - minLat) * ratioHeight + border
    y2 = winHeight - y2
    can.create_line(x1,y1,x2,y2,fill = couleur, width = ep)

fen = Tk()
fen.title('Carte de Paris')
coul_fond = "white"   #['purple','cyan','maroon','green','red','blue','orange','yellow']
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

# Affichage des points
rayon_noeud = 1  # rayon pour dessin des points
rayon_chemin = 2.5  # rayon pour dessin des points
rayon_od = 5     # rayon pour origine et destination
for i in range(0,NbNoeuds):
    if(Marque[i]):
        if i in Chemin:
            for j in suiv[i]:
                if j in Chemin:
                    TraceArcs(i, j, 'purple', 2)
            TraceCercle(i, 'purple', rayon_chemin)
        else:
            TraceCercle(i, 'yellow', rayon_noeud)
    else:
        TraceCercle(i,coul_noeud,rayon_noeud)

TraceCercle(sommet_depart,'green',rayon_od)
TraceCercle(sommet_arrivee,'red',rayon_od)

fen.mainloop()
