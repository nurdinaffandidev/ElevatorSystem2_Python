import unittest
from io import StringIO
from unittest.mock import patch, MagicMock
from elevator.Elevator import Elevator
from elevator.ElevatorRequest import ElevatorRequest
from elevator.ElevatorStatus import  ElevatorStatus
from elevator_simulation import (
    get_int_input,
    get_int_request_input,
    remove_same_floor_request,
    get_bool_input,
    find_best_elevator,
    get_summary,
    run_simulation
)


class TestElevatorSimulation(unittest.TestCase):
    # ARRANGE
    @patch('builtins.input', side_effect=['5'])
    def test_valid_get_int_input(self, mock_input):
        # ACT
        result = get_int_input("Enter a number: ", min_val=1)
        # ASSERT
        self.assertEqual(5, result)


    # ARRANGE
    @patch('builtins.input', side_effect=['a', '5'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_invalid_string_get_int_input(self, mock_stdout, mock_input):
        # ACT
        result = get_int_input("Enter a number: ", min_val=1)

        # ASSERT
        # Get printed output (captured from print statements)
        output = mock_stdout.getvalue()
        # Assert error message appears
        self.assertIn("Please enter a valid integer >= 1.", output)
        # assert final value; add a second (valid) input to side_effect so the function exits
        self.assertEqual(5, result)


    # ARRANGE
    @patch('builtins.input', side_effect=['-3', 'abc', '0', '7'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_multiple_get_int_inputs(self, mock_stdout, mock_input):
        # Invalid inputs: -3 (too small), 'abc' (non-int), 0 (too small)
        # Valid input: 7
        # ACT
        result = get_int_input("Enter a number: ", min_val=1)

        # ASSERT
        self.assertEqual(7, result) # Assert final valid result
        # Get printed output (captured from print statements)
        output = mock_stdout.getvalue()
        # Assert error message appears
        self.assertIn("Please enter a valid integer >= 1.", output)
        # Optional: check how many times the error was printed
        error_count = output.count("Please enter a valid integer >= 1.")
        self.assertEqual(error_count, 3)


    # ARRANGE
    @patch('builtins.input', side_effect=['5'])
    def test_valid_get_int_request_input(self, mock_input):
        # ACT
        result = get_int_request_input("Enter a number: ", min_val=1, max_val=10)
        # ASSERT
        self.assertEqual(5, result)


    # ARRANGE
    @patch('builtins.input', side_effect=['a'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_invalid_get_int_request_input_string(self, mock_stdout,mock_input):
        # ACT
        result = get_int_request_input("Enter a number: ", min_val=1, max_val=10, floor_type="Input")
        # ASSERT
        output = mock_stdout.getvalue()
        # Assert error message appears
        self.assertIn("Input floor must be between 1 and 10.", output)


    # ARRANGE
    @patch('builtins.input', side_effect=['0'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_invalid_get_int_request_input_below_min(self, mock_stdout, mock_input):
        # ACT
        result = get_int_request_input("Enter a number: ", min_val=1, max_val=10, floor_type="Input")
        # ASSERT
        output = mock_stdout.getvalue()
        # Assert error message appears
        self.assertIn("Input floor must be between 1 and 10.", output)


    # ARRANGE
    @patch('builtins.input', side_effect=['11'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_invalid_get_int_request_input_above_max(self, mock_stdout, mock_input):
        # ACT
        result = get_int_request_input("Enter a number: ", min_val=1, max_val=10, floor_type="Input")
        # ASSERT
        output = mock_stdout.getvalue()
        # Assert error message appears
        self.assertIn("Input floor must be between 1 and 10.", output)


    def test_remove_same_floor_request(self):
        # ARRANGE
        req_1 = ElevatorRequest(1,2)
        req_2 = ElevatorRequest(2,2)
        req_3 = ElevatorRequest(2,3)
        requests = [ req_1, req_2, req_3 ]

        # ACT
        cleaned_results = remove_same_floor_request(requests)

        # ASSERT
        self.assertEqual(2, len(cleaned_results))
        self.assertTrue(req_2 not in cleaned_results)


    # ARRANGE
    @patch('builtins.input', side_effect=['y'])
    def test_valid_get_bool_input_true(self, mock_input):
        # ACT
        result = get_bool_input("Continue?")

        # ASSERT
        self.assertTrue(result)


    # ARRANGE
    @patch('builtins.input', side_effect=['n'])
    def test_valid_get_bool_input_false(self, mock_input):
        # ACT
        result = get_bool_input("Continue?")

        # ASSERT
        self.assertFalse(result)


    # ARRANGE
    @patch('builtins.input', side_effect=['1', 'ba', 'b', 'yes'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_multiple_get_bool_input(self, mock_stdout, mock_input):
        # Invalid inputs: '1' (number), 'ba' (invalid chars), 'b' (invalid char)
        # Valid input: 'yes'
        # ACT
        result = get_bool_input("Continue?")

        # ASSERT
        self.assertTrue(result)
        # Get printed output (captured from print statements)
        output = mock_stdout.getvalue()
        # Assert error message appears
        self.assertIn("Please enter y/n: ", output)
        # Optional: check how many times the error was printed
        error_count = output.count("Please enter y/n: ")
        self.assertEqual(error_count, 3)


    def test_find_best_elevator_prefers_idle(self):
        # ARRANGE
        e1 = Elevator("E1", starting_floor=1)
        e1.status = ElevatorStatus.IDLE
        e2 = Elevator("E2", starting_floor=5)
        e2.status = ElevatorStatus.MOVING_UP
        e2.requests.append(ElevatorRequest(5, 10))
        request = ElevatorRequest(2, 6)

        # ACT
        result = find_best_elevator(request, [e1, e2])

        # ASSERT
        assert result == e1


    def test_get_summary_output(self):
        mock_elevator = Elevator("E1")
        mock_elevator.total_movement = 10
        mock_elevator.total_time = 30
        mock_elevator.stops = 3

        request = ElevatorRequest(1, 5)

        with patch('sys.stdout', new_callable=StringIO) as mock_out:
            get_summary({"E1": [request]}, [mock_elevator])
            output = mock_out.getvalue()

        assert "E1 :" in output
        assert "SCORE=" in output
        assert "MOVEMENT SUMMARY:" in output


    def test_run_simulation_assigns_and_summarizes(self):
        elevator = Elevator("E1")
        elevator.start = MagicMock()
        elevator.stop = MagicMock()
        elevator.join = MagicMock()
        elevator.status = ElevatorStatus.IDLE
        elevator.requests = []

        request = ElevatorRequest(1, 3)

        with patch("time.sleep"):  # skip actual waiting
            run_simulation([elevator], [request])

        assert len(elevator.requests) == 0  # should be processed
        elevator.start.assert_called_once()
        elevator.stop.assert_called_once()
        elevator.join.assert_called_once()