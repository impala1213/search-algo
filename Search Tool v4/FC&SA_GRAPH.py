import matplotlib.pyplot as plt

# 파일에서 목표 값을 읽어오는 함수
def read_values(file_name):
    with open(file_name, 'r') as file:
        values = [float(line.strip()) for line in file.readlines()]
    return values

# FC 언덕 오르기와 SA 알고리즘의 목표 값들을 읽어옵니다.
fc_values = read_values('setupFile/record_fc.txt')
sa_values = read_values('setupFile/record_sa.txt')

# 각 알고리즘의 반복 횟수에 맞게 x축 리스트를 생성합니다.
fc_iterations = list(range(1, len(fc_values) + 1))
sa_iterations = list(range(1, len(sa_values) + 1))

# 그래프를 그립니다.
plt.figure(figsize=(10, 5)) # 그래프 크기 설정
plt.plot(fc_iterations, fc_values, label='FC Hill Climbing') # FC 언덕 오르기 그래프
plt.plot(sa_iterations, sa_values, label='Simulated Annealing') # SA 그래프

# 그래프 제목과 축 라벨 설정
plt.title('TSP 100 GRAPH')
plt.xlabel('Iteration')
plt.ylabel('objective value')

# 범례 표시
plt.legend()

# 그래프를 화면에 표시
plt.show()
