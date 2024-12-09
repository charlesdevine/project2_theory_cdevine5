from NTMtrace_cdevine5 import NTMSimulator

def analyze_ntm(machine_file, test_strings, max_steps=1000):
    """
    Analyze NTM behavior for given test strings and write results to a file.
    """
    simulator = NTMSimulator(machine_file)
    output_file = "output_resultsfile_cdevine5.txt"
    
    with open(output_file, "w") as f:
        f.write(f"{'='*50}\n")
        f.write(f"NTM Simulator Analysis\n")
        f.write(f"Machine: {simulator.machine_name}\n")
        f.write(f"{'='*50}\n")
        
        for input_str in test_strings:
            f.write(f"\nProcessing input: '{input_str}'\n")
            
            accepted, steps, tree, total_transitions = simulator.simulate(input_str, max_steps)
            
            # Print the configuration tree
            f.write(f"Configuration Tree:\n")
            for depth, level in enumerate(tree):
                f.write(f"Depth {depth}:\n")
                for config in level:
                    f.write(f"{config}\n")
                f.write("\n")
            
            # Calculate nondeterminism
            avg_nondeterminism = calculate_nondeterminism(tree)
            
            # Determine result
            if accepted:
                result = "Accepted"
            elif steps >= max_steps:
                result = "Ran too long"
            else:
                result = "Rejected"
            
            # Write detailed analysis to the file
            f.write(f"Result: {result}\n")
            f.write(f"Depth of configuration tree: {len(tree)}\n")
            f.write(f"Number of configurations explored: {total_transitions}\n")
            f.write(f"Average Nondeterminism: {avg_nondeterminism:.2f}\n")
            
            # Provide a comment based on the result and nondeterminism
            if avg_nondeterminism == 1:
                comment = "Computation is deterministic"
            elif avg_nondeterminism < 2:
                comment = "Slight nondeterministic behavior observed"
            elif avg_nondeterminism < 5:
                comment = "Moderate nondeterministic behavior detected"
            else:
                comment = "Highly nondeterministic computation"
            
            f.write(f"Comment: {comment}\n")
    
    print(f"Results written to {output_file}")

def calculate_nondeterminism(tree):
    """
    Calculate the average nondeterminism across the configuration tree.
    Nondeterminism is defined as the average number of configurations 
    per depth level.
    """
    if not tree:
        return 0

    total_configs = 0
    for level in tree:
        total_configs += len(level)

    return total_configs / len(tree)


# Example usage
test_strings_aplus = ["", "a", "aa", "aaa", "aaaa", "aaaaa", "aaaaaaaa", "aaaaaaaaaaaaa", "ab", "aaab", "b"]
analyze_ntm("data_a_plus_cdevine5.csv", test_strings_aplus)
