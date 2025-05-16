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

location_of_cross = []
location_of_cross.append(road_width*number_of_roads)
location_of_cross.append(location_of_cross[0] + external_road_width)
location_of_cross.append(location_of_cross[1] + beam_width/2)
location_of_cross.append(location_of_cross[1] + beam_width)
# location_of_cross.append(location_of_cross[3] + walkway_width)
# print(f"location_of_cross: {location_of_cross}")

# align_cross = [location_of_cross[4], location_of_cross[3], location_of_cross[2], location_of_cross[1], location_of_cross[0]] 
align_cross = []

for i in range(len(location_of_cross)):
    align_cross.append(location_of_cross[len(location_of_cross)-i-1])

for i in range(len(location_of_cross)):
    align_cross.append(-1*location_of_cross[i])


print(f"align_cross: {align_cross}")

'''
align_cross = [location_of_cross[1], location_of_cross[0], location_of_cross[5], location_of_cross[6], location_of_cross[2], location_of_cross[7], location_of_cross[3], location_of_cross[8]
            #  , location_of_cross[4], location_of_cross[9]
              ]
'''
# align_cross = [location_of_cross[], location_of_cross[],]

# print(f"align_cross: {align_cross}")
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
if len(CL_cross_vector_x) == len(CL_cross_vector_y) == len(CL_cross_vector_z):
    for i in range(len(CL_cross_vector_x)):
        CL_align_vectors.append(
            Vector.ByCoordinates(CL_cross_vector_x[i], CL_cross_vector_y[i], CL_cross_vector_z[i])
            )
        # print(f"\n {count__}번째 벡터 값\n X:{CL_cross_vector_x[i]}, Y:{CL_cross_vector_y[i]}, Z:{CL_cross_vector_z[i]}")
translated_CL = []
for i in CL_align_vectors:
    translated_CL.append(
        Geometry.Translate(CL,i)
    )

OUT.append(translated_CL)

'''
###################################### 슬래브 작성 ######################################
'''
# 다이나모에서 확인하면 Curve.Length(CL) 이어야하지만 파이선에서는 아래와 같음
CL_length = CL.Length

OUT.append(CL_length)
translated_CL.insert(
    math.floor(len(align_cross)/2) ,CL
    )
# CL이 포함되었으니 더 이상 translated_CL이라고 부르면 안될듯
cross_linear = translated_CL
end_point_of_cross_linear = []

# 라인의 각 끝을 추가한다.
for i in cross_linear:
    end_point_of_cross_linear.append([i.PointAtParameter(0), i.PointAtParameter(1)])

epcl = []
epcl = list(map(list,zip(*end_point_of_cross_linear)))


slab_start = []
slab_end   = []
if len(epcl[0]) == len(epcl[1]):
    for i in range(0, len(epcl[0])):
            slab_start.append(epcl[0][i])
            slab_end.append(  epcl[1][i])
else: print("error, 두점의 개수는 같아야 한다.")

slab_start  = NurbsCurve.ByPoints(slab_start)
slab_end    = NurbsCurve.ByPoints(slab_end)
OUT.append([slab_start,slab_end])


