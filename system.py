

class System:
    def __init__(self, id: int, connections: list):
        self._id = id
        self._connections = connections

    @property
    def id(self):
        return self._id

    @id.setter
    def name(self, value: int):
        self._id = value

    @property
    def connections(self):
        return self._connections

    @connections.setter
    def connections(self, value: list):
        self._connections = value
