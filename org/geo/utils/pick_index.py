from org.geo.utils import Generator


def pick_zone(row_max, col_max, zone):
    new_row = zone[0]
    new_col = zone[1]
    pick_num = zone[2]
    pick_list = []
    row_min1 = int(pick_num/new_row)*int(row_max/new_row)
    row_max1 = int(row_max/new_row)+row_min1
    col_min1 = ((pick_num % new_row)-1)*int(col_max/new_col)
    col_max1 = int(col_max/new_col)+col_min1
    print(row_min1, row_max1, col_min1, col_max1)
    for row in range(row_min1, row_max1):
        for col in range(col_min1, col_max1):
            pick_index = (row-1)*row_max+col-1
            pick_list.append(pick_index)
    return pick_list


def all_zone(row_max, col_max):
    all_list = []
    for row in range(1, row_max):
        for col in range(1, col_max):
            pick_index = (row-1)*row_max+col-1
            all_list.append(pick_index)
    return all_list




# p = pick_zone(50, 50, [3, 3, 5])
# a = Generator.unique_pick_list(p, 100)
#
# print(p)
# print(a)
