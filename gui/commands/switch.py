
class Switch:
    def __init__(self, state):
        self.state = state
    def setState(self):
        self.state = not self.state
        print(self.state)
    def getstate(self):
        return self.state