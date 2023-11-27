from setup import Setup


"""
HillClimbing 클래스는 구현이 완료되었으며, 더 이상 수정할 것이 없습니다.
There is nothing to edit/modify for the HillClimbing class!
"""
class HillClimbing(Setup):
    def __init__(self):
        Setup.__init__(self)
        self._pType = 0        # Problem type
        self._limitStuck = 100 # Max evaluations with no improvement

    def setVariables(self, pType):
        self._pType = pType

    def displaySetting(self):
        if self._pType == 1:
            print()
            print("Mutation step size:", self._delta)

    def run(self):
        pass


class SteepestAscent(HillClimbing):
    def displaySetting(self):
        print()
        print("Search Algorithm: Steepest-Ascent Hill Climbing")
        HillClimbing.displaySetting(self)

    def run(self, p):
        current = p.randomInit()  # 'current' is a list of values
        valueC = p.evaluate(current)
        while True:
            neighbors = p.mutants(current)  # 현재값 주변의 이웃 생성
            successor, valueS = self.bestOf(neighbors, p)  # 주변 이웃중 best 선정
            if valueS >= valueC:  # 주변의 이웃중 더 나은값이 나오지 않을때까지 반복
                break
            else:
                current = successor
                valueC = valueS

        p.storeResult(current, valueC)
        return current, valueC

    def bestOf(self, neighbors, p):
        best = neighbors[0]
        bestValue = p.evaluate(best)
        for neighbor in neighbors[1:]:
            tempValue = p.evaluate(neighbor)
            if tempValue < bestValue:
                best = neighbor
                bestValue = tempValue
        return best, bestValue


class FirstChoice(HillClimbing):
    def displaySetting(self):
        print()
        print("Search Algorithm: First-Choice Hill Climbing")
        HillClimbing.displaySetting(self)
        print("Max evaluations with no improvement: {0:,} iterations"
              .format(self._limitStuck))

    def run(self, p):
        current = p.randomInit()  # 'current' is a list of values
        valueC = p.evaluate(current)  # 계산결과
        i = 0
        while i < self._limitStuck:
            successor = p.randomMutant(current)  # 랜덤한 하나의 변수에 +0.01 or -0.01
            valueS = p.evaluate(successor)  # 변이된 변수 계산결과
            if valueS < valueC:  # 변이된 변수가 더 나을경우
                current = successor  # 현재변수 = 변이변수
                valueC = valueS  # 현재값 = 변이값
                i = 0  # 스택 리셋
            else:
                i += 1
        p.storeResult(current, valueC)  # 최선의 결과 저장
        return current, valueC


class GradientDescent(HillClimbing):
    def displaySetting(self):
        print()
        print("Search Algorithm: Gradient Descent")
        print()
        print("Update rate:", self._alpha)
        print("Increment for calculating derivatives:", self._dx)

    def run(self, p):
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
