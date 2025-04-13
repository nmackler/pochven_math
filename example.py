from pochven import Pochven
import matplotlib.pyplot as plt
import numpy as np
import random
import argparse


def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description='Pochven Flashpoint Fleet Encounter Probability Calculator')

    parser.add_argument('--camping-system', type=int, default=None,
                        help='System ID to camp in (0-23). If not provided, a random system will be chosen.')

    parser.add_argument('--flashpoint-systems', type=int, nargs=3, default=None,
                        help='Three system IDs (0-23) where flashpoints start. If not provided, random systems will be chosen.')

    parser.add_argument('--n-flashpoints', type=int, default=10,
                        help='Number of flashpoints to complete in each simulation (default: 10)')

    parser.add_argument('--n-simulations', type=int, default=1000,
                        help='Number of simulations to run (default: 1000)')

    parser.add_argument('--max-flashpoints', type=int, default=20,
                        help='Maximum number of flashpoints to plot in probability curve (default: 20)')

    parser.add_argument('--visualize', action='store_true',
                        help='Visualize the Pochven constellation')

    parser.add_argument('--visualize-path', action='store_true',
                        help='Visualize a sample path between two systems')

    parser.add_argument('--plot-curve', action='store_true',
                        help='Plot the probability curve')

    parser.add_argument('--fleet-starting-system', type=int, default=None,
                        help='System ID where the flashpoint fleet starts (0-23). If not provided, starts at a random flashpoint.')

    args = parser.parse_args()

    # Create a Pochven instance with the specified parameters
    pochven = Pochven(
        camping_system=args.camping_system,
        flashpoint_starting_systems=args.flashpoint_systems,
        fleet_starting_system=args.fleet_starting_system
    )

    # Print initial state
    print("Initial state:")
    print(f"Camping system: {pochven.camping_system}")
    print(f"Flashpoints: {pochven.flashpoints}")
    if pochven.fleet_starting_system is not None:
        print(f"Fleet starting system: {pochven.fleet_starting_system}")

    # Visualize the initial state if requested
    if args.visualize:
        print("\nVisualizing Pochven constellation...")
        pochven.visualize_pochven()

    # Visualize a sample path if requested
    if args.visualize_path:
        # Choose random start and end systems if camping system is not in flashpoints
        flashpoint_systems = list(pochven.flashpoints.values())
        start_system = flashpoint_systems[0]
        end_system = pochven.camping_system

        path = pochven.find_shortest_path(start_system, end_system)
        print(
            f"\nSample path from system {start_system} to system {end_system}: {path}")
        print(
            f"Does this path include the camping system? {pochven.path_includes_camping_system(path)}")

        print("\nVisualizing the path...")
        pochven.visualize_pochven(
            show_path=True, start_system=start_system, end_system=end_system)

    # Calculate probability for the specified number of flashpoints
    sim_prob = pochven.calculate_encounter_probability(
        args.n_flashpoints, args.n_simulations)
    analytical_prob = pochven.calculate_analytical_probability(
        args.n_flashpoints)

    print(
        f"\nProbability of encounter after {args.n_flashpoints} flashpoints (with {args.n_simulations} simulations):")
    print(f"  Simulation probability: {sim_prob:.4f}")
    print(f"  Analytical probability: {analytical_prob:.4f}")

    # Plot the probability curve if requested
    if args.plot_curve:
        print("\nPlotting probability curve...")
        pochven.plot_probability_curve(
            max_flashpoints=args.max_flashpoints, n_simulations=args.n_simulations)


def run_example_simulation():
    """Run a detailed example simulation to demonstrate the functionality."""
    # Create a Pochven instance with a specific camping system and fleet starting system
    pochven = Pochven(camping_system=12, fleet_starting_system=5)

    print("Example simulation:")
    print(f"Camping system: {pochven.camping_system}")
    print(f"Initial flashpoints: {pochven.flashpoints}")
    print(f"Fleet starting system: {pochven.fleet_starting_system}")

    # Find the nearest flashpoint from the fleet starting system
    current_flashpoint_id = pochven.find_nearest_flashpoint(
        pochven.fleet_starting_system)
    current_system = pochven.fleet_starting_system

    # Calculate the path to the nearest flashpoint
    next_system = pochven.flashpoints[current_flashpoint_id]
    path = pochven.find_shortest_path(current_system, next_system)
    print(
        f"\nPath from starting system {current_system} to nearest flashpoint at system {next_system}: {path}")
    print(
        f"Does this path include the camping system? {pochven.path_includes_camping_system(path)}")

    # Move to the nearest flashpoint to begin the simulation
    current_system = next_system

    print(
        f"\nStarting at flashpoint {current_flashpoint_id} in system {current_system}")

    # Run 5 flashpoint completions
    for i in range(5):
        print(f"\nStep {i+1}:")
        print(f"  Current system: {current_system}")
        print(f"  Current flashpoints: {pochven.flashpoints}")

        # Complete the current flashpoint
        print(
            f"  Completing flashpoint {current_flashpoint_id} at system {current_system}...")
        current_system = pochven.complete_flashpoint(current_flashpoint_id)

        # Find the nearest flashpoint
        next_flashpoint_id = pochven.find_nearest_flashpoint(current_system)
        next_system = pochven.flashpoints[next_flashpoint_id]

        print(
            f"  Next nearest flashpoint is {next_flashpoint_id} at system {next_system}")

        # Calculate the path
        path = pochven.find_shortest_path(current_system, next_system)
        print(f"  Path to next flashpoint: {path}")

        # Check if the path includes the camping system
        includes_camping = pochven.path_includes_camping_system(path)
        print(f"  Path includes camping system: {includes_camping}")

        # Move to the next flashpoint
        current_flashpoint_id = next_flashpoint_id
        current_system = next_system


if __name__ == "__main__":
    main()

    # Uncomment to run the example simulation
    # run_example_simulation()
