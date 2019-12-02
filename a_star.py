import shapefile
import matplotlib.pyplot as plt
from matplotlib.colors import from_levels_and_colors
import numpy as np
import time
import math
from ipywidgets import *
from IPython.display import display


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class A_star:
    class Node:
        def __init__(self, point, endPoint, g):
            self.point = point
            self.endPoint = endPoint
            self.g = g
            self.father = None
            if algo == 1:
                self.h = abs(endPoint.x - point.x) + abs(endPoint.y - point.y)
            elif algo == 2:
                self.h = (endPoint.x - point.x) * (endPoint.x - point.x) + (endPoint.y - point.y) * (
                        endPoint.y - point.y)
            self.f = self.g + self.h

        def search_near(self, ud, rl, g_unit):
            nearPoint = Point(round((self.point.x + rl), 3), round((self.point.y + ud), 3))
            nearNode = A_star.Node(nearPoint, self.endPoint, self.g + g_unit)
            return nearNode

        def search_near_sub(self, ud, rl):
            nearPoint = Point(self.point.x + rl / 2, self.point.y + ud / 2)
            nearsubNode = A_star.Node(nearPoint, self.endPoint, self.g)
            return nearsubNode

    def __init__(self, start_point, end_point, map):
        self.path = []
        self.close_list = []
        self.open_list = []
        self.current = 0
        self.start_point = start_point
        self.end_point = end_point
        self.map = map

    def select_current(self):
        min_value = 1000000
        node_temp = 0
        for ele in self.open_list:
            if ele.f < min_value:
                min_value = ele.f
                node_temp = ele
        self.path.append(node_temp)
        self.open_list.remove(node_temp)
        self.close_list.append(node_temp)
        return node_temp

    def isIn_openList(self, node):
        for opennode_temp in self.open_list:
            if opennode_temp.point.x == node.point.x and opennode_temp.point.y == node.point.y:
                return opennode_temp
        return 0

    def isIn_closelist(self, node):
        for closenode_temp in self.close_list:
            if closenode_temp.point.x == node.point.x and closenode_temp.point.y == node.point.y:
                return 1
        return 0

    def is_obstacle(self, node, mp):

        x = math.ceil((node.point.x - start_point.x) / edge_unit);

        y = math.ceil((node.point.y - start_point.y) / edge_unit);

        if x == 0 or x == xlength - 1:
            return -1
        elif y == 0 or y == ylength - 1:
            return -1
        elif mp[x][y] >= median:
            return 1
        else:
            return 0

    def explore(self, node, node_temp):
        if node_temp.point.x == end_point.x and node_temp.point.y == end_point.y:
            return 1
        elif self.isIn_closelist(node_temp):
            return 0
        elif self.isIn_openList(node_temp) == 0:
            node_temp.father = node
            if (node_temp.point.x > -73.59 and node_temp.point.x < -73.55) and (
                    node_temp.point.y < 45.532 and node_temp.point.y > 45.49):
                self.open_list.append(node_temp)
                return 0
            else:
                return 0
        elif self.isIn_openList(node_temp) != 0:
            if node_temp.f < (self.isIn_openList(node_temp)).f:
                self.open_list.remove(self.isIn_openList(node_temp))
                node_temp.father = node
                self.open_list.append(node_temp)
            return 0

        return 0

    def judge_area(self, node, map):

        sub_node = node.search_near_sub(edge_unit, edge_unit)
        if self.is_obstacle(sub_node, map) == 1:
            right_top = 1
        elif self.is_obstacle(sub_node, map) == -1:
            right_top = -1
        else:
            right_top = 0

        sub_node = node.search_near_sub(edge_unit, -edge_unit)
        if self.is_obstacle(sub_node, map) == 1:
            left_top = 1
        elif self.is_obstacle(sub_node, map) == -1:
            left_top = -1
        else:
            left_top = 0

        sub_node = node.search_near_sub(-edge_unit, edge_unit)
        if self.is_obstacle(sub_node, map) == 1:
            right_bottom = 1
        elif self.is_obstacle(sub_node, map) == -1:
            right_bottom = -1
        else:
            right_bottom = 0

        sub_node = node.search_near_sub(-edge_unit, -edge_unit)
        if self.is_obstacle(sub_node, map) == 1:
            left_bottom = 1
        elif self.is_obstacle(sub_node, map) == -1:
            left_bottom = -1
        else:
            left_bottom = 0
        return left_top, right_top, left_bottom, right_bottom

    def near_explore(self, node):

        left_top, right_top, left_bottom, right_bottom = self.judge_area(node, new_grid)
        output = 0
        # vertical and horizontal
        # direction north
        ud = edge_unit
        rl = 0
        if (left_top == 1 and right_top == 0) or (left_top == 0 and right_top == 1):
            node_temp = node.search_near(ud, rl, 1.3)
            output = self.explore(node, node_temp)
            if output == 1:
                return 1
        elif left_top == 0 and right_top == 0:
            node_temp = node.search_near(ud, rl, 1)
            output = self.explore(node, node_temp)
            if output == 1:
                return 1
        # direction south
        ud = -edge_unit
        rl = 0

        if (left_bottom == 1 and right_bottom == 0) or (left_bottom == 0 and right_bottom == 1):
            node_temp = node.search_near(ud, rl, 1.3)
            output = self.explore(node, node_temp)
            if output == 1:
                return 1
        elif left_bottom == 0 and right_bottom == 0:
            node_temp = node.search_near(ud, rl, 1)
            output = self.explore(node, node_temp)
            if output == 1:
                return 1
        # direction west
        ud = 0
        rl = -edge_unit

        if (left_bottom == 1 and left_top == 0) or (left_bottom == 0 and left_top == 1):
            node_temp = node.search_near(ud, rl, 1.3)
            output = self.explore(node, node_temp)
            if output == 1:
                return 1
        elif left_bottom == 0 and left_top == 0:
            node_temp = node.search_near(ud, rl, 1)
            output = self.explore(node, node_temp)
            if output == 1:
                return 1
        # direction east
        ud = 0
        rl = edge_unit

        if (right_bottom == 1 and right_top == 0) or (right_bottom == 0 and right_top == 1):
            node_temp = node.search_near(ud, rl, 1.3)
            output = self.explore(node, node_temp)
            if output == 1:
                return 1
        elif right_bottom == 0 and right_top == 0:
            node_temp = node.search_near(ud, rl, 1)
            output = self.explore(node, node_temp)
            if output == 1:
                return 1
        # diagonals
        # direction north-east
        ud = edge_unit
        rl = edge_unit

        if right_top == 0:
            node_temp = node.search_near(ud, rl, 1.5)
            output = self.explore(node, node_temp)
            if output == 1:
                return 1
        # direction north-west
        ud = edge_unit
        rl = -edge_unit

        if left_top == 0:
            node_temp = node.search_near(ud, rl, 1.5)
            output = self.explore(node, node_temp)
            if output == 1:
                return 1
        # direction south-west
        ud = -edge_unit
        rl = -edge_unit

        if left_bottom == 0:
            node_temp = node.search_near(ud, rl, 1.5)
            output = self.explore(node, node_temp)
            if output == 1:
                return 1
        # direction south-east
        ud = -edge_unit
        rl = edge_unit

        if right_bottom == 0:
            node_temp = node.search_near(ud, rl, 1.5)
            output = self.explore(node, node_temp)
            if output == 1:
                return 1
        return output


if __name__ == "__main__":
    while True:
        sf = shapefile.Reader("/Users/donald/Downloads/Shape/crime_dt.shp")
        shapes = sf.shapes()
        global threshold
        global edge_unit
        global algo

        edge_unit = float(input('please input edge_unit: '))
        threshold = float(input('please input threshold: '))
        algo = float(input('please input algorithm choose: '
                           ' 1. Manhattan Distance '    ' 2. Euclidean Distance'))
        if algo==1:
            print('Manhattan Distance')
        else:
            print('Euclidean Distance')
        x = np.arange(-73.59, -73.55, edge_unit)
        y = np.arange(45.49, round(45.53 + edge_unit, 3), edge_unit)

        x1 = []
        y1 = []
        for i in range(0, len(shapes)):
            for point in shapes[i].points:
                x1.append(point[0])
                y1.append(point[1])
        x1 = np.array(x1).T
        y1 = np.array(y1).T
        grid, xedges, yedges = np.histogram2d(x1, y1, bins=[x, y])
        print('number of crime for each grid')
        print(grid)

        num = 0.0
        sort_list = []

        for i in range(len(grid)):
            for j in range(len(grid[i])):
                num += grid[i][j]
                sort_list.append(grid[i][j])
        print('overall: ' + str(num))
        np_grid = np.array(grid)
        print('avg: ' + str(np_grid.mean()))
        print('std: ' + str(np_grid.std()))

        sort_list.sort()

        median = sort_list[int(len(sort_list) * threshold)]

        xlength = len(grid) + 2
        ylength = len(grid[0]) + 2
        new_grid = [[0 for i in range(ylength)] for j in range(xlength)]
        for i in range(xlength):
            for j in range(ylength):
                if i == 0 or i == xlength - 1:
                    new_grid[i][j] = -1
                elif j == 0 or j == ylength - 1:
                    new_grid[i][j] = -1
                else:
                    new_grid[i][j] = grid[i - 1][j - 1]

        plt.figure()
        cmap, norm = from_levels_and_colors([0, median, 300], ['darkblue', 'yellow'])
        plt.pcolormesh(x, y, np.swapaxes(grid, 0, 1), cmap=cmap, norm=norm)
        plt.show()

        start_point = Point(-73.59, 45.49)
        end_point = Point(round(-73.55 - edge_unit, 3), 45.53)

        flag = 0
        step = 0
        xlength = len(grid) + 2
        ylength = len(grid[0]) + 2
        new_grid = [[0 for i in range(ylength)] for j in range(xlength)]
        for i in range(xlength):
            for j in range(ylength):
                if i == 0 or i == xlength - 1:
                    new_grid[i][j] = -1
                elif j == 0 or j == ylength - 1:
                    new_grid[i][j] = -1
                else:
                    new_grid[i][j] = grid[i - 1][j - 1]

        start = time.time()
        a_star = A_star(start_point, end_point, new_grid)
        start_node = a_star.Node(start_point, end_point, 0)
        a_star.open_list.append(start_node)

        while flag != 1:
            a_star.current = a_star.select_current()
            flag = a_star.near_explore(a_star.current)
            step = step + 1
            if len(a_star.open_list) == 0:
                print('Due to blocks, no path is found. Please change the map and try again')
                break
            if time.time() - start > 10:
                print('Time is up. The optimal path is not found.')

        end = time.time()
        print('runtime: ' + str(end - start) + ' s')

        node = a_star.close_list[len(a_star.close_list) - 1]
        num = 0
        axi_x = []
        axi_y = []
        plt.figure()
        cmap, norm = from_levels_and_colors([0, median, 300], ['darkblue', 'yellow'])
        plt.pcolormesh(x, y, np.swapaxes(grid, 0, 1), cmap=cmap, norm=norm)
        axi_x.append(end_point.x)
        axi_y.append(end_point.y - edge_unit)
        while flag != 0:

            if node.father != None:
                axi_x.append(node.point.x)
                axi_y.append(node.point.y)
                node = node.father

                num += 1
                if node.father == None:
                    axi_x.append(node.point.x)
                    axi_y.append(node.point.y)
                    break
        plt.plot(axi_x, axi_y, color="r", marker="o", markersize="2", linestyle="-", linewidth=2)
        plt.show()
