import threading
import time


class Elevator(threading.Thread):
    def __init__(self, name, starting_floor=1):
        super().__init__()
        self.name = name
        self.current_floor = starting_floor
        self.status = 'idle'
        self.requests = []
        self.target_destination_floors = []  # destination queue
        self.stops = 0
        self.lock = threading.Lock()
        self.reached_request_floor = False


    def assign_request(self, request):
        with self.lock:
            self.requests.append(request)
            self.target_destination_floors.append(request.destination_floor)
        print(f"<{self.name} assigned : [{request}]>")


    def run(self):
        while True:
            if self.status != 'idle':
                print(f"<{self.name} - running elevator: {self.status}>")
            with self.lock:
                if not self.requests:
                    time.sleep(1)
                    continue
                # Get next request (FIFO)
                current_request = self.requests.pop(0)

            # 1. Move to request's start floor (pickup)
            if self.current_floor != current_request.start_floor:
                print(f"--> {self.name} moving to pickup [{current_request}] at floor {current_request.start_floor} | current floor: {self.current_floor}")
                self.status = 'moving to pickup'
                self.move_to_floor(current_request.start_floor)

            # 2. Simulate loading at pickup floor
            print(f"<< {self.name} picked up [{current_request}] at floor {current_request.start_floor} >>")
            self.status = 'loading'
            time.sleep(2)  # Simulate loading
            self.stops += 1

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


    def move_to_floor(self, target_destination_floor):
        print(f"<{self.name}> moving from floor {self.current_floor} to {target_destination_floor}")
        tracked_current_floor = self.current_floor
        total_step = 0
        while self.current_floor != target_destination_floor:
            step = 1 if self.current_floor < target_destination_floor else -1
            self.current_floor += step
            total_step += step
            time.sleep(1)  # Simulate travel
            print(f"---> {self.name} moving to floor {self.current_floor}")
        print(f"<{self.name}> moved from floor {tracked_current_floor} to {target_destination_floor} in {abs(total_step)} steps")


    def unload_requests_at(self, floor):
        self.stops += 1
        with self.lock:
            # store completed request
            completed = [request for request in self.requests if request.destination_floor == floor]
            # update list with uncompleted request
            self.requests = [request for request in self.requests if request.destination_floor != floor]

        for completed_request in completed:
            print(f"<<{self.name} dropped off <{completed_request}> at floor {floor}>>")
        time.sleep(2)  # Hold for 2 seconds during unloading


    def __str__(self):
        return f"Elevator({self.name})"

    def __repr__(self):
        return f"Elevator({self.name}, {self.current_floor}, {self.status}, {self.target_destination_floors}, {self.stops})"
