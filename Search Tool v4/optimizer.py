import random
import math
from setup import Setup


class Optimizer(Setup):
    def __init__(self):
        Setup.__init__(self)
        self._pType = 0   # Type of problem
        self._numExp = 0  # Total number of experiments
    def setVariables(self, parameters):
        #Setup.setVariables(self, parameters)
        self._pType = parameters['pType']
        self._numExp = parameters['numExp']

    def getNumExp(self):
        return self._numExp

    def displayNumExp(self):
        print()
        print("Number of experiments:", self._numExp)

    def displaySetting(self):
        if self._pType == 1 and self._aType != 4 and self._aType != 6:
            print("Mutation step size:", self._delta)


class HillClimbing(Optimizer):
    def __init__(self):
        Optimizer.__init__(self)
        self._limitStuck = 0  # Max evaluations allowed for no improvement
        self._numRestart = 0         # Number of restart

    def setVariables(self, parameters):
        Optimizer.setVariables(self, parameters)
        self._limitStuck = parameters['limitStuck']
        self._numRestart = parameters['numRestart']

    def displaySetting(self):
        if self._numRestart > 1:
            print("Number of random restarts:", self._numRestart)
            print()
        Optimizer.displaySetting(self)
        if 2 <= self._aType <= 3:  # First-Choice, Stochastic
            print("Max evaluations with no improvement: {0:,} iterations"
                  .format(self._limitStuck))

    def run(self):
        pass

    def randomRestart(self, p, alg):
        bestSolution = None
        bestMinimum = float('inf')
        for i in range(self._numRestart):
            solution, minimum = alg.run(p)
            if minimum < bestMinimum:
                bestSolution = solution
                bestMinimum = minimum
        p.storeResult(bestSolution, bestMinimum)


class SteepestAscent(HillClimbing):
    def displaySetting(self):
        print()
        print("Search Algorithm: Steepest-Ascent Hill Climbing")
        print()
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
        print()
        HillClimbing.displaySetting(self)

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


class Stochastic(HillClimbing):
    def displaySetting(self):
        print()
        print("Search Algorithm: Stochastic Hill Climbing")
        print()
        HillClimbing.displaySetting(self)

    def run(self, p):
        current = p.randomInit()
        valueC = p.evaluate(current)
        p.storeResult(current, valueC)
        i = 0
        while i < self._limitStuck:
            neighbors = p.mutants(current)  # 현재값 주변의 이웃 생성
            successor, valueS = self.stochasticBest(neighbors, p)  # 주변 이웃중 best 선정
            if valueS >= valueC:  # 주변의 이웃중 더 나은값이 나오지 않을때까지 반복
                i += 1
            else:
                current = successor
                valueC = valueS
                i = 0

        p.storeResult(current, valueC)
        return current, valueC

    def stochasticBest(self, neighbors, p):
        valuesForMin = [p.evaluate(indiv) for indiv in neighbors]
        largeValue = max(valuesForMin) + 1
        valuesForMax = [largeValue - val for val in valuesForMin]
        # Now, larger values are better
        total = sum(valuesForMax)
        randValue = random.uniform(0, total)
        s = valuesForMax[0]
        for i in range(len(valuesForMax)):
            if randValue <= s: # The one with index i is chosen
                break
            else:
                s += valuesForMax[i+1]
        return neighbors[i], valuesForMin[i]


class GradientDescent(HillClimbing):
    def displaySetting(self):
        print()
        print("Search Algorithm: Gradient Descent")
        print()
        HillClimbing.displaySetting(self)
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

        p.storeResult(current, valueC)
        return current, valueC


class MetaHeuristics(Optimizer):
    def __init__(self):
        Optimizer.__init__(self)
        self._limitEval = 0     # Total # evaluations until temination
        self._whenBestFound = 0 # This is actually a result of experiment

    def setVariables(self, parameters):
        Optimizer.setVariables(self, parameters)
        self._limitEval = parameters['limitEval']

    def getWhenBestFound(self):
        return self._whenBestFound

    def displaySetting(self):
        Optimizer.displaySetting(self)
        print("Number of evaluations until termination: {0:,}"
              .format(self._limitEval))

    def run(self):
        pass


class SimulatedAnnealing(MetaHeuristics):
    def __init__(self):
        MetaHeuristics.__init__(self)
        self._numSample = 100  # Number of samples used to determine 
                               #  initial temperature
    def displaySetting(self):
        print()
        print("Search Algorithm: Simulated Annealing")
        print()
        MetaHeuristics.displaySetting(self)
    def run(self, p):
        current = p.randomInit()  # 'current' is a list of values
        valueC = p.evaluate(current)
        best = current[:]
        valueBest = valueC
        t = self.initTemp(p)
        i = 0
        while t > 0 and i < self._limitEval:  # 종료 조건 (온도가 충분히 낮아질 때까지)
            neighbor = p.randomMutant(current)
            valueN = p.evaluate(neighbor)
            deltaE = valueC - valueN
            i += 1
            if deltaE > 0 or random.random() < math.exp(deltaE / t):
                current = neighbor[:]
                valueC = valueN
                if valueC < valueBest:
                    best = current[:]
                    valueBest = valueC
                    self._whenBestFound = i
                    i = 0
            t = self.tSchedule(t)
        p.storeResult(best, valueBest)

    def initTemp(self, p): # To set initial acceptance probability to 0.5
        diffs = []
        for i in range(self._numSample):
            c0 = p.randomInit()     # A random point
            v0 = p.evaluate(c0)     # Its value
            c1 = p.randomMutant(c0) # A mutant
            v1 = p.evaluate(c1)     # Its value
            diffs.append(abs(v1 - v0))
        dE = sum(diffs) / self._numSample  # Average value difference
        t = dE / math.log(2)        # exp(–dE/t) = 0.5
        return t

    def tSchedule(self, t):
        return t * (1 - (1 / 10**4))


