import time
from elevator.Elevator import Elevator
from elevator.ElevatorRequest import ElevatorRequest


def get_int_input(prompt, min_val=1):
    """
        Prompt the user for an integer input with a minimum value.

        Args:
            prompt (str): The prompt message to display.
            min_val (int): The minimum acceptable integer value (inclusive).

        Returns:
            int: The validated user input as an integer.
    """
    while True:
        try:
            input_value = int(input(prompt))
            if input_value < min_val:
                raise ValueError
            return input_value
        except ValueError:
            print(f"Please enter a valid integer >= {min_val}.")


def get_int_request_input(prompt, min_val=1, max_val=25, floor_type=""):
    """
        Prompt the user for an integer input representing a floor within bounds.

        Args:
            prompt (str): The prompt message to display.
            min_val (int): Minimum valid floor.
            max_val (int): Maximum valid floor.
            floor_type (str): Description of the floor input (e.g., "Starting", "Destination").

        Returns:
            int or None: The validated floor number, or None if invalid.
    """
    try:
        input_value = int(input(prompt))
        if input_value < min_val or input_value > max_val:
            raise ValueError
        else:
            return input_value
    except ValueError:
        print(f"{floor_type} floor must be between {min_val} and {max_val}.")


def get_bool_input(prompt):
    """
        Prompt the user for a yes/no confirmation.

        Args:
            prompt (str): The message to display.

        Returns:
            bool: True if user inputs yes/y, False if no/n.
    """
    while True:
        input_val = input(prompt).strip().lower()
        if input_val in ('yes', 'y'):
            return True
        elif input_val in ('no', 'n'):
            return False
        else:
            print("Please enter y/n: ")


def remove_same_floor_request(elevator_requests):
    """
        Remove requests where the start and destination floors are the same.

        Args:
            elevator_requests (list): List of ElevatorRequest objects.

        Returns:
            list: Filtered list without same-floor requests.
    """
    return [request for request in elevator_requests if request.start_floor != request.destination_floor]


def main():
    """
        Main function to run the elevator simulation.

        - Initializes elevators.
        - Accepts elevator ride requests.
        - Runs the simulation.
    """
    elevators = []
    elevator_requests = []
    num_floors = get_int_input("Please enter the number of floors: ")
    num_elevators = get_int_input("Please enter the number of elevators to be in operation: ")

    for i in range (1,num_elevators + 1):
        elevator = Elevator(f"E{i}", 1)
        elevators.append(elevator)

    while True:
        request = ElevatorRequest()
        current_floor_request = get_int_request_input("Please enter the current floor you are from: ", max_val=num_floors, floor_type="Starting")
        if current_floor_request is None:
            continue
        request.start_floor = current_floor_request

        while request.start_floor != 0 and request.destination_floor == 0:
            destination_floor_request = get_int_request_input("Please enter the destination floor you are going to: ", min_val=1, max_val=num_floors, floor_type="Destination")
            if destination_floor_request is None:
                continue
            request.destination_floor = destination_floor_request

        if request.start_floor != 0 and request.destination_floor != 0:
            elevator_requests.append(request)
            print(f"<< {request} added >>")
        else:
            print(f"<< Invalid request: {request} >>")
            continue

        continue_add_request = get_bool_input("Would you like to add more request? y/n: ")
        if not continue_add_request:
            cleaned_elevator_requests = remove_same_floor_request(elevator_requests)
            print("\nAvailable elevators:")
            print("------------------------")
            for elevator in elevators:
                print(elevator)
            print(end="\n")

            print("Elevator requests: ")
            print("------------------------")
            for request in cleaned_elevator_requests:
                print(request)
            print(end="\n")

            # to run simulation
            run_simulation(elevators, cleaned_elevator_requests)
            break


def run_simulation(elevators, elevator_requests):
    """
        Runs the simulation by assigning requests to elevators and monitoring completion.

        Args:
            elevators (list): List of Elevator objects.
            elevator_requests (list): List of ElevatorRequest objects.
    """
    summary_dict = dict()

    # Start all elevator threads
    for elevator in elevators:
        elevator.start()
        summary_dict[elevator.name] = []

    print("Assigning elevator requests...\n")

    # Assign requests to elevators (simple greedy logic)
    for request in elevator_requests:
        best_elevator = find_best_elevator(request, elevators)
        best_elevator.assign_request(request)
        summary_dict[best_elevator.name].append(request)


    # Wait for all elevators to finish their assigned requests
    all_done = False
    while not all_done:
        time.sleep(1)  # check every second
        all_done = all(len(elevator.requests) == 0 and elevator.status == 'idle' for elevator in elevators)

    # Stop elevators after work is done
    for elevator in elevators:
        elevator.stop()

    for elevator in elevators:
        elevator.join()  # Wait for threads to stop

    get_summary(summary_dict, elevators)


def find_best_elevator(request, elevators):
    """
        Return the best elevator for a given request.
        1. Finds all elevators closest to the request start floor.
        2. Among those, prioritizes idle elevators (e.requests is empty).
        3. Falls back to any one if none are idle.

        Args:
            request (ElevatorRequest): The request to fulfill.
            elevators (list): List of Elevator objects.

        Returns:
            Elevator: The best available elevator.
    """
    # Calculate (elevator, distance)
    distances = [(elevator, abs(elevator.current_floor - request.start_floor)) for elevator in elevators]

    # Find the minimum distance
    min_distance = min(distances, key=lambda x: x[1])[1]

    # Get all elevators at that distance
    closest_elevators = [elevator for elevator, distance in distances if distance == min_distance]

    # Preferred idle ones
    idle_closest = [elevator for elevator in closest_elevators if not elevator.requests]

    # Return best match
    return idle_closest[0] if idle_closest else closest_elevators[0]


def get_summary(summary_dict, elevators):
    """
        Prints a summary of elevator movements and efficiency scores.

        Args:
            summary_dict (dict): Dictionary of elevator names and their handled requests.
            elevators (list): List of Elevator objects.
    """
    print("\nMOVEMENT SUMMARY:")
    print("----------------------")
    for elevator_name, requests in summary_dict.items():
        print(f"{elevator_name} :", end=" [")
        if requests:
            for request in requests:
                if request is requests[-1]:
                    print(request, end="]\n")
                else:
                    print(request, end=", ")
        else:
            print(" ]")

    print("\nELEVATOR EFFICIENCY SCORES:")
    print("--------------------------------")
    for elevator in elevators:
        print(f"| {elevator.name} SCORE= {elevator.get_efficiency_score():.4f} |\n"
              f"| Movement: {elevator.total_movement} floors |\n"
              f"| Stops: {elevator.stops} stops |\n| Time: {elevator.total_time}s |\n")


if __name__ == "__main__":
    main()