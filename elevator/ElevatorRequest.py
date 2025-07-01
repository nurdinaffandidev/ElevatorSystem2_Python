

class ElevatorRequest:
    """
        Represents a request made by a passenger to use the elevator.

        Attributes:
            start_floor (int): The floor where the passenger is currently located.
            destination_floor (int): The floor the passenger wants to go to.
            direction (str): Computed property indicating the travel direction
                             ('up', 'down', or 'same floor').

        Example:
            request = ElevatorRequest(3, 7)
            print(request.start_floor)         # 3
            print(request.destination_floor)   # 7
            print(request.direction)           # 'up'
    """

    def __init__(self, start_floor=0, destination_floor=0):
        self._start_floor = start_floor
        self._destination_floor = destination_floor

    @property
    def start_floor(self):
        return self._start_floor

    @start_floor.setter
    def start_floor(self, value):
        self._start_floor = value

    @property
    def destination_floor(self):
        return self._destination_floor

    @destination_floor.setter
    def destination_floor(self, value):
        self._destination_floor = value

    @property
    def direction(self):
        if self.destination_floor > self.start_floor:
            return 'up'
        elif self.destination_floor < self.start_floor:
            return 'down'
        else:
            return 'same floor'

    def __str__(self):
        return f"Request: {self.start_floor} → {self.destination_floor} ({self.direction.upper()})"
