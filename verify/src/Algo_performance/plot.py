import json
import numpy as np
import matplotlib.pyplot as plt

package_path = "/home/cse4568/verify/dofbot_verify/verify"
json_path = package_path+'/src/Algo_performance/my_data.json'


def read_patterns(json_path):
    '''

        "puzzle_pattern_index": "0",
        "target_pattern_index": "0",
        "no. of iterations": 50,
        "search_time in sec": 0.573,
        "no. of individual steps": 46,
        "no. of optimized steps": 33,
        "individual_steps":[[]]
        "optimized_steps" :[[]]
        
    '''
    with open(json_path) as json_file:
        data = json.load(json_file)

    return data


iterations = [50,100,200,500]

def sort():
    all_data = read_patterns(json_path)

    print("all_data_len: ",len(all_data))
    steps_count = []
    timeit = []
    while (len(all_data)!=0):
        steps = []
        times = []
        for i in range(4):
            data = all_data.pop(0)
            steps.append(data["no. of optimized steps"])
            times.append(data["search_time in sec"])
            
        steps_count.append(steps)
        timeit.append(times)

    # convert into numpy array
    steps_count = np.array(steps_count)
    timeit = np.array(timeit)
    
    # Transpose
    steps_count = np.transpose(steps_count)
    timeit = np.transpose(timeit)
    return steps_count, timeit
    


# draw 2d graphs for (each iterartion)
# x puzzle number
# y no. of optimized steps



def plot_steps(x_values, y_values1, y_values2, y_values3, y_values4):
    # Create subplots in a 2x2 grid layout
    fig, axs = plt.subplots(2, 2, figsize=(12, 8))

    # Plotting the four charts
    axs[0, 0].bar(x_values, y_values1, label='no of steps', color='blue')
    axs[0, 1].bar(x_values, y_values2, label='no of steps', color='green')
    axs[1, 0].bar(x_values, y_values3, label='no of steps', color='red')
    axs[1, 1].bar(x_values, y_values4, label='no of steps', color='purple')

    # Calculate and plot the average line for each subplot
    for ax, y_values, sample_size in zip(axs.flatten(), [y_values1, y_values2, y_values3, y_values4], [50, 100, 200, 500]):
        average_value = np.mean(y_values)
        ax.axhline(average_value, color='black', linestyle='dashed', linewidth=2, label='Average')
        
        # Annotate the average value on the subplot
        ax.annotate(f'Avg: {average_value:.2f}', xy=(0.5, 0.9), xycoords='axes fraction', ha='center', va='center',
                    bbox=dict(boxstyle='round', fc='w', alpha=0.8),fontsize=13)

    # Set labels and title for each subplot
    axs[0, 0].set_xlabel('solved_puzzles')
    axs[0, 0].set_ylabel('no. of steps')
    axs[0, 0].set_title('Sample size = 50',fontsize = 15)
    
    # Manually place labels at desired positions
    # axs[0, 0].text(0.8, 0.05, 'Label 1', transform=axs[0, 0].transAxes, color='blue')
    
    axs[0, 1].set_xlabel('solved_puzzles')
    axs[0, 1].set_ylabel('no. of steps')
    axs[0, 1].set_title('Sample size = 100', fontsize = 15)
    
    # axs[0, 1].text(0.5, -0.2, 'Label 2', transform=axs[0, 1].transAxes, color='green')
    
    axs[1, 0].set_xlabel('solved_puzzles')
    axs[1, 0].set_ylabel('no. of steps')
    axs[1, 0].set_title('Sample size = 200', fontsize = 15)
    
    # axs[1, 0].text(0.2, 0.9, 'Label 3', transform=axs[1, 0].transAxes, color='red')
    
    axs[1, 1].set_xlabel('solved_puzzles')
    axs[1, 1].set_ylabel('no. of steps')
    axs[1, 1].set_title('Sample size = 500',fontsize = 15)
    
    # axs[1, 1].text(0.1, 0.2, 'Label 4', transform=axs[1, 1].transAxes, color='purple')

    # Adjust layout for better appearance
    plt.tight_layout()
    plt.savefig('steps_comp.png')  # Change the filename and extension as needed

    # Show the plot
    plt.show()



def plot_times(x_values, y_values1, y_values2, y_values3, y_values4):
    # Create subplots in a 2x2 grid layout
    fig, axs = plt.subplots(2, 2, figsize=(12, 8))

    # Plotting the four charts
    axs[0, 0].bar(x_values, y_values1, label='time', color='blue')
    axs[0, 1].bar(x_values, y_values2, label='time', color='green')
    axs[1, 0].bar(x_values, y_values3, label='time', color='red')
    axs[1, 1].bar(x_values, y_values4, label='time', color='purple')

    # Calculate and plot the average line for each subplot
    for ax, y_values, sample_size in zip(axs.flatten(), [y_values1, y_values2, y_values3, y_values4], [50, 100, 200, 500]):
        average_value = np.mean(y_values)
        ax.axhline(average_value, color='black', linestyle='dashed', linewidth=2, label='Average')
        
        # Annotate the average value on the subplot
        ax.annotate(f'Avg. (sec) : {average_value:.2f} ', xy=(0.5, 0.9), xycoords='axes fraction', ha='center', va='center',
                    bbox=dict(boxstyle='round', fc='w', alpha=0.8),fontsize=13)

    # Set labels and title for each subplot
    axs[0, 0].set_xlabel('solved_puzzles')
    axs[0, 0].set_ylabel('time (sec)')
    axs[0, 0].set_title('Sample size = 50',fontsize = 15)
    
    # Manually place labels at desired positions
    # axs[0, 0].text(0.8, 0.05, 'Label 1', transform=axs[0, 0].transAxes, color='blue')
    
    axs[0, 1].set_xlabel('solved_puzzles')
    axs[0, 1].set_ylabel('time (sec)')
    axs[0, 1].set_title('Sample size = 100', fontsize = 15)
    
    # axs[0, 1].text(0.5, -0.2, 'Label 2', transform=axs[0, 1].transAxes, color='green')
    
    axs[1, 0].set_xlabel('solved_puzzles')
    axs[1, 0].set_ylabel('time (sec)')
    axs[1, 0].set_title('Sample size = 200', fontsize = 15)
    
    # axs[1, 0].text(0.2, 0.9, 'Label 3', transform=axs[1, 0].transAxes, color='red')
    
    axs[1, 1].set_xlabel('solved_puzzles')
    axs[1, 1].set_ylabel('time (sec)')
    axs[1, 1].set_title('Sample size = 500',fontsize = 15)
    
    # axs[1, 1].text(0.1, 0.2, 'Label 4', transform=axs[1, 1].transAxes, color='purple')

    # Adjust layout for better appearance
    plt.tight_layout()
    plt.savefig('time_comp.png')  # Change the filename and extension as needed

    # Show the plot
    plt.show()




def main():
    steps_count, timeit = sort()
    x_values = np.arange(0, len(steps_count[0]))
    y_values1 = steps_count[0]
    y_values2 = steps_count[1]
    y_values3 = steps_count[2]
    y_values4 = steps_count[3]
    
    
    y_time1 = timeit[0]
    y_time2 = timeit[1]
    y_time3 = timeit[2]
    y_time4 = timeit[3]
    
    
    
    # plot_four_charts(x_values,y_values1,y_values2,y_values3,y_values4)
    plot_steps(x_values,y_values1,y_values2,y_values3,y_values4)
    plot_times(x_values,y_time1,y_time2, y_time3, y_time4)



main()

# plt.show()