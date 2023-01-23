import sys
import numpy as np
import matplotlib
import matplotlib.pyplot as plt


def swap(l, i, j):
    app = l[i]
    l[i] = l[j]
    l[j] = app
    return l


def BigAreaSort(W, H):

    l = [i for i in range(len(W))]
    for i in range(len(l)):
        for j in range(i+1, len(l)):
            if W[l[i]]*H[l[i]] < W[l[j]]*H[l[j]]:
                l = swap(l, i, j)

    return [W[i] for i in l], [H[i] for i in l]


def loadExercice():
    w = 0
    n = 0
    W = []
    H = []

    filename = ""
    try:
        index = int(sys.argv[1])

        if index < 1 or index > 40:
            filename = "exercices/ins-1.txt"
            print("ins-1.txt")
        else:
            filename = "exercices/ins-"+str(index)+".txt"
            print("ins-", str(index), ".txt")
    except:
        filename = "exercices/ins-1.txt"
        print("ins-1.txt")

    with open(filename, "r") as reader:
        w = int(reader.readline())
        n = int(reader.readline())
        lines = reader.readlines()

        for row in lines:
            W.append(int(row.split(" ")[0]))
            H.append(int(row.split(" ")[1]))

    W, H = BigAreaSort(W, H)
    return w, n, W, H


def plotSolutions(n, w, h, W, H, Xs, Ys, numSol=1, shape=False):

    if numSol > 24:
        numSol = 24

    colors = ' red blue magenta yellow green orange rosybrown lightcoral darkred sienna darkorange darkgoldenrod gold darkkhaki olivedrab yellowgreen darkolivegreen lawngreen palegreen darkseagreen  seagreen springgreen aqua paleturquoise darkslategray cadetblue turquoise steelblue midnightblue cornflowerblue indigo darkviolet mediumorchid orchid lime lightgrey purple  brown pink grey'.split()
    cmap1 = matplotlib.colors.ListedColormap(
        "white "+str(colors), name='colors', N=None)
    cmap = matplotlib.colors.ListedColormap(colors, name='colors', N=None)

    AA = []

    for i in range(numSol):

        map = np.zeros((h, w)).tolist()

        for rect in range(n):
            for row in range(H[rect]):
                for col in range(W[rect]):
                    map[h-1-Ys[i][rect]-row][Xs[i][rect]+col] = rect+1

        AA.append(map)

    num_matrix = len(AA)

    ncol = 4

    if numSol < ncol:
        ncol = numSol
        nrow = 1
    else:
        nrow = int(numSol/ncol)
        if numSol % ncol > 0:
            nrow += 1

    extent = (0, w, 0, h)

    fig, axs = plt.subplots(nrows=nrow, ncols=ncol)
    fig.suptitle('VLSI SOLUTIONS')

    axs = np.array(axs).flatten()

    axs_len = axs.shape[0]
    for i in range(axs_len):

        if i < num_matrix:
            axs_i = axs[i]
            axs_i.grid(True, color="black")
            axs_i.set_xticks(
                np.array(list(range(0, w+1))))
            axs_i.set_yticks(
                np.array(list(range(0, h+1))))
            M = np.array(AA[i]).reshape((h, w))
            m = M.tolist()
            if 0 in m:
                axs_i.imshow(m, cmap=cmap1, extent=extent)
            else:
                axs_i.imshow(m, cmap=cmap, extent=extent)
            axs_i.plot()
        else:
            fig.delaxes(axs[i])

    plt.show()
