from problem import Numeric

LIMIT_STUCK = 100 # Max number of evaluations enduring no improvement


def main():
    # Create a Problme object for numerical optimization
    p = Numeric()    # Create a problem object 
    p.setVariables() # Set its class variables (expression, domain)
    # Call the search algorithm
    firstChoice(p)
    # Show the problem and algorithm settings
    p.describe()
    displaySetting(p)
    # Report results
    p.report()
    
def firstChoice(p):
    current = p.randomInit()   # 'current' is a list of values
    valueC = p.evaluate(current) # 계산결과
    i = 0
    while i < LIMIT_STUCK: 

        successor = p.randomMutant(current) #랜덤한 하나의 변수에 +0.01 or -0.01 
        valueS = p.evaluate(successor) # 변이된 변수 계산결과
        if valueS < valueC: #변이된 변수가 더 나을경우
            current = successor #현재변수 = 변이변수
            valueC = valueS # 현재값 = 변이값
            i = 0              # 스택 리셋
        else:
            i += 1
    p.storeResult(current,valueC) #최선의 결과 저장
    return current, valueC

def displaySetting(p):
    print()
    print("Search algorithm: First-Choice Hill Climbing")
    print()
    print("Mutation step size:", p.getDelta())
    print("Max evaluations with no improvement: {0:,} iterations"
          .format(LIMIT_STUCK))

main()
