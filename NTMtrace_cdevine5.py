import csv
from typing import List, Tuple, Dict
from collections import defaultdict

# Represents a single transition in a Turing Machine
class Transition:
    def __init__(self, current_state: str, read_char: str, next_state: str, write_char: str, direction: str):
        self.current_state = current_state  # Current state of the machine
        self.read_char = read_char          # Character currently read from the tape
        self.next_state = next_state        # State the machine transitions to
        self.write_char = write_char        # Character to write on the tape
        self.direction = direction          # Movement direction: 'L' (Left) or 'R' (Right)

# Represents the configuration of the machine at any point in time
class Configuration:
    def __init__(self, left_tape: str, state: str, current_char: str, right_tape: str):
        self.left_tape = left_tape         # Tape content to the left of the current position
        self.state = state                 # Current state of the machine
        self.current_char = current_char    # Character currently under the tape head
        self.right_tape = right_tape       # Tape content to the right of the current position

    def __str__(self):
        return f"[{self.left_tape}], ({self.state}), [{self.current_char}{self.right_tape}]"

# Main class to simulate the Turing Machine
class NTMSimulator:
    def __init__(self, machine_file: str):
        self.transitions = defaultdict(list)  # Dictionary to store transitions
        self.start_state = ""                 # The starting state of the machine
        self.accept_state = ""                # State representing acceptance
        self.reject_state = "qrej"           # State representing rejection
        self.load_machine(machine_file)       # Load machine definition from a file

    # Load machine transitions and states from a CSV file
    def load_machine(self, filename: str):
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            
            self.machine_name = next(reader)[0]  # Machine name
            next(reader)  # Skip the states list
            next(reader)  # Skip input alphabet (Sigma)
            next(reader)  # Skip tape alphabet (Gamma)
            
            self.start_state = next(reader)[0]  # Starting state
            self.accept_state = next(reader)[0]  # Accept state
            self.reject_state = next(reader)[0]  # Reject state
            
            # Load transitions into the dictionary
            for row in reader:
                if len(row) != 5:
                    continue  # Ignore invalid rows
                curr_state, read_char, next_state, write_char, direction = row
                self.transitions[(curr_state, read_char)].append(
                    Transition(curr_state, read_char, next_state, write_char, direction)
                )

    # Simulate the Turing Machine on an input string
    def simulate(self, input_str: str, max_steps: int = 1000) -> Tuple[bool, int, List[List[Configuration]], int]:
        # Start with an initial configuration of the machine
        initial_config = Configuration("", self.start_state, input_str[0] if input_str else "_", input_str[1:])
        config_tree = [[initial_config]]  # Store the state tree at each depth level
        total_transitions = 0  # Count the number of transitions executed

        # Run the simulation for up to max_steps
        for depth in range(max_steps):
            current_level = config_tree[-1]
            next_level = []

            # Process each configuration in the current level
            for config in current_level:
                if config.state == self.accept_state:
                    return True, depth, config_tree, total_transitions  # Machine accepted input
                if config.state == self.reject_state:
                    continue  # Skip configurations already in reject state

                # Get applicable transitions for the current state and character
                transitions = self.transitions.get((config.state, config.current_char), [])
                if not transitions:
                    next_level.append(Configuration(config.left_tape, self.reject_state, config.current_char, config.right_tape))
                    continue

                # Apply each transition and create new configurations
                for t in transitions:
                    new_config = self.apply_transition(config, t)
                    next_level.append(new_config)
                    total_transitions += 1

            # If no new configurations are created, terminate the simulation
            if not next_level or all(c.state == self.reject_state for c in next_level):
                return False, depth, config_tree, total_transitions

            config_tree.append(next_level)

        return False, max_steps, config_tree, total_transitions

    # Apply a transition to a given configuration
    def apply_transition(self, config: Configuration, transition: Transition) -> Configuration:
        new_left = config.left_tape
        new_right = config.right_tape
        new_current = transition.write_char

        # Move the tape head according to the transition direction
        if transition.direction == 'L':
            if new_left:
                new_current = new_left[-1]
                new_left = new_left[:-1]
            else:
                new_current = '_'
            new_right = transition.write_char + config.right_tape
        else:
            new_left = config.left_tape + transition.write_char
            if new_right:
                new_current = new_right[0]
                new_right = new_right[1:]
            else:
                new_current = '_'

        return Configuration(new_left, transition.next_state, new_current, new_right)

    # Print all configurations at each depth level of the simulation tree
    def print_all_configurations(self, tree: List[List[Configuration]]):
        for level in tree:
            for config in level:
                print(config)
