import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import Point, PolyCurve

class LinPoint:
    def __init__(self, lin='', x=0, y=0, z=0):
        self.lin = lin  # 측점
        self.x = x      # Easting
        self.y = y      # Northing
        self.z = z      # 표고
        self.isAbsolute = True # 상대 좌표인가?
        self.initialize()

    def initialize(self): # 측점이 string으로 나오기 때문에 변경 필요
        parts = self.lin.split('+')
        result = float(parts[0]+parts[1])
        self.lin = float(result)

    def __repr__(self):
        return f"LinPoint(lin='{self.lin}', x={self.x}, y={self.y}, z={self.z})"

# Point를 담는 클래스
class PointArray:
    def __init__(self):
        self.points = []

    def add_point(self, point):
        if isinstance(point, LinPoint):
            self.points.append(point)
        else:
            raise TypeError("Only LinPoint instances can be added.")
    # 시작점과 끝점을 입력하면 해당 값에서 슬라이스된 array를 출력
    # start에 -1 입력시 처음부터, end = -1 면 끝까지
    def points_slide(self, start, end):
        returnList = []
        if end == -1:
            for i in self.points:
                if start<=i.lin:
                    returnList.append(i)
                else: continue
            return returnList

        for i in self.points:
            if i.lin<start:
                continue
            elif start<=i.lin<=end:
                print(i)
                returnList.append(i)
            else:
                continue
        self.points = returnList
        return self
    # 절대좌표값을 첫번째 인수를 기준으로 상대 좌표롤 만듬 
    def to_rel(self):
        ox = self.points[0].x
        oy = self.points[0].y
        oz = self.points[0].z
        for p in self.points:
            p.x = p.x - ox
            p.y = p.y - oy
            p.z = p.z - oz
    # 다이나모 Point 객체로 변경
    def to_dynamo_points(self):
        return [Point.ByCoordinates(p.x, p.y, p.z) for p in self.points]