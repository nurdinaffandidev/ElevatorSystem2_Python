import tkinter
from tkinter import ttk
import threading
import time

class ElevatorGUI(tkinter.Tk):
    """
        A Tkinter-based GUI window for visualizing the real-time state of elevators in a simulation.

        This class displays a multi-floor building and animates the elevators' movements over time.
        It periodically polls elevator objects to update their positions on a canvas.

        Attributes:
            elevators (list): List of Elevator objects being simulated.
            num_floors (int): Number of floors in the simulated building.
            canvas (tkinter.Canvas): The canvas on which elevator and floor visuals are drawn.
            elevator_shapes (dict): Maps elevator names to their rectangle and text representations.
    """

    def __init__(self, elevators, num_floors):
        """
            Initialize the GUI window and draw the building structure and elevators.

            Args:
                elevators (list): A list of Elevator objects to visualize.
                num_floors (int): The total number of floors in the building.
        """
        super().__init__()
        self.title("Elevator Simulation")
        self.elevators = elevators
        self.num_floors = num_floors
        self.canvas = tkinter.Canvas(self, width=150 + len(elevators) * 150, height=num_floors * 60 + 60, bg='black')
        self.canvas.pack()
        self.elevator_shapes = {}
        self.draw_floors()
        self.draw_elevators()

        # Start GUI update loop
        self.update_gui()


    def draw_floors(self):
        """
            Draw horizontal floor lines and floor number labels.
            The top floor appears at the top of the canvas.
        """
        for f in range(self.num_floors):
            y = 20 + (self.num_floors - f - 1) * 60
            self.canvas.create_line(20, y, 1000, y, fill="gray")
            self.canvas.create_text(10, y, anchor="w", text=f"Floor {f+1}")


    def draw_elevators(self):
        """
            Draws initial elevator rectangles and labels on the canvas.
            Each elevator is represented by a colored rectangle and a text label.
        """
        for idx, elevator in enumerate(self.elevators):
            x = 100 + idx * 100
            y = 20 + (self.num_floors - elevator.current_floor) * 60
            rect = self.canvas.create_rectangle(x, y, x+60, y+40, fill="blue", tags=f"elevator_{elevator.name}")
            text = self.canvas.create_text(x+30, y+20, text=elevator.name, fill="white", tags=f"text_{elevator.name}")
            self.elevator_shapes[elevator.name] = (rect, text)


    def update_gui(self):
        """
            Periodically updates the GUI to reflect the current floor of each elevator.
            This method is scheduled to run every 500ms using `after()`.
        """
        for elevator in self.elevators:
            x = 20 + int(elevator.name[1:]) * 100
            y = 20 + (self.num_floors - elevator.current_floor) * 60
            rect, text = self.elevator_shapes[elevator.name]
            self.canvas.coords(rect, x, y, x + 60, y + 40)
            self.canvas.coords(text, x + 30, y + 20)
            self.canvas.itemconfig(text, text=elevator.name)
        self.after(500, self.update_gui)  # repeat every 0.5 seconds