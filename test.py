import pandas as pd
from pointRead import *

        
# 파일 읽기
csv_path = "data/Civil Report.csv"
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

start = int(input("측점 시작값 입력: "))
end   = int(input("측점 끝값 입력: "))




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