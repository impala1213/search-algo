from problem import Tsp
def main():
    # Create an object for TSP
    p = Tsp()        # Create a problem object 
    p.setVariables() # Set its class variables (numCities, locations)
    p.calcDistanceTable()
    # Call the search algorithm
    steepestAscent(p)
    # Show the problem and algorithm settings
    p.describe()
    displaySetting()
    # Report results
    p.report()
    
def steepestAscent(p):
    current = p.randomInit() # 'current' is a list of city ids
    valueC = p.evaluate(current)
    while True:
        neighbors = p.mutants(current)
        (successor, valueS) = bestOf(neighbors, p)
        if valueS >= valueC:
            break
        else:
            current = successor
            valueC = valueS
    p._solution = current
    p._value = valueC
    return current, valueC

def bestOf(neighbors, p):
    best = neighbors[0]
    bestValue = p.evaluate(best)
    for neighbor in neighbors[1:]:
        tempValue = p.evaluate(neighbor)
        if tempValue < bestValue:
            best = neighbor
            bestValue = tempValue
    return best, bestValue

def displaySetting():
    print()
    print("Search algorithm: Steepest-Ascent Hill Climbing")

main()
