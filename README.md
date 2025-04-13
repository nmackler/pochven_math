# Pochven Math

A simulation tool for calculating the probability of encountering a flashpoint fleet in EVE Online's Pochven region.

## Overview

This project simulates the movement of a flashpoint fleet through the Pochven constellation in EVE Online. The goal is to calculate the probability that a fleet camping in a specific system will encounter the flashpoint fleet as it travels between flashpoints.

The Pochven constellation is modeled as a ring of 24 systems, with 3 active flashpoints at any given time. When a flashpoint is completed, a new one spawns in a random system, and the flashpoint fleet travels to the nearest flashpoint.

## Features

- Simulate flashpoint fleet movements through Pochven
- Calculate the probability of encountering a camping fleet
- Visualize the Pochven constellation, including systems, flashpoints, and paths
- Plot probability curves for different numbers of flashpoints
- Compare simulation results with analytical approximations

## Files

- `system.py`: Defines the System class representing a star system in Pochven
- `pochven.py`: Implements the Pochven class with simulation and visualization methods
- `example.py`: Command-line tool to run simulations and visualize results

## Usage

### Basic Usage

```bash
python example.py --camping-system 12 --n-flashpoints 10 --visualize --plot-curve
```

### Command-line Arguments

- `--camping-system`: System ID to camp in (0-23). If not provided, a random system will be chosen.
- `--flashpoint-systems`: Three system IDs (0-23) where flashpoints start. If not provided, random systems will be chosen.
- `--fleet-starting-system`: System ID where the flashpoint fleet starts (0-23). If not provided, starts at a random flashpoint.
- `--n-flashpoints`: Number of flashpoints to complete in each simulation (default: 10)
- `--n-simulations`: Number of simulations to run (default: 1000)
- `--max-flashpoints`: Maximum number of flashpoints to plot in probability curve (default: 20)
- `--visualize`: Visualize the Pochven constellation
- `--visualize-path`: Visualize a sample path between two systems
- `--plot-curve`: Plot the probability curve

### Example

To calculate the probability of encountering a flashpoint fleet after 15 flashpoints, while camping in system 5:

```bash
python example.py --camping-system 5 --n-flashpoints 15 --n-simulations 2000
```

To specify both the camping system and the fleet's starting system:

```bash
python example.py --camping-system 5 --fleet-starting-system 10 --n-flashpoints 15
```

To visualize the Pochven constellation and plot a probability curve:

```bash
python example.py --visualize --plot-curve
```

## Implementation Details

### Simulation Method

The simulation works as follows:

1. Initialize the Pochven constellation with 24 systems and 3 flashpoints
2. Start the flashpoint fleet at the specified system or at a flashpoint
3. Complete the current flashpoint, which removes it and spawns a new one
4. Find the nearest flashpoint from the current position
5. Calculate the shortest path to the nearest flashpoint
6. Check if this path includes the camping system
7. Move to the nearest flashpoint and repeat steps 3-6 for the desired number of flashpoints
8. Run multiple simulations and calculate the probability of encountering the camping fleet at least once

**Randomization Behavior:**
- If no arguments are provided for any starting positions (camping system, flashpoints, or fleet starting system), all positions are randomized for each simulation run
- If any arguments are provided, those positions remain fixed across all simulation runs
- This ensures maximum variability when no specific starting conditions are specified, while still allowing for deterministic testing with fixed positions

### Analytical Approximation

The analytical approximation is based on the following assumptions:

1. In a ring of 24 systems, the average path length between two random systems is approximately 6
2. The probability that a random path includes the camping system is approximately 6/24 = 1/4

## Visualization

The project includes visualization tools to help understand the Pochven constellation and the paths taken by the flashpoint fleet:

- `visualize_pochven()`: Displays the Pochven constellation as a ring, highlighting the camping system and flashpoints
- `visualize_pochven(show_path=True, start_system=X, end_system=Y)`: Also shows the shortest path between two systems
- `plot_probability_curve()`: Plots the probability of encounter as a function of the number of flashpoints

## Mathematical Background

The probability calculation is based on the concept of "at least once" in multiple trials. If p is the probability of an encounter in a single flashpoint completion, then the probability of at least one encounter in n flashpoint completions is:

P(at least one encounter) = 1 - P(no encounters) = 1 - (1-p)^n

In our simplified analytical model, we estimate p ≈ 1/4, so:

P(at least one encounter) ≈ 1 - (3/4)^n

The simulation provides a more accurate estimate by accounting for the actual topology of Pochven and the distribution of paths over time.
