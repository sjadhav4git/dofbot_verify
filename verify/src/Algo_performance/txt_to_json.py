import json

def txt_to_json(input_file, output_file):
    data_list = []

    with open(input_file, 'r') as txt_file:
        for line in txt_file:
            # Assuming the data is comma-separated
            puzzle, shuffle, multistep, singlestep, time = line.strip().split(';')
            # print(puzzle, shuffle, multistep, singlestep, time)
            # Creating a dictionary for each line
            data = {
                'puzzle_pattern_index': int(puzzle),
                'target_pattern_index': int(shuffle),
                'no. of optimized steps': int(multistep),
                'no. of individual steps': int(singlestep),
                'search_time in sec' :  float(time)
            }
            
            # Appending the dictionary to the list
            data_list.append(data)

    # Writing the list of dictionaries to a JSON file
    with open(output_file, 'a') as json_file:
        json.dump(data_list, json_file, indent=2)

# Example usage
txt_path = '/home/cse4568/verify/dofbot_verify/verify/src/Algo_performance/Anupam_Anaylysis_rubik_race.txt'
json_path = '/home/cse4568/verify/dofbot_verify/verify/src/Algo_performance/Anupam_data.json'
txt_to_json(txt_path, json_path)

'''
    "puzzle_pattern_index": "0",
    "target_pattern_index": "0",
    "no. of iterations": 50,
    "search_time in sec": 0.573,
    "no. of individual steps": 46,
    "no. of optimized steps": 33,
    "individual_steps":
'''