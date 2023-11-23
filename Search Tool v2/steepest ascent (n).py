from problem import Numeric


def main():
    # Create a Problme object for numerical optimization
    p = Numeric()    # Create a problem object 
    p.setVariables() # Set its class variables (expression, domain)
    # Call the search algorithm
    steepestAscent(p)
    # Show the problem and algorithm settings
    p.describe()
    displaySetting(p)
    # Report results
    p.report()
    
def steepestAscent(p):
    current = p.randomInit() # 'current' is a list of values
    valueC = p.evaluate(current)
    while True:
        neighbors = p.mutants(current) #현재값 주변의 이웃 생성
        successor, valueS = bestOf(neighbors, p) #주변 이웃중 best 선정
        if valueS >= valueC: #주변의 이웃중 더 나은값이 나오지 않을때까지 반복
            break
        else:
            current = successor
            valueC = valueS
    return current, valueC

def bestOf(neighbors, p):
    best = neighbors[0]
    bestValue = p.evaluate(best)
    for neighbor in neighbors[1:]: #neighbor 1부터 끝까지 진행
        tempValue = p.evaluate(neighbor) #neighbor 값 = tempvalue
        if tempValue < bestValue: #tempvalue가 bestvalue 보다 좋을경우 bestvalue = neighbor
            best = neighbor
            bestValue = tempValue
    return best, bestValue

def displaySetting(p):
    print()
    print("Search algorithm: Steepest-Ascent Hill Climbing")
    print()
    print("Mutation step size:", p.getDelta())

main()
