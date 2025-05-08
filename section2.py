import pandas as pd
import sys
import tempfile
import os
import math
# pointRead.py 문자열 저장
pointread_code = IN[0]

temp_dir = tempfile.gettempdir()
pointread_path = os.path.join(temp_dir, "pointRead.py")
with open(pointread_path, "w", encoding="utf-8") as f:
    f.write(pointread_code)

# 저장된 경로 import
if temp_dir not in sys.path:
    sys.path.append(temp_dir)


# 매번 새로 불러오기가 가능해야 하지만 노드연결을 연결해제후 재연결해야만함.
import importlib
import pointRead
importlib.reload(pointRead)


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

rawPoints.to_rel()
start = IN[2]
end = IN[3]

linear_point = rawPoints.points_slide(start,end)
OUT = []
rawPoints.toMM()
linear_point = linear_point.to_dynamo_points()

CL = PolyCurve.ByPoints(linear_point)

OUT.append(CL)


# Meter to MilliMeter
for idx in range(len(IN)):
    if 4 <= idx <=7: 
        IN[idx] = IN[idx] * 1000

road_width = IN[4]                      # 차로폭
external_road_width = IN[5]             # 차로 외부 폭
beam_width = IN[6]                      # 보강형 보 폭
walkway_width = IN[7]                   # 인도 폭

number_of_roads = IN[8]                 # 차로 수
superelevation = IN[9]/100              # 편경사 -> %로 변경

crossing_list = IN[4:7]                 # 횡단 정보

# print(crossing_list)

OUT = [CL, crossing_list]

location_of_cross = []
location_of_cross.append(road_width*number_of_roads)
location_of_cross.append(location_of_cross[0] + external_road_width)
location_of_cross.append(location_of_cross[1] + beam_width/2)
location_of_cross.append(location_of_cross[1] + beam_width)
location_of_cross.append(location_of_cross[3] + walkway_width)
print(f"location_of_cross: {location_of_cross}")
for i in range(len(location_of_cross)):
    location_of_cross.append(-1*location_of_cross[i])

align_cross = [location_of_cross[1], location_of_cross[0], location_of_cross[5], location_of_cross[6], location_of_cross[2], location_of_cross[7], location_of_cross[3], location_of_cross[8], location_of_cross[4], location_of_cross[9]]

print(f"align_cross: {align_cross}")
# print(f"location_of_cross: {location_of_cross}")
OUT.append(align_cross)
# Geometry.Translate(CL,align_cross)
CL_cross_vector_x = []
CL_cross_vector_y = []
CL_cross_vector_z = []

# 벡터 x 값: 횡단 값에서 skew를 적용
# 벡터 y 값: 횡단 값에서 그대로 적용
# 벡터 z 값: 차로폭에서 편경사를 적용한 값
for i in align_cross:
    CL_cross_vector_x.append(i * math.tan(math.radians(-10)))
    CL_cross_vector_y.append(i)
    CL_cross_vector_z.append(align_cross[0] * superelevation)

CL_align_vectors = []
count__ = 0
if len(CL_cross_vector_x) == len(CL_cross_vector_y) == len(CL_cross_vector_z):
    for i in range(len(CL_cross_vector_x)):
        CL_align_vectors.append(
            Vector.ByCoordinates(CL_cross_vector_x[i], CL_cross_vector_y[i], CL_cross_vector_z[i])
            )
        print(f"\n {count__}번째 벡터 값\n X:{CL_cross_vector_x[i]}, Y:{CL_cross_vector_y[i]}, Z:{CL_cross_vector_z[i]}")
        count__ = count__ + 1
translated_CL = []
for i in CL_align_vectors:
    translated_CL.append(
        Geometry.Translate(CL,i)
    )

OUT.append(translated_CL)