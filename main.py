import time

import numpy as np

import futoshiki


def loader_fuktoshiki(file_name):
    f = open(file_name, "r")
    contents = f.readlines()
    temp = contents[0].split("\t")
    dimentions = int(temp[temp.__len__() - 1])

    problem = np.arange(dimentions * dimentions).reshape(dimentions, dimentions)
    for i in range(dimentions):
        temp = contents[2 + i].split(";")
        for j in range(dimentions):
            problem[i][j] = temp[j]
    relations = []
    i = 2 + dimentions

    while i < contents.__len__() - 1:
        i += 1
        temp = contents[i].split(";")
        tempek = temp[1].split("\n")
        temp[1] = tempek[0]
        newTemp = []
        newTemp.append(temp[0])
        newTemp.append(temp[1])
        relations.append(newTemp)

    return dimentions, problem, relations


def loader_scycrapper(file_name):
    f = open(file_name, "r")
    contents = f.readlines()
    temp = contents[0].split("\t")
    dimentions = int(temp[temp.__len__() - 1])
    problem = np.arange((dimentions + 2) * (dimentions + 2)).reshape((dimentions + 2), (dimentions + 2))
    for i in range(dimentions + 2):
        up = contents[1 + i].split(";")
        down = contents[2 + i].split(";")
        left = contents[3 + i].split(";")
        right = contents[4 + i].split(";")
        for j in range(dimentions + 1):
            if i == 0 and dimentions + 1 > j > 0:
                problem[i][j] = up[j + 1]
            elif dimentions + 1 > i > 0 and j == 0:
                problem[i][j] = left[i + 1]
            elif i == dimentions and dimentions + 1 > j > 0:
                problem[i][j] = down[j + 1]
            elif 0 < i < dimentions + 1 == j:
                problem[i][j] = right[i + 1]
            else:
                problem[i][j] = 0

    print(problem)


dim, pro, rel = loader_fuktoshiki("data/futoshiki_5_4.txt")
pro2 = np.copy(pro)

start = time.time()
futoshiki.solve_futoshiki_backtracking(dim, pro, futoshiki.get_relations_cords(rel))
print("Solution: " + str(len(futoshiki.solutions_backtracking)))
for solution in futoshiki.solutions_backtracking:
    print(solution)
end = time.time()
print(end - start)

print("-----------------------------------")

start = time.time()
futoshiki.solve_futoshiki_backtracking_fch(dim, pro2, futoshiki.get_relations_cords(rel))
print("Solution: " + str(len(futoshiki.solutions_backtracking_fch)))
for solution in futoshiki.solutions_backtracking_fch:
    print(solution)
end = time.time()
print(end - start)

# loader_scy("data/test_sky_4_0.txt")
