# Intersection test taken from https://www.geeksforgeeks.org/check-if-two-given-line-segments-intersect/
from __future__ import division
def Orientation(p, q, r):
    """
    Finds the orientation of ordered triplet (p,q,r)
    The function returns following values
    0 --> p, q and r are colinear
    1 --> Clockwise
    2 --> Counterclockwise
    """
    val = (q.y - p.y) * (r.x - q.x) - (q.x - p.x) * (r.y - q.y)

    if abs(val) < 0.00001: return 0
    elif val > 0: return 1
    else: return 2

class Point:
    """
    Point class that is hashable with a sensible equality comparison
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "("+str(self.x)+", "+str(self.y)+")"

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self,other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return not self == other

    def __gt__(self, other):
        # points ordered in accending order from top to bottom, then left to right
        return (self.y < other.y) or (self.y == other.y and self.x > other.x)

class Segment:
    """
    Line segment class that is hashable with a sensible equality comparison for use in sets
    Assumes integer coordinates for computation of onSegment
    """
    def __init__(self, A, B):
        # Changed this to have A = upper endpoint, B = lower endpoint always, assuming A!=B
        if A < B:
            self.A = A
            self.B = B
        else:
            self.A = B
            self.B = A
        if (self.A.x - self.B.x) !=0:
            self.slope = (self.A.y-self.B.y)/(self.A.x-self.B.x)
        else:
            self.slope = 1000000000

    def __str__(self):
        return "Segment "+str(self.A)+ " -> " + str(self.B)

    def __hash__(self):
        return hash(self.A)^hash(self.B)

    def __eq__(self, other):
        return (self.A == other.A and self.B == other.B) or (self.A == other.B and self.B == other.A)

    def __ne__(self, other):
        return not __eq__(self,other)

    def __gt__(self, other):
        if other.slope == 0:
            return True
        if (self.slope > 0 and other.slope > 0) or (self.slope < 0 and other.slope < 0):
            return self.slope < other.slope
        if self.slope > 0:
            return True
        return False


    def onSegment(self, p):
        """
        Given a point, p, returns True if p lies in the interior of this segment.
        """
        eps = 0.00001
        det = self.A.x*(self.B.y - p.y) + self.B.x*(p.y - self.A.y) + p.x*(self.A.y - self.B.y)
        if abs(det) > eps:
            return False

        # Otherwise p is collinear with the segment endpoints, so we just check if it's in the right range
        return p.x <= max(self.A.x, self.B.x) and p.x >= min(self.A.x, self.B.x) and p.y <= max(self.A.y, self.B.y) and p.y >= min(self.A.y, self.B.y)

    def intersects(self, other):
        # returns true if interior of segments intersect. Returns false if self == other.

        # if self.A == other.A or self.B == other.B or self.A == other.B or self.B == other.A:
        #     return False

        o1 = Orientation(self.A, self.B, other.A)
        o2 = Orientation(self.A, self.B, other.B)
        o3 = Orientation(other.A, other.B, self.A)
        o4 = Orientation(other.A, other.B, self.B)

        # General case
        if o1 != o2 and o3 != o4:
            return True

        # Special cases
        if o1 == 0 and self.onSegment(other.A):
            return True
        if o2 == 0 and self.onSegment(other.B):
            return True
        if o3 == 0 and other.onSegment(self.A):
            return True
        if o4 == 0 and other.onSegment(self.B):
            return True

        return False

    def intersectionPoint(self, other):
        # Assumes segments are not collinear
        intersects = False
        a1 = self.B.y - self.A.y
        b1 = self.A.x - self.B.x
        c1 = a1*self.A.x + b1* self.A.y

        a2 = other.B.y - other.A.y
        b2 = other.A.x - other.B.x
        c2 = a2*other.A.x + b2* other.A.y

        determinant = a1*b2 - a2*b1

        x = (b2*c1 - b1*c2)/determinant
        y = (a1*c2 - a2*c1)/determinant

        if (x >= min(self.A.x, self.B.x)) and (x <= max(self.A.x, self.B.x)) and (x >= min(other.A.x, other.B.x)) and (x <= max(other.A.x, other.B.x)) and (y >= min(self.A.y, self.B.y)) and (y <= max(self.A.y, self.B.y)) and (y >= min(other.A.y, other.B.y)) and (y <= max(other.A.y, other.B.y)):
            intersects = True

        return intersects, Point(x,y)
