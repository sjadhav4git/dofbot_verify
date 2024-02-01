import json
import numpy as np
import matplotlib.pyplot as plt


txt_path = '/home/cse4568/verify/dofbot_verify/verify/src/Algo_performance/Anupam_Anaylysis_rubik_race.txt'

def read_txt(input_file):
    with open(input_file, 'r') as txt_file:
        steps = []
        times = []
        for line in txt_file:
            # Assuming the data is comma-separated
            puzzle, shuffle, multistep, singlestep, time = line.strip().split(';')
            # print(puzzle, shuffle, multistep, singlestep, time)
            # Creating a dictionary for each line
            steps.append(int(multistep))
            times.append(round(float(time),3))
    return steps,times



def plot_steps_single(x_values, y_values):
    # Create a single subplot
    fig, ax = plt.subplots(figsize=(8, 6))

    # Plotting the data
    ax.bar(x_values, y_values, label='Number of Steps', color='orchid')

    # Calculate and plot the average line
    average_value = np.mean(y_values)
    ax.axhline(average_value, color='black', linestyle='dashed', linewidth=2, label='Average')
    
    # Annotate the average value on the graph
    ax.annotate(f'Avg: {average_value:.2f}', xy=(0.5, 0.9), xycoords='axes fraction', ha='center', va='center',
                bbox=dict(boxstyle='round', fc='w', alpha=0.8), fontsize=13)

    # Set labels and title
    ax.set_xlabel('Solved Puzzles')
    ax.set_ylabel('Number of Steps')
    ax.set_title('Number of Steps for Each Puzzle', fontsize=15)

    # Display legend
    ax.legend()

    # Adjust layout for better appearance
    plt.tight_layout()
    plt.savefig('steps_single.png')  # Change the filename and extension as needed

    # Show the plot
    plt.show()












def main():
    steps, times = read_txt(txt_path)
    x_values = np.arange(0, len(steps))
    
    plot_steps_single(x_values,steps)
    plot_steps_single(x_values,times)



main()

# plt.show()