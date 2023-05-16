# BO-4 На заданій множині S із N точок на площині побудувати опуклу оболонку і вписати еліпс максимальної площі.
# Алгоритм бінарного пошуку вершин максимального трикутника

import random
import matplotlib.pyplot as plot
from shapely.geometry import Polygon, LineString


class Point:
    def __init__(self, x, y):
        self.X = x
        self.Y = y

    def __str__(self):
        return f"{self.X} {self.Y}"

    def get_x(self):
        return self.X

    def get_y(self):
        return self.Y

    __lt__ = lambda self, other: self.Y < other.Y if (self.X == other.X) else self.X < other.X
    __eq__ = lambda self, other: self.X == other.X and self.Y == other.Y


def enter_points():
    n = int(input("Введіть кількість точок \n"))
    point = [Point(*map(int, input(f"Введіть координати точок по Х та У {x + 1}: \n").split()))
             for x in range(n)]
    return point


def sort_points(point_list):

    def slope(y):
        x = point_list[0]
        try:
            return (x.get_y() - y.get_y()) / (x.get_x() - y.get_x())
        except:
            return 1

    point_list.sort()
    point_list = point_list[:1] + sorted(point_list[1:], key=slope)
    return point_list


def graham_scan(point_list):

    def cross_product_orientation(a, b, c):
        return (b.get_y() - a.get_y()) * (c.get_x() - a.get_x()) - (b.get_x() - a.get_x()) * (c.get_y() - a.get_y())

    convex_hull = []
    sorted_points = sort_points(point_list)
    for p in sorted_points:
        while len(convex_hull) > 1 and cross_product_orientation(convex_hull[-2], convex_hull[-1], p) >= 0:
            convex_hull.pop()
        convex_hull.append(p)
    return convex_hull


def line_intersection(polygon_list, first_point, second_point):
    polygon = Polygon(polygon_list)
    line = LineString([(first_point.X, first_point.Y), (second_point.X, second_point.Y)])
    return line.intersection(polygon)


def find_distance(x1, y1, y2, x3, y3):
    if y1 > y2:
        y1, y2 = y2, y1
    dist = abs(x3 - x1) ** 2
    if y3 > y2:
        dist += (y3 - y2) ** 2
    elif y3 < y1:
        dist += (y3 - y1) ** 2
    return dist ** 0.5


def can_built(first_points, line_point_first_x, line_point_first_y, line_point_second_x, line_point_second_y):
    second_list_for_polygon = first_points
    polygon = Polygon(first_points)
    area = polygon.area
    min1, min2 = 100, 100
    for point in first_points:
        dist = find_distance(line_point_first_x, line_point_first_y, line_point_second_y, point[0],
                             point[1])
        if dist < min1:
            min1 = dist
            point1 = point
        elif min1 < dist < min2:
            min2 = dist
            point2 = point
    second_list_for_polygon.remove([point1[0], point1[1]])
    second_list_for_polygon.remove([point2[0], point2[1]])
    second_list_for_polygon.append([[line_point_first_x, line_point_first_y], [line_point_second_x, line_point_second_y]])
    new_polygon = Polygon(second_list_for_polygon)
    area2 = new_polygon.area
    if area2 > area:
        return second_list_for_polygon
    else:
        return first_points


if __name__ == '__main__':
    points = enter_points()
    convex_shell = graham_scan(points)
    x_values = [x.X for x in convex_shell]
    x_values.append(convex_shell[0].get_x())
    y_values = [y.Y for y in convex_shell]
    y_values.append(convex_shell[0].get_y())
    plot.plot(x_values, y_values)

    if len(convex_shell) > 5:
        new_list = []
        for _ in range(5):
            x = random.choice(convex_shell)
            new_list.append(x)
            convex_shell.remove(x)
        list_for_polygon = [[point.X, point.Y] for point in new_list]
        while len(convex_shell) >= 2:
            intersect = line_intersection(list_for_polygon, convex_shell[0], convex_shell[1])
            if not intersect:
                list_for_polygon = can_built(new_list, convex_shell[0].X, convex_shell[0].Y, convex_shell[1].X, convex_shell[1].Y)
            convex_shell.remove(convex_shell[0])

        plot.scatter([x.X for x in points], [y.Y for y in points], marker='o', s=4, edgecolors='red')
        sorted_list = sort_points([Point(x[0], x[1]) for x in list_for_polygon])
        x_values = [x.X for x in sorted_list]
        x_values.append(sorted_list[0].get_x())
        y_values = [y.Y for y in sorted_list]
        y_values.append(sorted_list[0].get_y())
        plot.plot(x_values, y_values)
        plot.show()
    else:
        print("Не допустима кількість точок")
