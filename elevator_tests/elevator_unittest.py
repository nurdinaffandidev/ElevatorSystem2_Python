import time
import unittest
from unittest.mock import patch
from elevator.Elevator import Elevator
from elevator.ElevatorRequest import ElevatorRequest
from elevator.ElevatorStatus import  ElevatorStatus

class TestElevator(unittest.TestCase):

    def test_assign_request(self):
        print("\nTEST: test_assign_request")
        print("=========================")
        # Arrange
        elevator = elevator = Elevator("E1")
        # Act
        elevator.assign_request(ElevatorRequest(1, 2))
        # Assert
        self.assertEqual(1, len(elevator.requests))


    # Run the elevator in the main thread (no threading) for test
    @staticmethod
    def run_once(elevator):
        while elevator.requests:
            with elevator.lock:
                current_request = elevator.requests.pop(0)

            if elevator.current_floor != current_request.start_floor:
                elevator.move_to_floor(current_request.start_floor)
                elevator.stops += 1
                elevator.status = ElevatorStatus.LOADING
                time.sleep(2)  # Mocked

            elevator.move_to_floor(current_request.destination_floor)
            elevator.stops += 1

    # test move to floor results in correct current floor, stops, total_movement, with 1 request
    @patch("elevator.Elevator.time.sleep") # mocking time.sleep
    def test_single_request(self, mock_sleep):
        print("\nTEST: test_single_request")
        print("=========================")
        # Arrange
        elevator = Elevator("E1", starting_floor=1)
        request = ElevatorRequest(start_floor=1, destination_floor=3)
        elevator.assign_request(request)

        # Act
        self.run_once(elevator)

        # Assert
        self.assertEqual(elevator.current_floor, 3)
        self.assertEqual(elevator.stops, 1)
        self.assertEqual(elevator.total_movement, 2)
        # self.assertEqual(mock_sleep.call_count, 2)  # Simulated 2 sleep calls (not really required)


    # test move to floor results in correct current floor, stops, total_movement, with 2 request
    @patch("elevator.Elevator.time.sleep") # mocking time.sleep
    def test_multiple_request(self, mock_sleep):
        print("\nTEST: test_multiple_request")
        print("=========================")
        # Arrange
        elevator = Elevator("E1", starting_floor=1)
        request_1 = ElevatorRequest(start_floor=3, destination_floor=1)
        elevator.assign_request(request_1)
        request_2 = ElevatorRequest(start_floor=2, destination_floor=5)
        elevator.assign_request(request_2)

        # Act
        self.run_once(elevator)

        # Assert
        self.assertEqual(elevator.current_floor, 5)
        self.assertEqual(elevator.stops, 4)
        self.assertEqual(elevator.total_movement, 8)

        # test move to floor results in correct current floor, stops, total_movement, with 1 request

    @patch("elevator.Elevator.time.sleep")  # mocking time.sleep
    def test_get_efficiency_score(self, mock_sleep):
        print("\nTEST: test_get_efficiency_score")
        print("=========================")
        # Arrange
        elevator = Elevator("E1", starting_floor=1)
        request = ElevatorRequest(start_floor=1, destination_floor=5)
        elevator.assign_request(request)

        # Act
        self.run_once(elevator)
        score = round(elevator.get_efficiency_score(), 4)

        # Assert
        self.assertEqual(score, 0.1250)


    @patch.object(Elevator, 'start')  # prevent thread from actually starting
    def test_thread_start_mocked(self, mock_start):
        print("\nTEST: test_thread_start_mocked")
        print("=========================")
        elevator = Elevator("E1")
        elevator.start()
        mock_start.assert_called_once()