from enum import Enum

class ElevatorStatus(Enum):
    IDLE = 'idle'
    MOVING_UP = 'moving_up'
    MOVING_DOWN = 'moving_down'
    LOADING = 'loading'
    UNLOADING = 'unloading'