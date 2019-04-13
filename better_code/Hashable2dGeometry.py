# Intersection test taken from https://www.geeksforgeeks.org/check-if-two-given-line-segments-intersect/

def Orientation(p, q, r):
    """
    Finds the orientation of ordered triplet (p,q,r)
    The function returns following values
    0 --> p, q and r are colinear
    1 --> Clockwise
    2 --> Counterclockwise
    """
    val = (q.y - p.y) * (r.x - q.x) - (q.x - p.x) * (r.y - q.y)

    if val == 0: return 0
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

    def __str__(self):
        return "Segment "+str(self.A)+ " -> " + str(self.B)

    def __hash__(self):
        return hash(self.A)^hash(self.B)

    def __eq__(self, other):
        return (self.A == other.A and self.B == other.B) or (self.A == other.B and self.B == other.A)

    def __ne__(self, other):
        return not __eq__(self,other)

    def onSegment(self, p):
        """
        Given a point, p, returns True if p lies in the interior of this segment.
        """
        crossprod = (p.y - self.A.y) * (self.B.x - self.A.x) - (p.x - self.A.x) * (self.B.y - self.A.y)
        if crossprod != 0: return False

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
