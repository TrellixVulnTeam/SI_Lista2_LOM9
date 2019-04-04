import time

import numpy as np

import skycrapper


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
    problem = np.zeros(dimentions * dimentions).reshape((dimentions), (dimentions))
    buildings = []
    buildingsNumpy = np.arange(4 * dimentions).reshape(4, dimentions)
    for i in range(4):
        temp = contents[i + 1].split(";")
        temp[temp.__len__() - 1] = temp[temp.__len__() - 1].split("\n")[0]
        temp.remove(temp[0])
        buildings.append(temp)
    for i in range(4):
        for j in range(dimentions):
            buildingsNumpy[i][j] = buildings[i][j]
    return dimentions, problem, buildingsNumpy


dim, pro1, rel = loader_fuktoshiki("data/test_futo_8_0.txt")
pro2 = np.copy(pro1)
pro3 = np.copy(pro1)
pro4 = np.copy(pro1)

# start = time.time()
# futoshiki.solve_futoshiki_backtracking(dim, pro1, futoshiki.get_relations_cords(rel))
# print("Solution Backtracking: " + str(len(futoshiki.solutions_backtracking)))
# # for solution in futoshiki.solutions_backtracking:
# #     print(solution)
# end = time.time()
# print(end - start)
#
# print("-----------------------------------")
#
# start = time.time()
# futoshiki.solve_futoshiki_backtracking_heurestic(dim, pro3, futoshiki.get_relations_cords(rel))
# print("Solution Backtracking heurestic: " + str(len(futoshiki.solutions_backtracking_heurestic)))
# # for solution in futoshiki.solutions_backtracking_heurestic:
# #     print(solution)
# end = time.time()
# print(end - start)
#
# print("-----------------------------------")
#
# start = time.time()
# futoshiki.solve_futoshiki_backtracking_fch(dim, pro2, futoshiki.get_relations_cords(rel))
# print("Solution Forward checking: " + str(len(futoshiki.solutions_backtracking_fch)))
# # for solution in futoshiki.solutions_backtracking_fch:
# #     print(solution)
# end = time.time()
# print(end - start)
#
# print("-----------------------------------")
#
# start = time.time()
# futoshiki.solve_futoshiki_backtracking_fch_heuristic(dim, pro4, futoshiki.get_relations_cords(rel))
# print("Solution Forward checking heurestic: " + str(len(futoshiki.solutions_backtracking_fch_heuristic)))
# # for solution in futoshiki.solutions_backtracking_fch_heuristic:
# #     print(solution)
# end = time.time()
# print(end - start)


##---------------------SKYCRAPPER
dim, pro, buil = loader_scycrapper("data/test_sky_6_4.txt")
# pro2 = np.copy(pro)
start = time.time()
skycrapper.solve_skysprapper_backtracking(dim, pro, buil)
print("Solution: " + str(len(skycrapper.solutions_backtracking)))
for solution in skycrapper.solutions_backtracking:
    print(solution)
end = time.time()
print(end - start)
