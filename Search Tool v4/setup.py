
class Setup:
    def __init__(self):
        self._aType = 0   # Type of optimizer
        self._delta = 0   # Step size for axis-parallel mutation
        self._alpha = 0   # Update rate for gradient descent
        self._dx = 0      # Increment for calculating derivative

    def setVariables(self, parameters):
        self._aType = parameters['aType']
        self._delta = parameters['delta']
        self._alpha = parameters['alpha']
        self._dx = parameters['dx']

    def getAType(self):
        return self._aType

    # get_delta(), get_alpha(), get_dx()...
