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
    def pointsSlide(self, start, end):
        returnList = []
        for i in self.points:
            if i.lin<start:
                continue
            elif start<=i.lin<=end:
                print(i)
                returnList.append(i)
            else:
                continue
        self = returnList
        return self
    # 절대좌표값을 첫번째 인수를 기준으로 상대 좌표롤 만듬 
    def absToRel(self):
        if isinstance(self, PointArray):
            if len(self.points)>0:
                origin = self.points[0]
                for i in self.points:
                    if self.points.index(i) < len(self.points)-1:
                        i.x -= origin.x
                        i.y -= origin.y
                        i.z -= origin.z
                    else: continue
            else:
                print("좌표의 갯수는 1개 이상이어야 합니다.")
        else:
            print("잘못된 입력값, Point Array 객체를 받습니다.")