import threading
import time


class Elevator(threading.Thread):
    """
        A threaded simulation of an elevator system.

        Attributes:
            name (str): The identifier for the elevator.
            current_floor (int): The floor where the elevator currently is.
            status (str): The current state of the elevator (idle, loading, moving, etc.).
            requests (list): A queue of pickup/drop-off requests.
            stops (int): Total number of stops the elevator has made.
            total_movement (int): Total number of floors moved.
            total_time (int): Total simulated time (in seconds) spent operating.
            lock (threading.Lock): Thread-safe access to shared resources.
            _stop_signal (threading.Event): Signal to gracefully stop the thread.
    """
    def __init__(self, name, starting_floor=1):
        """
            Initialize the Elevator object.

            Args:
                name (str): Name or identifier of the elevator.
                starting_floor (int, optional): Initial floor. Defaults to 1.
        """
        super().__init__()
        self.name = name
        self.current_floor = starting_floor
        self.status = 'idle'
        self.requests = []
        self.stops = 0
        self.total_movement = 0
        self.total_time = 0
        self.lock = threading.Lock()
        self.reached_request_floor = False
        self._stop_signal = threading.Event()


    def assign_request(self, request):
        """
            Assign a pickup/drop-off request to this elevator.

            Args:
                request: A request object with `start_floor` and `destination_floor`.
        """
        with self.lock:
            self.requests.append(request)
        print(f"<{self.name} assigned : [{request}]>")


    def stop(self):
        """
            Signals the thread to stop after the current iteration.
        """
        self._stop_signal.set()


    def run(self):
        """
            Main loop of the elevator thread. Processes requests by:
            1. Moving to the pickup floor.
            2. Simulating loading time.
            3. Moving to the destination floor.
            4. Simulating unloading time.
        """
        while not self._stop_signal.is_set():
            if self.status != 'idle':
                print(f"<{self.name} - running elevator: {self.status}>")
            with self.lock:
                if not self.requests:
                    time.sleep(1)
                    self.total_time += 1
                    continue
                # Get next request (FIFO)
                current_request = self.requests.pop(0)

            # 1. Move to request's start floor (pickup)
            if self.current_floor != current_request.start_floor:
                print(f"--> {self.name} moving to pickup [{current_request}] at floor {current_request.start_floor} | current floor: {self.current_floor}")
                self.status = 'moving to pickup'
                self.move_to_floor(current_request.start_floor)
                self.stops += 1 # adding stop here for condition move to request's start floor (pickup)

            # 2. Simulate loading at pickup floor
            print(f"<< {self.name} picked up [{current_request}] at floor {current_request.start_floor} >>")
            self.status = 'loading'
            time.sleep(2)  # Simulate loading

            # 3. Move to destination floor
            print(f"--> {self.name} moving to drop-off [{current_request}] at floor {current_request.destination_floor} | current floor: {self.current_floor}")
            self.status = 'moving to drop-off'
            self.move_to_floor(current_request.destination_floor)

            # 4. Unload at destination
            self.status = 'unloading'
            print(f"<< {self.name} dropped off [{current_request}] at floor {current_request.destination_floor} >>")
            time.sleep(2)  # Simulate unloading
            self.status = 'idle'
            self.stops += 1
            self.total_time += 2


    def move_to_floor(self, target_destination_floor):
        """
            Moves the elevator one floor at a time to the target destination.

            Args:
                target_destination_floor (int): The target floor.
        """
        print(f"<{self.name}> moving from floor {self.current_floor} to {target_destination_floor}")
        tracked_current_floor = self.current_floor
        total_step = 0
        while self.current_floor != target_destination_floor:
            step = 1 if self.current_floor < target_destination_floor else -1
            self.current_floor += step
            total_step += step
            self.total_time += 1  # 1 second per floor
            time.sleep(1)  # Simulate travel
            print(f"---> {self.name} moving to floor {self.current_floor}")

        self.total_movement += abs(total_step)
        print(f"<{self.name}> moved from floor {tracked_current_floor} to {target_destination_floor} in {abs(total_step)} steps")


    def get_efficiency_score(self, weight_movement=1, weight_stop=2, weight_time=0.5):
        """
            Calculates the elevator's efficiency score based on movement, stops, and time.
            Efficiency Formula = 1 / ( weight_movement * self.total_movement +
                               weight_stops * self.stops +
                               weight_time * self.total_time )

            Args:
                weight_movement (float): Weight assigned to total movement.
                weight_stop (float): Weight assigned to total stops.
                weight_time (float): Weight assigned to total time.

            Returns:
                float: Efficiency score (higher is better).
        """
        return 1 / ( weight_movement * self.total_movement +
                     weight_stop * self.stops +
                     weight_time * self.total_time + 1e-5 ) # avoid division by zero


    def __str__(self):
        return f"Elevator({self.name})"

    def __repr__(self):
        return f"Elevator({self.name}, {self.current_floor}, {self.status}, {self.stops})"
