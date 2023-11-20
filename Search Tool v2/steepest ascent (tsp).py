from problem import Tsp


def main():
    # Create an object for TSP
    p = Tsp()        # Create a problem object 
    p.setVariables() # Set its class variables (numCities, locations)
    # Call the search algorithm
    steepestAscent(p)
    # Show the problem and algorithm settings
    p.describe()
    displaySetting()
    # Report results
    p.report()
    
def steepestAscent(p):
    ###
    ### Your code goes here!
    ###

def bestOf(neighbors, p):
    ###
    ### Your code goes here!
    ###

def displaySetting():
    print()
    print("Search algorithm: Steepest-Ascent Hill Climbing")

main()
