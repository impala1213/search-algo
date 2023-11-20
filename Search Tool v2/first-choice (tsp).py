from problem import Tsp

LIMIT_STUCK = 100 # Max number of evaluations enduring no improvement


def main():
    # Create an object for TSP
    p = Tsp()        # Create a problem object 
    p.setVariables() # Set its class variables (numCities, locations)
    # Call the search algorithm
    firstChoice(p)
    # Show the problem to be solved
    p.describe()
    displaySetting()
    # Report results  
    p.report()
    
def firstChoice(p):
    ###
    ### Your code goes here!
    ###

def displaySetting():
    print()
    print("Search algorithm: First-Choice Hill Climbing")
    print("Max evaluations with no improvement: {0:,} iterations"
          .format(LIMIT_STUCK))

main()
