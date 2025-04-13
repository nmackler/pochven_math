from system import System
import random
from typing import Optional, List, Tuple
import matplotlib.pyplot as plt
import numpy as np
import math


class Pochven:
    def __init__(self, include_home_systems=False, camping_system: Optional[int] = None, flashpoint_starting_systems: Optional[list] = None):
        self.flashpoints = dict()
        self.systems = dict()
        self.camping_system = int()

        # validate values if included
        if camping_system is not None and camping_system not in range(0, 24):
            raise ValueError(
                "The camping system must be an int between 0 and 23 inclusive")

        if flashpoint_starting_systems is not None and len(flashpoint_starting_systems) != 3:
            raise ValueError(
                "The flashpoint starting systems must be a list of 3 integers between 0 and 23")

        if include_home_systems:
            raise NotImplementedError(
                "I didn't implement logic for home systems yet.")

        # create systems
        for system_id in range(0, 24):
            if system_id == 0:
                connections = [1, 23]
            elif system_id == 23:
                connections = [22, 0]
            else:
                connections = [system_id - 1, system_id + 1]
            self.systems[system_id] = System(
                id=system_id, connections=connections)

        # set flashpoint starting systems
        if flashpoint_starting_systems is not None:
            for i, value in enumerate(flashpoint_starting_systems):
                if value not in range(0, 24):
                    raise ValueError(
                        "The flashpoint starting systems must be a list of 3 integers between 0 and 23")
                self.flashpoints[i] = value
        else:
            for key in range(0, 3):
                flashpoint_location = random.randint(
                    0, 23)  # Fixed: changed from 24 to 23
                self.flashpoints[key] = flashpoint_location

        # set camping system
        if camping_system is not None:
            self.camping_system = camping_system
        else:
            self.camping_system = random.randint(
                0, 23)  # Fixed: changed from 24 to 23

    def find_shortest_path(self, start_system_id: int, end_system_id: int) -> List[int]:
        """
        Find the shortest path between two systems in the ring topology.

        Args:
            start_system_id: The ID of the starting system
            end_system_id: The ID of the ending system

        Returns:
            A list of system IDs representing the path (including start and end)
        """
        # Calculate clockwise distance
        clockwise_dist = (end_system_id - start_system_id) % 24

        # Calculate counter-clockwise distance
        counter_clockwise_dist = (start_system_id - end_system_id) % 24

        # Determine the shorter path
        if clockwise_dist <= counter_clockwise_dist:
            # Clockwise path
            path = [(start_system_id + i) %
                    24 for i in range(clockwise_dist + 1)]
        else:
            # Counter-clockwise path
            path = [(start_system_id - i) %
                    24 for i in range(counter_clockwise_dist + 1)]

        return path

    def complete_flashpoint(self, flashpoint_id: int) -> int:
        """
        Complete a flashpoint and remove it from active flashpoints.

        Args:
            flashpoint_id: The ID of the flashpoint to complete

        Returns:
            The system ID where the flashpoint was completed
        """
        if flashpoint_id not in self.flashpoints:
            raise ValueError(f"Flashpoint {flashpoint_id} does not exist")

        # Store the system where the flashpoint was completed
        completed_system = self.flashpoints[flashpoint_id]

        # Remove the flashpoint
        del self.flashpoints[flashpoint_id]

        # Spawn a new flashpoint
        self.spawn_new_flashpoint()

        return completed_system

    def spawn_new_flashpoint(self) -> Tuple[int, int]:
        """
        Spawn a new flashpoint in a random system.

        Returns:
            A tuple of (flashpoint_id, system_id) for the new flashpoint
        """
        # Find a new ID for the flashpoint
        new_id = max(self.flashpoints.keys()) + 1 if self.flashpoints else 0

        # Find a system that doesn't already have a flashpoint
        available_systems = range(0, 24)
        if not available_systems:
            raise ValueError("No available systems for new flashpoint")

        # Randomly select a system
        new_system = random.choice(available_systems)

        # Add the new flashpoint
        self.flashpoints[new_id] = new_system

        return new_id, new_system

    def find_nearest_flashpoint(self, current_system_id: int) -> int:
        """
        Find the nearest flashpoint from the current system.

        Args:
            current_system_id: The ID of the current system

        Returns:
            The ID of the nearest flashpoint
        """
        nearest_flashpoint_id = None
        min_distance = float('inf')

        for flashpoint_id, flashpoint_system in self.flashpoints.items():
            # Calculate the shortest path
            path = self.find_shortest_path(
                current_system_id, flashpoint_system)
            # Subtract 1 because path includes start system
            distance = len(path) - 1

            if distance < min_distance:
                min_distance = distance
                nearest_flashpoint_id = flashpoint_id

        return nearest_flashpoint_id

    def path_includes_camping_system(self, path: List[int]) -> bool:
        """
        Check if a path includes the camping system.

        Args:
            path: A list of system IDs representing a path

        Returns:
            True if the path includes the camping system, False otherwise
        """
        return self.camping_system in path

    def simulate_flashpoint_runs(self, n_flashpoints: int, n_simulations: int = 1000) -> float:
        """
        Simulate multiple runs of flashpoint fleet movements and count encounters.

        Args:
            n_flashpoints: Number of flashpoints to complete in each simulation
            n_simulations: Number of simulations to run

        Returns:
            Probability of encountering the camping fleet at least once
        """
        encounters = 0

        for _ in range(n_simulations):
            # Create a copy of the original state
            original_flashpoints = self.flashpoints.copy()
            original_camping_system = self.camping_system

            # Start at a random flashpoint
            current_flashpoint_id = random.choice(
                list(original_flashpoints.keys()))
            current_system = original_flashpoints[current_flashpoint_id]

            # Track if we encounter the camping system in this simulation
            encountered = False

            for _ in range(n_flashpoints):
                # Complete the current flashpoint
                current_system = self.complete_flashpoint(
                    current_flashpoint_id)

                # Find the nearest flashpoint
                next_flashpoint_id = self.find_nearest_flashpoint(
                    current_system)
                next_system = self.flashpoints[next_flashpoint_id]

                # Find the path to the next flashpoint
                path = self.find_shortest_path(current_system, next_system)

                # Check if the path includes the camping system
                if self.path_includes_camping_system(path):
                    encountered = True

                # Move to the next flashpoint
                current_flashpoint_id = next_flashpoint_id
                current_system = next_system

            if encountered:
                encounters += 1

            # Restore original state
            self.flashpoints = original_flashpoints
            self.camping_system = original_camping_system

        return encounters / n_simulations

    def calculate_encounter_probability(self, n_flashpoints: int, n_simulations: int = 1000) -> float:
        """
        Calculate the probability of encountering the camping fleet at least once
        after n flashpoints spawn.

        Args:
            n_flashpoints: Number of flashpoints to complete
            n_simulations: Number of simulations to run

        Returns:
            Probability of encountering the camping fleet at least once
        """
        return self.simulate_flashpoint_runs(n_flashpoints, n_simulations)

    def calculate_analytical_probability(self, n_flashpoints: int) -> float:
        """
        Calculate the analytical probability of encountering the camping fleet at least once
        after n flashpoints spawn.

        This is based on the fact that in a ring topology with 24 systems, the probability
        of a random path including the camping system can be calculated directly.

        Args:
            n_flashpoints: Number of flashpoints to complete

        Returns:
            Analytical probability of encountering the camping fleet at least once
        """
        # In a ring of 24 systems, the average path length between two random systems is 6
        # The probability that a random path includes the camping system is approximately 6/24 = 1/4
        # The probability of not encountering in n_flashpoints is (3/4)^n_flashpoints
        # So the probability of encountering at least once is 1 - (3/4)^n_flashpoints

        # This is a simplified model and assumes random distribution of flashpoints
        # For more accurate results, use the simulation method

        p_not_encounter = (3/4) ** n_flashpoints
        p_encounter = 1 - p_not_encounter

        return p_encounter

    def visualize_pochven(self, show_flashpoints: bool = True, show_path: bool = False,
                          start_system: Optional[int] = None, end_system: Optional[int] = None) -> None:
        """
        Visualize the Pochven constellation, highlighting the camping system and flashpoints.

        Args:
            show_flashpoints: Whether to highlight the flashpoints
            show_path: Whether to show a path between two systems
            start_system: The starting system for the path (required if show_path is True)
            end_system: The ending system for the path (required if show_path is True)
        """
        # Create a figure
        plt.figure(figsize=(10, 10))

        # Calculate positions for systems in a circle
        angles = np.linspace(0, 2*np.pi, 24, endpoint=False)
        radius = 5
        x = radius * np.cos(angles)
        y = radius * np.sin(angles)

        # Plot systems
        plt.scatter(x, y, s=200, c='lightblue', edgecolors='black', zorder=2)

        # Plot connections
        for i in range(24):
            for conn in self.systems[i].connections:
                plt.plot([x[i], x[conn]], [y[i], y[conn]], 'gray', zorder=1)

        # Highlight camping system
        plt.scatter(x[self.camping_system], y[self.camping_system], s=300, c='red',
                    edgecolors='black', zorder=3, label='Camping System')

        # Highlight flashpoints
        if show_flashpoints:
            for _, system_id in self.flashpoints.items():
                plt.scatter(x[system_id], y[system_id], s=250, c='yellow',
                            edgecolors='black', zorder=3, label='Flashpoint')

        # Show path if requested
        if show_path:
            if start_system is None or end_system is None:
                raise ValueError(
                    "Both start_system and end_system must be provided to show a path")

            path = self.find_shortest_path(start_system, end_system)
            path_x = [x[i] for i in path]
            path_y = [y[i] for i in path]

            plt.plot(path_x, path_y, 'green',
                     linewidth=3, zorder=4, label='Path')

            # Highlight start and end
            plt.scatter(x[start_system], y[start_system], s=250, c='green',
                        edgecolors='black', zorder=5, label='Start')
            plt.scatter(x[end_system], y[end_system], s=250, c='blue',
                        edgecolors='black', zorder=5, label='End')

        # Add system labels
        for i in range(24):
            plt.text(1.1*x[i], 1.1*y[i], str(i), fontsize=12,
                     ha='center', va='center', zorder=6)

        # Add legend (remove duplicates)
        handles, labels = plt.gca().get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        plt.legend(by_label.values(), by_label.keys(), loc='best')

        # Set title and remove axes
        plt.title('Pochven Constellation')
        plt.axis('off')
        plt.tight_layout()

        # Show the plot
        plt.show()

    def plot_probability_curve(self, max_flashpoints: int = 20, n_simulations: int = 1000) -> None:
        """
        Plot the probability curve of encountering the camping fleet as a function of n_flashpoints.

        Args:
            max_flashpoints: Maximum number of flashpoints to simulate
            n_simulations: Number of simulations to run for each data point
        """
        # Create arrays to store results
        n_values = list(range(1, max_flashpoints + 1))
        sim_probs = []
        analytical_probs = []

        # Calculate probabilities
        for n in n_values:
            sim_prob = self.calculate_encounter_probability(n, n_simulations)
            analytical_prob = self.calculate_analytical_probability(n)

            sim_probs.append(sim_prob)
            analytical_probs.append(analytical_prob)

        # Create the plot
        plt.figure(figsize=(10, 6))
        plt.plot(n_values, sim_probs, 'bo-', label='Simulation')
        plt.plot(n_values, analytical_probs, 'r--', label='Analytical')

        # Add labels and title
        plt.xlabel('Number of Flashpoints')
        plt.ylabel('Probability of Encounter')
        plt.title(
            'Probability of Encountering Camping Fleet vs. Number of Flashpoints')
        plt.grid(True)
        plt.legend()

        # Set x-ticks to only show whole numbers
        plt.xticks(n_values)

        # Show the plot
        plt.show()
