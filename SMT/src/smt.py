from convert import loadExercice, plotSolutions
import time
from z3 import *
from MyTimer import *
# Main Model


def XY_bound(n, w, h, W, H, X, Y):
    XY_bound = []
    for i in range(n):
        XY_bound.append(And(X[i] >= 0, X[i]+W[i] <= w))
        XY_bound.append(And(Y[i] >= 0, Y[i]+H[i] <= h))

    return XY_bound


def my_no_overlap(n, w, h, W, H, X, Y):
    my_no_overlap = []
    for i in range(n):
        for j in range(n):
            if i != j:
                f = And(
                    Implies(And(X[j] >= X[i], X[j] < X[i]+W[i]),
                            Or(Y[i]+H[i] <= Y[j], Y[j]+H[j] <= Y[i])),
                    Implies(And(Y[j] >= Y[i], Y[j] < Y[i]+H[i]),
                            Or(X[i]+W[i] <= X[j], X[j]+W[j] <= X[i])),
                    Implies(And(X[i] >= X[j], X[i] < X[j]+W[j]),
                            Or(Y[i]+H[i] <= Y[j], Y[j]+H[j] <= Y[i])),
                    Implies(And(Y[i] >= Y[j], Y[i] < Y[j]+H[j]),
                            Or(X[i]+W[i] <= X[j], X[j]+W[j] <= X[i]))
                )

                my_no_overlap.append(f)
    return my_no_overlap
# Implied Constarints


def bound_h(n, w, h, W, H, X, Y):
    bound_h = []
    minArea = sum([W[i]*H[i] for i in range(n)])
    maxAreaW = sum([max(W)*H[i] for i in range(n)])
    maxAreaH = sum([max(H)*W[i] for i in range(n)])

    down_h = int(minArea/w)
    up_h = int(min(maxAreaW, maxAreaH)/w)
    f = And(h >= down_h, h <= up_h)
    bound_h.append(f)
    return bound_h


def impliedH(n, w, h, W, H, X, Y):
    impliedH = []
    for offset_X in range(w):
        f = Sum([If(And(X[rect] <= offset_X, offset_X < X[rect] +
                        W[rect]), H[rect], 0)for rect in range(n)]) <= h

        impliedH.append(f)
    return impliedH


# Simmetry constraints


def orderSameShape(n, w, h, W, H, X, Y):
    orderSameShape = []
    for i in range(n):
        for j in range(n):
            if i < j:
                f = Implies(And(W[i] == W[j], H[i] == H[j]), Or(
                    X[i]+W[i] <= X[j], Y[i]+H[i] <= Y[j]))

                orderSameShape.append(f)
    return orderSameShape


def orderRectMaxLength(n, w, h, W, H, X, Y):
    orderRectMaxLength = []
    for i in range(n):
        for j in range(n):
            if (i < j and W[i] == w):
                f1 = Y[i]+H[i] <= Y[j]

                orderRectMaxLength.append(f1)
            elif (i < j and H[i] == h):
                f2 = X[i]+W[i] <= X[j]

                orderRectMaxLength.append(f2)
    return orderRectMaxLength
# Solver


def solve_satisfy(s, h, X, Y, n, numSol=None, optimize=False):
    s.push()
    sol = 0
    Xs = []
    Ys = []
    h_out = -1
    while (numSol is None or sol < numSol) and s.check() == sat:
        print("============================")
        # print(s.model())
        X_out = []
        Y_out = []
        h_app = int(s.model()[h].as_long())
        if (optimize == True and h_out == -1) or (optimize == True and h_app == h_out):

            if h_out == -1:
                h_out = h_app
            for k in range(n):
                X_out.append(s.model()[X[k]])
                Y_out.append(s.model()[Y[k]])

            Xs.append([int(x.as_long()) for x in X_out])
            Ys.append([int(y.as_long()) for y in Y_out])

            print("h = ", h_out)
            print("X = ", X_out)
            print("Y = ", Y_out)

            XY_constraint = []
            for l in range(n):
                XY_constraint.append(
                    X[l] != s.model()[X[l]])
                XY_constraint.append(
                    Y[l] != s.model()[Y[l]])

            # prevent next model from using the same assignment as a previous model
            s.add(Or(XY_constraint))
            sol += 1
        else:
            break
    s.pop()
    if sol == 0:
        print("unsatisfiable")
    else:
        print("total solution: ", sol)

    return sol, h_out, Xs, Ys


# OBJECTIVE FUNCTION
def initialize():

    # # Input Problem
    w, n, W, H = loadExercice()

    print("n = ", n)
    print("w = ", w)
    print("W = ", W)
    print("H = ", H)
    # Variables
    X = [Int(f"X_{i+1}") for i in range(n)]
    Y = [Int(f"Y_{i+1}") for i in range(n)]
    h = Int("h")

    opt = Optimize()

    opt.add(
        XY_bound(n, w, h, W, H, X, Y) +
        my_no_overlap(n, w, h, W, H, X, Y) +
        bound_h(n, w, h, W, H, X, Y) +
        impliedH(n, w, h, W, H, X, Y) +
        orderSameShape(n, w, h, W, H, X, Y) +
        orderRectMaxLength(n, w, h, W, H, X, Y)
    )

    opt.minimize(h)
    numSol, h_out, Xs, Ys = solve_satisfy(
        opt, h, X, Y, n, numSol=1, optimize=True)

    return n, w, h_out, W, H, Xs, Ys, numSol


if __name__ == "__main__":

    wd = MyTimer(300)
    wd.start()
    start_time = time.time()
    n, w, h_out, W, H, Xs, Ys, numSol = initialize()
    print("Solve Time: ", str((time.time() - start_time)).split(".")
          [0]+"."+str((time.time() - start_time)).split(".")[1][:3])
    wd.stop()

    #plotSolutions(n, w, h_out, W, H, Xs, Ys, numSol, shape=False)
    plotSolutions(n, w, h_out, W, H, Xs, Ys, numSol=numSol, shape=True)
