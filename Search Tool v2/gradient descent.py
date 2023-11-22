from problem import Numeric


def main():
    # Create a Problme object for numerical optimization
    p = Numeric()    # Create a problem object 
    p.setVariables() # Set its class variables (expression, domain)
    # Call the search algorithm
    gradientDescent(p)
    # Show the problem and algorithm settings
    p.describe()
    displaySetting(p)
    # Report results
    p.report()
    
def gradientDescent(p):
    current = p.randomInit()  # 시작점을 무작위로 선택
    valueC = p.evaluate(current)  # 시작점의 함수 값
    while True:  # 무한 루프
        neighbors = p.mutants(current)  # 주변 해들의 리스트
        if len(neighbors) == 0:  # 만약 주변에 해가 없다면 종료
            break

        # 주변 해들 중 가장 좋은 해와 그 값 찾기
        successor, valueS = None, float('inf')
        for neighbor in neighbors:
            value = p.evaluate(neighbor)
            if value < valueS:  # 최소화 문제라고 가정
                valueS = value
                successor = neighbor

        if valueS >= valueC:  # 만약 현재 해가 주변 해들보다 좋다면 종료
            break
        else:  # 아니라면 현재 해를 가장 좋은 주변 해로 바꾸고 계속
            current = successor
            valueC = valueS
    p.storeResult(current, valueC)  # 최적의 해와 그 때의 함수 값을 저장



def displaySetting(p):
    print()
    print("Search algorithm: Gradient Descent")
    print()
    print("Update rate:", p.getAlpha())
    print("Increment for calculating derivative:", p.getDx())

main()
