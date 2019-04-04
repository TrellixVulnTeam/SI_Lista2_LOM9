import math
import random

import numpy


def get_relations_cords(relationListOfList):
    listOfRelations = []
    for relation in relationListOfList:
        relationCords = []
        for cords in relation:
            row = ord(cords[0]) - 65
            col = int(cords[1]) - 1
            cordsList = [row, col]
            relationCords.append(cordsList)
        listOfRelations.append(relationCords)
    return (listOfRelations)


def used_in_row(dimension, mother, row, num):
    for i in range(dimension):
        if (mother[row][i] == num):
            return True
    return False


def used_in_col(dimension, mother, col, num):
    for i in range(dimension):
        if (mother[i][col] == num):
            return True
    return False


def relations_ok(mother, row, col, num, listOfRelations):
    for relation in listOfRelations:
        if relation[0][0] == row and relation[0][1] == col:
            if num < mother[relation[1][0]][relation[1][1]] or mother[relation[1][0]][relation[1][1]] == 0:
                pass
            else:
                return False

        if relation[1][0] == row and relation[1][1] == col:
            if num > mother[relation[0][0]][relation[0][1]] or mother[relation[0][0]][relation[0][1]] == 0:
                pass
            else:
                return False
    return True


def check_location_is_safe(dimension, mother, row, col, num, listOfRelations):
    return not used_in_row(dimension, mother, row, num) \
           and not used_in_col(dimension, mother, col, num) \
           and relations_ok(mother, row, col, num, listOfRelations)


def find_empty_location(dimension, mother, l):
    for row in range(dimension):
        for col in range(dimension):
            if (mother[row][col] == 0):
                l[0] = row
                l[1] = col
                return True
    return False


def find_empty_location_heurestic(dimension, mother, l, listOfRelations):
    for relation in listOfRelations:
        if mother[relation[0][0]][relation[0][1]] == 0:
            l[0] = relation[0][0]
            l[1] = relation[0][1]
            return True
        if mother[relation[1][0]][relation[1][1]] == 0:
            l[0] = relation[1][0]
            l[1] = relation[1][1]
            return True

    for row in range(dimension):
        for col in range(dimension):
            if (mother[row][col] == 0):
                l[0] = row
                l[1] = col
                return True
    return False

# backtracking
solutions_backtracking = []
def solve_futoshiki_backtracking(dimension, mother, listOfRelations):
    l = [0, 0]

    # If there is no unassigned location, we are done
    if (not find_empty_location(dimension, mother, l)):
        solutions_backtracking.append(numpy.copy(mother))
        return True

    row = l[0]
    col = l[1]

    for num in range(1, dimension + 1):

        if (check_location_is_safe(dimension, mother, row, col, num, listOfRelations)):

            # make tentative assignment
            mother[row][col] = num

            # return, if sucess
            if (solve_futoshiki_backtracking(dimension, mother, listOfRelations)):
                return True

            # failure, unmake & try again
            mother[row][col] = 0

    # this triggers backtracking
    # print("backtracking1")
    return False


# backtracking with heurestic
solutions_backtracking_heurestic = []


def solve_futoshiki_backtracking_heurestic(dimension, mother, listOfRelations):
    l = [0, 0]

    # If there is no unassigned location, we are done
    if (not find_empty_location_heurestic(dimension, mother, l, listOfRelations)):
        solutions_backtracking_heurestic.append(numpy.copy(mother))
        return True

    row = l[0]
    col = l[1]

    for num in range(1, dimension + 1):

        if (check_location_is_safe(dimension, mother, row, col, num, listOfRelations)):

            # make tentative assignment
            mother[row][col] = num

            # return, if sucess
            if (solve_futoshiki_backtracking_heurestic(dimension, mother, listOfRelations)):
                return True

            # failure, unmake & try again
            mother[row][col] = 0

    return False

def get_remaining_values(dimension, mother, listOfRelations):
    remaining_values = []
    for i in range(dimension * dimension):
        list = []
        for j in range(1, dimension + 1):
            list.append(j)
        remaining_values.append(list)

    for row in range(len(mother)):
        for col in range(len(mother[1])):
            if mother[row][col] != 0:
                # remove the value from the constrained squares
                value = mother[row][col]
                remaining_values = remove_values(dimension, mother, listOfRelations, row, col, value, remaining_values)

    return remaining_values

def remove_values(dimension, mother, listOfRelations, row, col, value, remaining_values):
    # use a value of zero to indicate that the square is assigned
    remaining_values[col + row * dimension] = [0]

    # Remove the specified value from each row, column, and block if it's there
    for x in remaining_values[row * dimension:row * dimension + dimension]:
        try:
            x.remove(value)
        except ValueError:
            pass

    for i in range(dimension):
        try:
            remaining_values[col + dimension * i].remove(value)
        except ValueError:
            pass

    for relation in listOfRelations:
        if relation[0][0] == row and relation[0][1] == col:
            if mother[relation[1][0]][relation[1][1]] == 0:
                # only greater numbers are ok
                for i in range(1, dimension + 1):
                    if i <= value:
                        try:
                            remaining_values[relation[1][0] * dimension + relation[1][1]].remove(i)
                        except ValueError:
                            pass

        if relation[1][0] == row and relation[1][1] == col:
            if mother[relation[0][0]][relation[0][1]] == 0:
                # only smaller numbers are ok
                for i in range(1, dimension + 1):
                    if i >= value:
                        try:
                            remaining_values[relation[0][0] * dimension + relation[0][1]].remove(i)
                        except ValueError:
                            pass

    return remaining_values


# checks to see if the value being removed is the only one left
def forward_check(dimension, remaining_values, value, row, col):
    for i in range(dimension):
        if i == col:
            continue

        x = remaining_values[row * dimension + i]

        if len(x) == 1:
            if x[0] == value:
                return 0

    for i in range(dimension):
        if i == row:
            continue

        x = remaining_values[col + dimension * i]
        if len(x) == 1:
            if x[0] == value:
                return 0
    return 1


solutions_backtracking_fch = []
# backtracking with forward checking
def solve_futoshiki_backtracking_fch(dimension, mother, listOfRelations):
    l = [0, 0]

    # If there is no unassigned location, we are done
    if (not find_empty_location(dimension, mother, l)):
        solutions_backtracking_fch.append(numpy.copy(mother))
        return True

    row = l[0]
    col = l[1]

    remaining_values = get_remaining_values(dimension, mother, listOfRelations)
    values = list(remaining_values[col + row * dimension])

    while len(values) != 0:
        value = values[int(math.floor(random.random() * len(values)))]
        values.remove(value)
        if forward_check(dimension, remaining_values, value, row, col):
            mother[row][col] = value
            if solve_futoshiki_backtracking_fch(dimension, mother, listOfRelations):
                return True
            else:
                mother[row][col] = 0

    # this triggers backtracking
    # print("backtracking2")
    return False


solutions_backtracking_fch_heuristic = []


# backtracking with forward checking heuristic
def solve_futoshiki_backtracking_fch_heuristic(dimension, mother, listOfRelations):
    l = [0, 0]

    # If there is no unassigned location, we are done
    if (not find_empty_location_heurestic(dimension, mother, l, listOfRelations)):
        solutions_backtracking_fch_heuristic.append(numpy.copy(mother))
        return True

    row = l[0]
    col = l[1]

    remaining_values = get_remaining_values(dimension, mother, listOfRelations)
    values = list(remaining_values[col + row * dimension])

    while len(values) != 0:
        value = values[int(math.floor(random.random() * len(values)))]
        values.remove(value)
        if forward_check(dimension, remaining_values, value, row, col):
            mother[row][col] = value
            if solve_futoshiki_backtracking_fch_heuristic(dimension, mother, listOfRelations):
                return True
            else:
                mother[row][col] = 0

    # this triggers backtracking
    # print("backtracking2")
    return False