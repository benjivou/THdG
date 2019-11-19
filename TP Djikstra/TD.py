import os
import math
import time

file_graph = 'Arcs.csv'
# Read the doc
TheGraph = open(file_graph, 'r')
all_arcs = TheGraph.readlines()

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

print(NBArcs)