import pandas as pd
import sys
import os

# File Path 노드에서 받은 .py 파일 경로
main_script_path = IN[0]
pointRead_dir = os.path.dirname(main_script_path)
sys.path.append(pointRead_dir)


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

start = IN[2]
end = IN[3]


rawPoints.pointsSlide(start,end)

for i in rawPoints.points:
    print(f"{rawPoints.points.index(i)+1}번째 포인트:")
    print(i)
    print()

print("---------------------------------------")
print("상대좌표로 변경")
print("---------------------------------------")

# absToRel(newPointList)
rawPoints.absToRel()
for i in rawPoints.points:
    print(f"{rawPoints.points.index(i)+1}번째 포인트:")
    print(i)
    print()