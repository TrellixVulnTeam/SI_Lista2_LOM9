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


def used_in_row(dimension, matrix, row, num):
    for i in range(dimension):
        if (matrix[row][i] == num):
            return True
    return False


def used_in_col(dimension, matrix, col, num):
    for i in range(dimension):
        if (matrix[i][col] == num):
            return True
    return False


def calculate_visable_buildings(table):
    howMany = 0
    for i in range(table.__len__()):
        isVisable = True
        for j in range(0, i):
            if table[j] > table[i]:
                isVisable = False
        if isVisable:
            howMany += 1
    return howMany


def too_many_empty(table):
    for i in range(table.__len__()):
        if table[i] == 0:
            return True
    return False


def relations_ok(matrix, row, col, num, buildings, dimention):
    up = buildings[0][col]
    up_table = []
    down = buildings[1][col]
    down_table = []
    left = buildings[2][row]
    left_table = []
    right = buildings[3][row]
    right_table = []
    for i in range(dimention):
        if i == row:
            up_table.append(num)
        else:
            up_table.append(matrix[i][col])
        if dimention - 1 - i == row:
            down_table.append(num)
        else:
            down_table.append(matrix[dimention - i - 1][col])
    for i in range(dimention):
        if i == col:
            left_table.append(num)
        else:
            left_table.append(matrix[row][i])
        if dimention - 1 - i == col:
            right_table.append(num)
        else:
            right_table.append(matrix[row][dimention - i - 1])

    if too_many_empty(up_table):
        if not too_many_empty(left_table):
            if (not calculate_visable_buildings(left_table) == left and left != 0):
                return False
            if (not calculate_visable_buildings(right_table) == right and right != 0):
                return False
        return True
    if too_many_empty(left_table):
        if not too_many_empty(up_table):
            if (not calculate_visable_buildings(up_table) == up and up != 0):
                return False
            if (not calculate_visable_buildings(down_table) == down and down != 0):
                return False
        return True

    if (not calculate_visable_buildings(up_table) == up and up != 0):
        return False
    if (not calculate_visable_buildings(down_table) == down and down != 0):
        return False
    if (not calculate_visable_buildings(left_table) == left and left != 0):
        return False
    if (not calculate_visable_buildings(right_table) == right and right != 0):
        return False

    return True


def check_location_is_safe(dimension, matrix, row, col, num, buildings):
    return not used_in_row(dimension, matrix, row, num) \
           and not used_in_col(dimension, matrix, col, num) \
           and relations_ok(matrix, row, col, num, buildings, dimension)


def find_empty_location(dimension, matrix, l):
    for row in range(dimension):
        for col in range(dimension):
            if (matrix[row][col] == 0):
                l[0] = row
                l[1] = col
                return True
    return False


# backtracking
solutions_backtracking = []


def solve_skysprapper_backtracking(dimension, matrix, buildings):
    l = [0, 0]

    # If there is no unassigned location, we are done
    if (not find_empty_location(dimension, matrix, l)):
        solutions_backtracking.append(numpy.copy(matrix))
        return True

    row = l[0]
    col = l[1]

    for num in range(1, dimension + 1):

        if (check_location_is_safe(dimension, matrix, row, col, num, buildings)):

            # make tentative assignment
            matrix[row][col] = num

            # return, if sucess
            if (solve_skysprapper_backtracking(dimension, matrix, buildings)):
                return True

            # failure, unmake & try again
            matrix[row][col] = 0
    return False


def get_remaining_values(dimension, matrix, listOfRelations):
    remaining_values = []
    for i in range(dimension * dimension):
        list = []
        for j in range(1, dimension + 1):
            list.append(j)
        remaining_values.append(list)

    for row in range(len(matrix)):
        for col in range(len(matrix[1])):
            if matrix[row][col] != 0:
                # remove the value from the constrained squares
                value = matrix[row][col]
                remaining_values = remove_values(dimension, row, col, value, remaining_values)

    return remaining_values


def remove_values(dimension, row, col, value, remaining_values):
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

    return remaining_values


solutions_forward_checking = []


# backtracking with forward checking
def solve_skysprapper_forward_checking(dimension, matrix, buildings):
    l = [0, 0]

    # If there is no unassigned location, we are done
    if (not find_empty_location(dimension, matrix, l)):
        solutions_forward_checking.append(numpy.copy(matrix))
        return True

    row = l[0]
    col = l[1]

    remaining_values = get_remaining_values(dimension, matrix, buildings)
    values = list(remaining_values[col + row * dimension])
    for num in values:
        # make tentative assignment
        matrix[row][col] = num

        # return, if sucess
        if (solve_skysprapper_forward_checking(dimension, matrix, buildings)):
            return True

        # failure, unmake & try again
        matrix[row][col] = 0

    # this triggers backtracking
    # print("backtracking2")
    return False
