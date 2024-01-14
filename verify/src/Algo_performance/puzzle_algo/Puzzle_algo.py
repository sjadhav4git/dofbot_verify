#!/usr/bin/env python

import time
import json
import cv2
from tqdm import tqdm
import numpy as np
import random
import rospy
import sys
import csv

# package_path = "/home/jetson/sanket_ws/src/verify"
# database_path = package_path+"/database/"

package_path = "/home/cse4568/verify/dofbot_verify/verify"
database_path = package_path+"/src/Algo_performance/"




class color_pallet_image_generator:
    def rectangle_locations(self):
        start_points_x = [0,100,200,300,400] 
        start_points_y = [0,100,200,300,400]
        
        end_points_x = [100,200,300,400,500] 
        end_points_y = [100,200,300,400,500]
        
        start_points = []
        end_points = []
        
        for x in start_points_x:
            for y in start_points_y:
                start_points.append([x,y])
                
        for x in end_points_x:
            for y in end_points_y:
                end_points.append([x,y])
        
        return start_points, end_points
    
    
    def generate_image_puzzle_pattern(self,puzzle_pattern,size):
        rect_start_points, rect_end_points = self.rectangle_locations()
        puzzle_pattern = np.transpose(puzzle_pattern)
        puzzle_pattern = [item for sublist in puzzle_pattern for item in sublist]
        
        Black = (0,0,0)
        
        G = (0, 152, 37)
        B = (182, 34, 0)
        R = (30, 30, 200)
        # Y = (1,203,231)
        Y = (0,204,204)
        
        W = (218,220,230)
        # O = (25,126,230)
        O = (0,128,255)
        
        pallet_width,pallet_height = 100,100
        
        canvas_width,canvas_height = int(pallet_width*size), int(pallet_height*size)
        canvas = np.zeros((canvas_height, canvas_width, 3), dtype=np.uint8)
        canvas.fill(0)
        
        for i in range(25):
            color = puzzle_pattern[i]            
            if color == 'R':
                pallet_color = R
            elif color == 'G':
                pallet_color = G
            elif color == 'B':
                pallet_color = B
            elif color == 'Y':
                pallet_color = Y
            elif color == 'W':
                pallet_color = W
            elif color == 'O':
                pallet_color = O
            elif color == '0':
                pallet_color = Black
            
            start_point = (int(rect_start_points[i][0]),int(rect_start_points[i][1]))
            end_point = (int(rect_end_points[i][0]),int(rect_end_points[i][1]))
            
             
            # rect_start_points[i]
            # end_point = rect_end_points[i]

            cv2.rectangle(canvas,start_point,end_point,pallet_color,-1)
            cv2.rectangle(canvas,start_point,end_point,Black,5)
        return canvas  
    
    

class algorithm:
    
    def find_color_at_location(self,location, puzzle_pattern):
        row_num = location[1]
        column_num = location[0]
        return(puzzle_pattern[row_num][column_num])
    
    
    def find_location_of_color(self, puzzle_pattern,target_color):
        match_color_location = []
        for x in range(5):
            for y in range(5):
                location = [x,y]
                puzzle_color = self.find_color_at_location(location, puzzle_pattern)
                if puzzle_color == target_color:
                    match_color_location.append(location)
        return match_color_location
    
    
    def find_blank_space(self, puzzle_pattern):
        row_index = 0
        column_index = 0 
        for row_index in range(5):
            for column_index in range(5):
                element = puzzle_pattern[row_index][column_index]
                if element == '0':
                    # return [row_index,column_index]
                    x = column_index
                    y = row_index
                    return[x, y]
    
    
    def A_star(self, start_point, goal_point, lock_positions):
        # create_grid
        def grid_creator(lock_positions):
            grid = []
            for y in range(5):
                row = []
                for x in range(5):
                    if [x, y] not in lock_positions:
                        row.append(0)
                    else:
                        row.append(1)
                grid.append(row)
            return grid

        grid = grid_creator(lock_positions)
        start = (start_point[1], start_point[0])
        goal = (goal_point[1], goal_point[0])

        # Define the possible movements (up, down, left, right)
        movements = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        # Create a dictionary to store the cost of each position
        costs = {}
        for row in range(len(grid)):
            for col in range(len(grid[row])):
                costs[(row, col)] = float('inf')

        # Create a list to store the open set
        open_set = [(0, start)]  # Start position with cost 0

        # Create a dictionary to store the parent of each position
        parents = {}
        parents[start] = None

        # Create a function to calculate the heuristic (Manhattan distance)
        def heuristic(a, b):
            return abs(b[0] - a[0]) + abs(b[1] - a[1])

        # A* algorithm
        while open_set:
            open_set.sort(key=lambda x: x[0])  # Sort the open set based on total cost
            current_cost, current = open_set.pop(0)

            if current == goal:
                break

            for movement in movements:
                dx, dy = movement
                next_position = (current[0] + dx, current[1] + dy)

                if (
                    0 <= next_position[0] < len(grid)
                    and 0 <= next_position[1] < len(grid[0])
                ):
                    if grid[next_position[0]][next_position[1]] == 1:
                        continue

                    new_cost = current_cost + 1

                    if new_cost < costs[next_position]:
                        costs[next_position] = new_cost
                        total_cost = new_cost + heuristic(next_position, goal)
                        open_set.append((total_cost, next_position))
                        parents[next_position] = current

        # Retrieve the path by backtracking from the goal to the start
        path = []
        current = goal
        while current != start:
            path.append(current)
            current = parents[current]
        path.append(start)
        path.reverse()

        # Convert into [x, y] array
        def convert(path):
            Path = []
            for loc in path:
                x = loc[1]
                y = loc[0]
                Path.append([x, y])
            return Path

        path = convert(path)

        return path
      
    
    def tile_move_A_star_path_list(self,available_color_locations,target_color_location,lock_positions):
        selected_tile_path_lists = []
        for color_location in available_color_locations:
            start = color_location
            goal = [target_color_location[0]+1,target_color_location[1]+1]
            selected_path = self.A_star(start,goal,lock_positions)
            selected_tile_path_lists.append(selected_path)
        return selected_tile_path_lists
        

    def list_flattener(self,List):
        flat_list = []
        for sublist in List:
            for subelement in sublist:
                flat_list.append(subelement)
            # print(sublist)      
        flat_list_unique_elements = []
        for i in range(len(flat_list)-1):
            if flat_list[i] != flat_list[i+1]:
                flat_list_unique_elements.append(flat_list[i])
                
        flat_list_unique_elements.append(flat_list[-1])
            
        return flat_list_unique_elements


    def update_puzzle(self,puzzle_pattern,blank_path):
        # print("\nblank_path: ",blank_path)
        # print("un-puzzlePattern: ", puzzle_pattern)
        clrs = []
        for i in range (len(blank_path)-1):
            row= blank_path[i+1][1]
            col =blank_path[i+1][0]            
            clrs.append(puzzle_pattern[row][col])
            
        for i in range (len(blank_path)-1):
            row= blank_path[i][1]
            col =blank_path[i][0]
            puzzle_pattern [row][col]=clrs[i]
        
        row= blank_path[-1][1]
        col =blank_path[-1][0]
        puzzle_pattern[row][col] = '0'
        
        # print("updated-puzzle_pattern",puzzle_pattern)
        # print("clrs",clrs)
        return puzzle_pattern


    def NewSlicer(self,blank_path_list):
        #make a dict of movements:
        all_movements ={}
        for i in range(len(blank_path_list)-1):
            all_movements[i] = (blank_path_list[i+1],blank_path_list[i])
        # print(all_movements)
        # print("dict ele by ind", all_movements[0] )

        indexes_char = []
        for _,val in all_movements.items():
            # find movement direction
            if val[0][0] == val[1][0]:
                # print('x')
                indexes_char.append('y')
            else:
                indexes_char.append('x')
        
        # print(indexes_char)
        # print(len(indexes_char))
        
        check_char = indexes_char[0]
        # for ind,val in enumerate(indexes_char[1:]):
        indexes = []
        for ind,now_char in enumerate(indexes_char):
            if now_char != check_char:
                indexes.append(ind-1)
                check_char = now_char
        indexes.append(len(indexes_char)-1)
        # print()
        # print("indexes : ", indexes)   
        # print()
        croped_path = []
        for i in indexes:
            croped_path.append(all_movements[i])
        
        # print(croped_path)
        # print(len(croped_path)) 
        # 
        # 
        # 
        # 
        #convart dict to list
        all_moves_list = list(all_movements.values())
        def co_ords_to_loc_convartor(path):
            final_path_dofbot = []
            cord_dict = {1: [0, 0], 2: [1, 0], 3: [2, 0], 4: [3, 0], 5: [4, 0], 6: [0, 1], 7: [1, 1], 8: [2, 1], 9: [3, 1], 10: [4, 1], 
                        11: [0, 2], 12: [1, 2], 13: [2, 2], 14: [3, 2], 15: [4, 2], 16: [0, 3], 17: [1, 3], 18: [2, 3], 19: [3, 3], 
                        20: [4, 3], 21: [0, 4], 22: [1, 4], 23: [2, 4], 24: [3, 4], 25: [4, 4]}
            def find_key(cord_dict, target_val):
                for key,val in cord_dict.items():
                    if val[0] == target_val[0] and val[1] == target_val[1]:
                        return key
            for ele in path:
                key1 = find_key(cord_dict, ele[0])    
                key2 = find_key(cord_dict, ele[1])
                final_path_dofbot.append((key1, key2))
            return final_path_dofbot
        # print("All_movements_locs",co_ords_to_loc_convartor(all_moves_list))
        # print()
        # print("cropped_list: ",co_ords_to_loc_convartor(croped_path))
        croped_path_list = co_ords_to_loc_convartor(croped_path)
        
        def indivisual_path(blank_path_list):
            indivisual_path_list = []
            for _,val in all_movements.items():
                indivisual_path_list.append(val)
            indivisual_path_final = co_ords_to_loc_convartor(indivisual_path_list)
            return indivisual_path_final
        
        indivisual_path_final = indivisual_path(blank_path_list)
        
        return croped_path_list,indivisual_path_final


    def solve_puzzle(self,puzzle_pattern,target_pattern,unsolved_target_list,lock_positions):
        
        # lock_positions = []
        total_path= []
        
        while True:
            
            # for center in lock_positions:
            #     clr = (40,40,40)
            #     loc = ((center[0]*100 + 50),(center[1]*100 + 50))
            
            if len(unsolved_target_list) == 0:
                # print("puzzle solved...")
                break 
            # peak first element color of unsolved target list and start solving it
            # unsolved target list updating each time hence we pick first element every time until there are no elements left.
            target_color_location = unsolved_target_list[0]
            
            target_color = self.find_color_at_location(target_color_location,target_pattern)
            
            #
            # __________________________________________________________________
            # find target color in puzzle_pattern
            #-> note: shouldn't be color at lock_positions
            
            available_color_locations = self.find_location_of_color(puzzle_pattern,target_color)  
            available_color_locations_temp = []
            for valid_loc in available_color_locations:
                if valid_loc not in lock_positions:
                    available_color_locations_temp.append(valid_loc)
            available_color_locations = available_color_locations_temp
            # print("---------------------------------------------------------------")
            # print("\n\n\navailable_color_locations: ",available_color_locations, "target_color:",target_color,"at",target_color_location)
            
            # find paths from each available color locations to destination location using A_star --tile_move_A_star_path_list
            selected_tile_path_lists = self.tile_move_A_star_path_list(available_color_locations,target_color_location,lock_positions)
            
            # find shortest path:
            lengths = []
            for selected_path in selected_tile_path_lists:
                length = len(selected_path)
                lengths.append(length)
            
            index = lengths.index(min(lengths))
            shortest_path = selected_tile_path_lists[index]
            selected_path = shortest_path
            
            # print("selected_avl_clr_loc:",selected_path[0])
            
            # find blank path from blank location to index 1 location in selected path
            # and add index 0 location in blank path
            
            # print("\nselected_path-103",selected_path)
            for i in range(len(selected_path)-1):
                temp_lock_position  = selected_path[i]
                # print("temp_lock_position-106",temp_lock_position)
                blank_space_location = self.find_blank_space(puzzle_pattern)
                goal_point = selected_path[i+1]
                # print("lock_positions", lock_positions)
                lock_positions.append(temp_lock_position)
                # print("lock_positions_append", lock_positions)
                blank_path = self.A_star(blank_space_location,goal_point,lock_positions)
                lock_positions.pop()
                
                blank_path.append(selected_path[i])
                total_path.append(blank_path)
                # print("i:",i,"\nBlank_path:",blank_path)
                # print("lock_positions_pop", lock_positions)
                
                # update_puzzle_pattern
                self.update_puzzle(puzzle_pattern,blank_path)
                updated_puzzle_canvas = CPIG.generate_image_puzzle_pattern(puzzle_pattern,5)   
                #cv2.imshow("updated_puzzle",updated_puzzle_canvas)
                #cv2.waitKey(20)
                #cv2.imshow("prev_updated_puzzle",updated_puzzle_canvas)
                        
            #_____________________________________________________________________
            # update lock_pose.json
            new_lock_pose = [unsolved_target_list[0][0] +1 ,unsolved_target_list[0][1] +1 ]
            lock_positions.append(new_lock_pose)
            # locked_loc = unsolved_target_list.pop(0) 
            unsolved_target_list.pop(0) 
            # print("unsolved_target_list-210:",unsolved_target_list)
                
            # lock_positions.append(locked_loc)
            
            
        #cv2.imshow('puzzle',canvas)
        #cv2.imshow('target',target_canvas)
        #cv2.imshow('solved_puzzle',updated_puzzle_canvas)
        # self.list_flattener(total_path)

        #cv2.waitKey(20)
        # print("total_path",total_path)
        # print(len(total_path))
        # print(np.shape(total_path))

        blank_path_list = self.list_flattener(total_path)
        return blank_path_list      



class functions:
    def read_patterns(self):
        json_path = database_path+"current_pattern.json"
        with open(json_path,"r") as json_file_1:
            data = json.load(json_file_1)
        puzzle_pattern = data["puzzle_pattern"]
        target_pattern = data["target_pattern"]
        return puzzle_pattern,target_pattern
    
    def read_unsolved_target_list_list(self):
        json_path = database_path+"unsolved_target_lists_random_shuffle.json"
        with open(json_path,"r") as json_file:
            data1 = json.load(json_file)
        return data1["unsolved_target_list_lists"]
    
    def solving_lock_position_sequence(self, final_pattern):
        unsolved_target_list = [[0,0],[1,0],[2,0],
                            [0,1],[1,1],[2,1],
                            [0,2],[1,2],[2,2]]
        ind_list = []
        for element in final_pattern:
            ind = unsolved_target_list.index(element)
            ind_list.append(ind)
        return ind_list 
    
    def solve_by_target_list(self,unsolved_target_list):
        puzzle_pattern,target_pattern= self.read_patterns()
        
        
        
        # print(puzzle_pattern, target_pattern)
        lock_positions = []
        blank_path_list = ALGO.solve_puzzle(puzzle_pattern,target_pattern,unsolved_target_list,lock_positions)
        return blank_path_list,puzzle_pattern,target_pattern
    
    def save_final_path_new(self, optimised_path,blank_path_list_final):
        """ Save final_path_dofbot in final_path_dofbot.json file and return final_paht_dofbot
        """
        final_path_dofbot = optimised_path
        data = {
            "final_path_dofbot" : final_path_dofbot,
            "blank_path_list_final": blank_path_list_final
        }
        json_path = database_path+"final_path_dofbot.json"
        with open(json_path,"w") as json_file:
            # print("loding data to final_path_dofbot\n...")
            json.dump(data,json_file,indent=4)
            # print("loded successfully")
        return final_path_dofbot



class solver:
    def random_n_generate(self,length):
        start_time = time.time()
        unsolved_target_list = [[0,0],[1,0],[2,0],
                                [0,1],[1,1],[2,1],
                                [0,2],[1,2],[2,2]]


        index_list = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        
        random_unsolved_target_list_lists =[unsolved_target_list]
        
        for i in range(length-1):
            random.shuffle(index_list)
            unsolved_target_list_temp = []
            for j in index_list:
                unsolved_target_list_temp.append(unsolved_target_list[j])
            random_unsolved_target_list_lists.append(unsolved_target_list_temp)
        
        data = {
            "unsolved_target_list_lists": random_unsolved_target_list_lists
            # "unsolved_target_list_lists": unsolved_target_list_lists
        }
        json_path = database_path+"unsolved_target_lists_random_shuffle.json"
        with open(json_path, "w") as json_file:
            json.dump(data,json_file,indent=4)

        # print("\ndata saved to unsolved_target_lists.json")
        end_time = time.time()
        # print("time taken to save n samples: ", end_time-start_time, "sec")
        
    
    def generate_samples(self,itr):
        """ Run this function to generate random solving sequences.
        """
        iteration = itr
        # waitKey = 50
        # RANDOM_SHUFFLE = random_unsolved_shuffle.random_unsolved()
        self.random_n_generate(iteration)
        # print("\n\nwith {} radnom samples".format(iteration))

    
    def solve_final_optimized(self,itr):
        progress_bar = tqdm(total = itr, desc="Searching Optimized way to: ")
        """
        Solve puzzle and visualize the movements and save the movement co-ordinates to ffinal_path_dofbot.json
        """
        self.generate_samples(itr)
        start_time  = time.time()
        # print("Start_solving\nwait...")
        unsolved_target_list_list_selected = FUN.read_unsolved_target_list_list()
        individual_no_of_steps = []
        individual_final_paths = []
        grouped_no_of_steps = []
        indexes = []    
        
        previous_len = None
        optimized_path = None
        blank_path_list_final = None
        
        for i in range(itr):
            unsolved_target_list = unsolved_target_list_list_selected[i]
            # print("\n\n\t")
            # print("unsolved_target_list_BIN", unsolved_target_list)
            lock_position_sequence = FUN.solving_lock_position_sequence(unsolved_target_list)
            # print("lock_position_sequence_BIN", lock_position_sequence)
            try:
                blank_path_list,puzzle_pattern,target_pattern = FUN.solve_by_target_list(unsolved_target_list)
                # print("blank_path_list_BIN", blank_path_list)
                grouped_blank_path,individual_final_path = ALGO.NewSlicer(blank_path_list)
                individual_no_of_steps.append(len(blank_path_list))
                individual_final_paths.append(individual_final_path)
                grouped_no_of_steps.append(len(grouped_blank_path))
                indexes.append(i)    
            except:
                # print("inside_except")
                
                if i == 0:
                    blank_path_list = [i for i in range(500)]
                    grouped_blank_path = [i for i in range(500)]
                pass
            
            
            if i == 0:
                index_stored = i
                current_len = len(grouped_blank_path)   
                previous_len = current_len
                final_LCP = lock_position_sequence
                blank_path_list_final = blank_path_list
                optimized_path = grouped_blank_path
                individual_final_paths_path = individual_final_path
            else:
                current_len = len(grouped_blank_path)
                if current_len < previous_len:
                    index_stored = i
                    previous_len = current_len
                    final_LCP = lock_position_sequence
                    blank_path_list_final = blank_path_list
                    optimized_path = grouped_blank_path
                    individual_final_paths_path = individual_final_path
                    
            
        
            progress_bar.update(1)
        progress_bar.close() 

        total_search_time = round(time.time() - start_time, 3)
        if total_search_time > 60:
            minutes = total_search_time/60
            # print("total searching time\t\t\t\t\t", round(minutes,2), "min")
        else:
            # print("total searching time\t\t\t\t\t", round(total_search_time,2), "sec")
            pass
        
        
        final_path_dofbot_cords = optimized_path
        
        
        
        # print("\nindividual_steps: \n\t", individual_final_paths_path)
        # print('\ninidividual no of steps : ', len(individual_final_paths_path))
        
        
        final_path_dofbot_json = FUN.save_final_path_new(final_path_dofbot_cords, blank_path_list_final)
        # print("\ntarget_following_sequence",final_LCP)
        # print("-"*50,"\noptimized_steps:\n\t", final_path_dofbot_json,"\n\noptimized no of steps: ",len(final_path_dofbot_json),"\n","-"*50,"\n") #-----------------------------------

         
        rospy.loginfo("ENDED")
        return individual_final_paths_path,final_path_dofbot_json,final_LCP,total_search_time
        
CPIG = color_pallet_image_generator()
ALGO = algorithm()
FUN = functions()
SOLVE = solver()



def main_method(n):
    individual_final_paths_path,final_path_dofbot_json,solving_sequence,search_time_sec = SOLVE.solve_final_optimized(n)
    individual_no_of_steps = len(individual_final_paths_path)
    optimized_no_of_steps = len(final_path_dofbot_json)
    print("individual_no_of_steps: ", individual_no_of_steps)
    print("optimized_no_of_steps: ", optimized_no_of_steps)
    print("solving_sequence : ", solving_sequence)
    print("total_search_time: ", search_time_sec, " sec")
    print("\nIndividual steps: \n", individual_final_paths_path)
    print("\nOptimized steps: \n", final_path_dofbot_json)
    return individual_no_of_steps,optimized_no_of_steps, individual_final_paths_path, final_path_dofbot_json,search_time_sec

def check():
    unsolved_target_list_list_selected = FUN.read_unsolved_target_list_list()
    print(unsolved_target_list_list_selected)
    unsolved_target_list = unsolved_target_list_list_selected[0]
    print(unsolved_target_list)
    
    blank_path_list = FUN.solve_by_target_list(unsolved_target_list)
    print(blank_path_list)
    # print("end")



def append_to_json(json_file_path, puzzle_pattern_index, target_pattern_index, no_of_iterations,
                  no_of_individual_steps, no_of_optimized_steps, individual_steps, optimized_steps,search_time_sec):
    try:
        # Read existing data from the JSON file
        with open(json_file_path, 'r') as file:
            existing_data = json.load(file)
    except FileNotFoundError:
        # If the file doesn't exist, start with an empty list
        existing_data = []

    # Append new data to the existing data
    new_data = {
        'puzzle_pattern_index': puzzle_pattern_index,
        'target_pattern_index': target_pattern_index,
        'no. of iterations': no_of_iterations,
        'search_time in sec': search_time_sec,
        'no. of individual steps': no_of_individual_steps,
        'no. of optimized steps': no_of_optimized_steps,
        'individual_steps': individual_steps,
        'optimized_steps': optimized_steps
    }
    # new_data = {
    #     'puzzle_pattern_index': puzzle_pattern_index,
    #     'target_pattern_index': target_pattern_index,
    #     'no. of iterations': no_of_iterations,
    #     'search_time in sec': search_time_sec,
    #     'no. of individual steps': no_of_individual_steps,
    #     'no. of optimized steps': no_of_optimized_steps
    #  }
    existing_data.append(new_data)

    # Write the updated data back to the JSON file
    with open(json_file_path, 'w') as file:
        json.dump(existing_data, file, indent=2)
    
    
    
if __name__ == '__main__':
    # rospy.init_node("puzzle_solver",anonymous=True)
    if len(sys.argv) > 1:
        try:
            iterations = int(sys.argv[1])
            puzzle_index = (sys.argv[2])
            target_index = (sys.argv[3])
            # print(f"My Integer: {my_integer}")
        except:
            
            print("Invalid integer provided.")
    else:
        iterations = 1
        
    # individual_no_of_steps,optimized_no_of_steps, individual_final_paths_path, final_path_dofbot_json = main_method(iterations)
    print("iterations: ",iterations)
    no_of_individual_steps, no_of_optimized_steps, individual_steps, optimized_steps,search_time_sec = main_method(iterations)
    json_path = '/home/cse4568/verify/dofbot_verify/verify/src/Algo_performance/my_data.json'
    append_to_json(json_path, puzzle_index,target_index,iterations,no_of_individual_steps,no_of_optimized_steps,individual_steps,optimized_steps,search_time_sec)
    
    # check()
    # try:
    #     rospy.loginfo("ENter")
    #     main_method()
    #     rospy.loginfo("capture and save successful")
    # except:
    #     rospy.loginfo("Puzzle_solved")
    #     pass