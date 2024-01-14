#!/usr/bin/env python3

import rospy
import subprocess
import json
import numpy as np
package_path = "/home/cse4568/verify/dofbot_verify/verify"
puzzle_algo_path = package_path+"/src/Algo_performance/puzzle_algo/Puzzle_algo.py"

def read_patterns():
    json_path = package_path+"/src/Algo_performance/patterns.json"
    
    with open(json_path) as json_file:
        data = json.load(json_file)

    puzzles = data["puzzles"]
    targets = data["targets"]
    return puzzles, targets


def write_patterns(puzzle_pattern, target_pattern):
    
    
    data = {
        "puzzle_pattern": puzzle_pattern,
        "target_pattern": target_pattern
        }
    
    # json_data = json.dumps(data, indent=4)  # The indent parameter is optional for pretty formatting
    json_path = package_path+"/src/Algo_performance/current_pattern.json"
    with open(json_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)
        

def main():
    # Read all puzzles and targets
    puzzles, targets = read_patterns()    
    iterations = [50,100,200,500]
    # iterate for each puzzle and target.
    # print('='*80)
    
    for puzzle_index,puzzle in enumerate(puzzles):
        for target_index,target in enumerate(targets):
            print('='*80)
            write_patterns(puzzle,target)
            for i in iterations:
                print()
                print('-'*80)
                print()
                print('puzzle: ',puzzle_index, ', target: ',target_index)
                # print('-'*30)
                
                # Write current_puzzle
                # print("puzzle :\n", np.array(puzzle))
                # print()
                # print("target: \n", np.array(target))
                
                # puzzle_algo_path = puzzle_algo_path+" 50"
                # subprocess.run(['python3',puzzle_algo_path])
                
                command = ['python3', puzzle_algo_path, str(i), str(puzzle_index), str(target_index)]
                result = subprocess.run(command, capture_output=True, text=True)
                print(result.stdout)


def test():
    subprocess.run(['python3',puzzle_algo_path])

# test()
main()