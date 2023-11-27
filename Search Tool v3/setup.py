"""
Setup.py 파일은 구현이 완료되었으며, 더 이상 수정할 것이 없습니다.
There is nothing to edit/modify here!
"""
class Setup:
    def __init__(self):
        self._delta = 0.01     # Step size for axis-parallel mutation
        self._alpha = 0.01     # Update rate for gradient descent
        self._dx = 10 ** (-4)  # Increment for calculating derivative
        
    def getDelta(self):
        return self._delta

    def getAlpha(self):
        return self._alpha

    def getDx(self):
        return self._dx