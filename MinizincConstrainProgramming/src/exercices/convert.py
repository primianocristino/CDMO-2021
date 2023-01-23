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


if __name__ == "__main__":
    i = 1
    limit = 40

    while i <= limit:

        w = 0
        n = 0
        W = []
        H = []
        reader = open("ins-"+str(i)+".txt")

        with open("ins-"+str(i)+".txt", "r") as reader:
            w = int(reader.readline())
            n = int(reader.readline())
            lines = reader.readlines()

            for row in lines:
                W.append(int(row.split(" ")[0]))
                H.append(int(row.split(" ")[1]))

        W, H = BigAreaSort(W, H)

        with open("../sortedExercices/ins-"+str(i)+".dzn", "w") as writer:
            writer.write("w="+str(w)+";\n")
            writer.write("n="+str(n)+";\n")

            writer.write("W="+str(W)+";\n")
            writer.write("H="+str(H)+";")
        i = i+1
