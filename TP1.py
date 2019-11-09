# Cherche dit si un chemin existe
# pas : sommets déja traversés
def ChercheChemin(dep,arr,pas = [], chemin = []):

    isPosible = False
    suiv_prepa = []
    isFirst = False

    # first element
    if pas == []:
        pas.append(dep)
        isFirst = True

    chemin.append(dep)

    # prepare list
    for som in suiv[dep] :
        if som not in pas:
            suiv_prepa.append(som)
            pas.append(som)

    isPosible = (dep == arr)
    # suiv
    for suivant in suiv_prepa:
        # check si c'est déja passé par là

        if isPosible == False :
            isPosible = ChercheChemin(suivant,arr,pas,chemin)

        else :


             break

    if isFirst:
        # reformat
        i = 0

        while i < len(chemin) - 1:
            print("arc ( " + str(chemin[i]) + " , " + str(chemin[i + 1]) + " )")
            i += 1

        if len(chemin) == 1:
            print("arc ( " + str(dep) + " , " + str(arr) + " )")

    return isPosible



file_graph = 'graph_TP1.txt'
# Read the doc
TheGraph = open(file_graph, 'r')
all_arcs = TheGraph.readlines()

# Remove tab
Origin = []
Destination = []

for arc in all_arcs:
    this_arc = arc.split("\t")
    orig = int(this_arc[0])
    dest = int(this_arc[1].strip("\n"))
    Origin.append(orig)
    Destination.append(dest)
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

# print('NBArcs : ' + str(NBArcs))
# print('NBVertics : ' + str(NbVertices))
# print(suiv)
# print(prec)

print(ChercheChemin(4,14))