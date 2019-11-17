# classes for data, at the moment rooms.

class room:
    def __init__(self, name, dataKeys):
        self.name = name
        self.json = {}
        for value in dataKeys:
            self.json[value] = -1
