import pandas as pd
import sys
import tempfile
import os

# pointRead.py 문자열 저장
pointread_code = IN[0]

temp_dir = tempfile.gettempdir()
pointread_path = os.path.join(temp_dir, "pointRead.py")
with open(pointread_path, "w", encoding="utf-8") as f:
    f.write(pointread_code)

# 저장된 경로 import
if temp_dir not in sys.path:
    sys.path.append(temp_dir)

import importlib
import pointRead
importlib.reload(pointRead)  # 매번 새로 불러오기

# pointRead에서 불러오기
from pointRead import *

# 파일 읽기
csv_path = IN[1]
df = pd.read_csv(csv_path, header=13, encoding='cp949')
filtered_df = df[['측점', 'Northing', 'Easting', '표고']]



rawPoints = PointArray()

for _, row in filtered_df.iterrows():
    rawPoints.add_point(
        LinPoint(
            lin=row['측점'],
            x=row['Easting'],
            y=row['Northing'],
            z=row['표고']
        )
    )

# start = int(input("측점 시작값 입력: "))
# end   = int(input("측점 끝값 입력: "))


for i in rawPoints.points:
    print(f"{rawPoints.points.index(i)+1}번째 포인트:")
    print(i)
    print()

print("---------------------------------------")
print("상대좌표로 변경")
print("---------------------------------------")

# absToRel(newPointList)
print("함수호출")
rawPoints.to_rel()


start = IN[2]
end = IN[3]

rawPoints.points_slide(start,end)

OUT = rawPoints.to_dynamo_points()