# system import
import os
import sys
import math


class Point:
    x = None
    y = None

    def __init__(self, point):
        self.set_point(point)

    def set_point(self, point):
        self.x = point[0]
        self.y = point[1]


class Edge:
    pt1 = None
    pt2 = None

    def __init__(self, pt1: Point, pt2: Point):
        self.set_edge(pt1, pt2)

    def set_edge(self, pt1: Point, pt2: Point):
        self.pt1 = pt1
        self.pt2 = pt2


class Rect:
    bbox = None
    points = None
    edges = None

    def __init__(self, bbox):
        self.set_bbox(bbox)

    def set_bbox(self, bbox):
        self.bbox = [Point(bbox[0]), Point(bbox[1])]
        self.points = self.to_polygon()
        self.edges = self.get_edges()

    def to_polygon(self):
        pt1 = self.bbox[0]
        pt2 = Point([self.bbox[1].x, self.bbox[0].y])
        pt3 = self.bbox[1]
        pt4 = Point([self.bbox[0].x, self.bbox[1].y])
        return [pt1, pt2, pt3, pt4]

    def get_edges(self):
        edges = []
        for i in range(1, len(self.points)):
            edges.append(Edge(self.points[i - 1], self.points[i]))
        edges.append(Edge(self.points[-1], self.points[0]))
        return edges

    def get_width(self):
        return abs(self.bbox[0].x - self.bbox[1].x)

    def get_height(self):
        return abs(self.bbox[0].y - self.bbox[1].y)

    def get_center(self):
        return Point([(self.bbox[0].x + self.bbox[1].x) * 0.5,
                      (self.bbox[0].y + self.bbox[1].y) * 0.5])


class Polygon:
    def __init__(self, points):
        self.points = points


class ShapesOperator:
    zero = 1e-16

    def __init__(self):
        pass

    def is_rects_overlap(self, rect1: Rect, rect2: Rect):
        w1 = rect1.get_width()
        w2 = rect2.get_width()
        h1 = rect1.get_height()
        h2 = rect2.get_height()
        center_dx = abs(rect1.get_center().x - rect2.get_center().x)
        center_dy = abs(rect1.get_center().y - rect2.get_center().y)
        if center_dx - (w1 + w2) * 0.5 < self.zero and center_dy - (h1 + h2) * 0.5 < self.zero:
            return True
        else:
            return False

    # 判断两条线段是否相交
    def is_edges_intersect(self, edge1: Edge, edge2: Edge):
        # 快速排斥实验
        if max(edge1.pt1.x, edge1.pt2.x) < min(edge2.pt1.x, edge2.pt2.x) or \
                max(edge2.pt1.x, edge2.pt2.x) < min(edge1.pt1.x, edge1.pt2.x) or \
                max(edge1.pt1.y, edge1.pt2.y) < min(edge2.pt1.y, edge2.pt2.y) or \
                max(edge2.pt1.y, edge2.pt2.y) < min(edge1.pt1.y, edge1.pt2.y):
            return False
        # 跨立实验
        # (ca × cd)(cd × cb) 与(bc × ba)(ba × bd)
        cp_ca_x_cd = self.cross_product(Point([edge2.pt1.x, edge2.pt1.y]),
                                        Point([edge1.pt1.x, edge1.pt1.y]),
                                        Point([edge2.pt2.x, edge2.pt2.y]))
        cp_cd_x_cb = self.cross_product(Point([edge2.pt1.x, edge2.pt1.y]),
                                        Point([edge2.pt2.x, edge2.pt2.y]),
                                        Point([edge1.pt2.x, edge1.pt2.y]))
        cp_bc_x_ba = self.cross_product(Point([edge1.pt2.x, edge1.pt2.y]),
                                        Point([edge2.pt1.x, edge2.pt1.y]),
                                        Point([edge1.pt1.x, edge1.pt1.y]))
        cp_ba_x_bd = self.cross_product(Point([edge1.pt2.x, edge1.pt2.y]),
                                        Point([edge1.pt1.x, edge1.pt1.y]),
                                        Point([edge2.pt2.x, edge2.pt2.y]))
        if (cp_ca_x_cd * cp_cd_x_cb > 0 or abs(cp_ca_x_cd * cp_cd_x_cb) < self.zero) and \
                (cp_bc_x_ba * cp_ba_x_bd > 0 or abs(cp_bc_x_ba * cp_ba_x_bd) < self.zero):
            return True
        return False

    @staticmethod
    def cross_product(pt: Point, pt1: Point, pt2: Point):
        return (pt.x - pt1.x) * (pt.y - pt2.y) - (pt.y - pt1.y) * (pt.x - pt2.x)

    @staticmethod
    def get_edges_cross_point(edg1, edg2):
        left = (edg2.pt2.x - edg2.pt1.x) * (edg1.pt1.y - edg1.pt2.y) - (edg1.pt2.x - edg1.pt1.x) * (edg2.pt1.y - edg2.pt2.y)
        right = (edg1.pt1.y - edg2.pt1.y) * (edg1.pt2.x - edg1.pt1.x) * (edg2.pt2.x - edg2.pt1.x) + edg2.pt1.x * (edg2.pt2.y - edg2.pt1.y) * (edg1.pt2.x - edg1.pt1.x) - edg1.pt1.x * (
                edg1.pt2.y - edg1.pt1.y) * (edg2.pt2.x - edg2.pt1.x)
        x = right / left

        left = (edg1.pt1.x - edg1.pt2.x) * (edg2.pt2.y - edg2.pt1.y) - (edg1.pt2.y - edg1.pt1.y) * (edg2.pt1.x - edg2.pt2.x)
        right = edg1.pt2.y * (edg1.pt1.x - edg1.pt2.x) * (edg2.pt2.y - edg2.pt1.y) + (edg2.pt2.x - edg1.pt2.x) * (edg2.pt2.y - edg2.pt1.y) * (edg1.pt1.y - edg1.pt2.y) - edg2.pt2.y * (
                edg2.pt1.x - edg2.pt2.x) * (edg1.pt2.y - edg1.pt1.y)
        y = right / left
        return Point([x, y])

    def is_equal(self, num1: float, num2: float):
        if abs(num1 - num2) < self.zero:
            return True
        else:
            return False


if __name__ == '__main__':
    opt = ShapesOperator()
    e1 = Edge(Point([0., 0.]), Point([10., 10.]))
    e2 = Edge(Point([0, 1]), Point([5, 1]))
    b = opt.is_edges_intersect(e1, e2)
    if b:
        pt = opt.get_edges_cross_point(e1, e2)
        print((pt.x, pt.y))
