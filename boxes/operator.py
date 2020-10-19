# system import
import os
import sys
import math

class Point:
    def __init__(self, point):
        self.x = point[0]
        self.y = point[1]

class Edge:
    def __init__(self, edge):
        self.x1 = edge[0][0]
        self.x2 = edge[1][0]
        self.y1 = edge[0][1]
        self.y2 = edge[1][1]

class Rect:
    def __init__(self, box):
        opt = BoxOperator()
        self.box = box
        self.points = opt.box_to_polygon(box)
        self.edges = opt.get_edges(self.points)


class BoxOperator:
    def __init__(self):
        self.zero = 1e-16
        pass

    def is_boxes_overlap(self, box1, box2):
        w1 = abs(box1[0][0] - box1[1][0])
        w2 = abs(box2[0][0] - box2[1][0])
        h1 = abs(box1[0][1] - box1[1][1])
        h2 = abs(box2[0][1] - box2[1][1])
        center_dx = abs((box1[0][0]+box1[1][0])*0.5-(box2[0][0]+box2[1][0])*0.5)
        center_dy = abs((box1[0][1]+box1[1][1])*0.5-(box2[0][1]+box2[1][1])*0.5)
        if center_dx-(w1+w2)*0.5 < self.zero and center_dy-(h1+h2)*0.5 < self.zero:
            return True
        else:
            return False

    def box_to_polygon(self, box):
        x1 = box[0][0]
        x2 = box[1][0]
        y1 = box[0][1]
        y2 = box[1][1]
        polygon = [[x1, y1], [x2, y1], [x2, y2], [x1, y2]]
        return polygon

    def get_edges(self, l_points):
        edges = []
        for i in range(1, len(l_points)):
            edges.append(Edge([l_points[i-1], l_points[i]]))
        edges.append(Edge([l_points[-1], l_points[0]]))
        return edges

    # 判断两条线段是否相交
    def is_edges_intersect(self, edge1: Edge, edge2: Edge):
        # 快速排斥实验
        if max(edge1.x1, edge1.x2) < min(edge2.x1, edge2.x2) or \
            max(edge2.x1, edge2.x2) < min(edge1.x1, edge1.x2) or \
            max(edge1.y1, edge1.y2) < min(edge2.y1, edge2.y2) or \
            max(edge2.y1, edge2.y2) < min(edge1.y1, edge1.y2):
            return False
        # 跨立实验
        # (ca × cd)(cd × cb) 与(bc × ba)(ba × bd)
        cp_ca_x_cd = self.cross_product(Point([edge2.x1, edge2.y1]),
                                        Point([edge1.x1, edge1.y1]),
                                        Point([edge2.x2, edge2.y2]))
        cp_cd_x_cb = self.cross_product(Point([edge2.x1, edge2.y1]),
                                        Point([edge2.x2, edge2.y2]),
                                        Point([edge1.x2, edge1.y2]))
        cp_bc_x_ba = self.cross_product(Point([edge1.x2, edge1.y2]),
                                        Point([edge2.x1, edge2.y1]),
                                        Point([edge1.x1, edge1.y1]))
        cp_ba_x_bd = self.cross_product(Point([edge1.x2, edge1.y2]),
                                        Point([edge1.x1, edge1.y1]),
                                        Point([edge2.x2, edge2.y2]))
        if (cp_ca_x_cd*cp_cd_x_cb > 0 or abs(cp_ca_x_cd*cp_cd_x_cb)<self.zero) and \
                (cp_bc_x_ba*cp_ba_x_bd > 0 or abs(cp_bc_x_ba*cp_ba_x_bd)<self.zero):
            return True
        return False


    def cross_product(self, pt: Point, pt1: Point, pt2: Point):
        return (pt.x-pt1.x)*(pt.y-pt2.y)-(pt.y-pt1.y)*(pt.x-pt2.x)

    def GetCrossPoint(self, edg1, edg2):
        p1 = Point([edg1.x1, edg1.y1])
        p2 = Point([edg1.x2, edg1.y2])
        q1 = Point([edg2.x1, edg2.y1])
        q2 = Point([edg2.x2, edg2.y2])
        tmpLeft = (q2.x-q1.x)*(p1.y-p2.y)-(p2.x-p1.x)*(q1.y-q2.y)
        tmpRight = (p1.y-q1.y)*(p2.x-p1.x)*(q2.x-q1.x)+q1.x*(q2.y-q1.y)*(p2.x-p1.x)-p1.x*(
                p2.y-p1.y)*(q2.x-q1.x)
        x = tmpRight / tmpLeft

        tmpLeft = (p1.x - p2.x) * (q2.y - q1.y) - (p2.y - p1.y) * (q1.x - q2.x)
        tmpRight = p2.y * (p1.x - p2.x) * (q2.y - q1.y) + (q2.x - p2.x) * (q2.y - q1.y) * (p1.y - p2.y) - q2.y * (
                    q1.x - q2.x) * (p2.y - p1.y)
        y = tmpRight / tmpLeft
        print([x,y])

    def is_equal(self, num1: float, num2: float):
        if abs(num1-num2) < self.zero:
            return True
        else:
            return False

if __name__ == '__main__':
    a = Rect([[0, 0], [10, 10]])
    print(a.edges)
    print(a.box)
    print(a.points)
    op = BoxOperator()
    e1 = Edge([[0., 0.], [10., 10.]])
    e2 = Edge([[0, 1], [6, 2]])
    b = op.is_edges_intersect(e1, e2)
    if b:
        op.GetCrossPoint(e1, e2)
