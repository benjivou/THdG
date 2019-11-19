import os
import math
import time
from tkinter import *




file_arc = 'Arcs.csv'
file_noeuds = 'Noeuds.csv'

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

NBArcs = len(Origin)
NbVertices = max(max(Origin), max(Destination)) + 1

prec = [[] for i in range(NbVertices)]
suiv = [[] for i in range(NbVertices)]

# Travel in the origin
for u in range(0, NbVertices):
    orig = Origin[u]
    dest = Destination[u]
    suiv[orig].append(dest)
    prec[dest].append(orig)

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

can.mainloop()
print(NBArcs)