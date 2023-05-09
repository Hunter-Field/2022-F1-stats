import csv
import matplotlib.pyplot as plt
import numpy as np

def main():
    # DISPLAYS THE OPTIONS FOR THE USER TO SELECT
    print('\nThis program calculates the likelihood that a driver would finish within 3 places of their starting grid position at the end of any given race in 2022.\n')
    race_names = ['(1) Bahrain', '(2) Saudi Arabia',  '(3) Australia', '(4) Emilia Romangna', '(5) Miami', '(6) Spain', '(7) Monaco', '(8) Azerbaijan', '(9) Canada', '(10) Great Britain', '(11) Austria', '(12) France', '(13) Hungary', '(14) Belgium', '(15) Netherlands', '(16) Italy', '(17) Singapore', '(18) Japan', '(19) United States', '(20) Mexico', '(21) Brazil', '(22) Abu Dhabi', '(23) ALL']
    print('Would which race would like to view statistics for?\n')
    print(f'{race_names[0]:<25}{race_names[1]:<25}{race_names[2]:<25}{race_names[3]:<25}')
    print(f'{race_names[4]:<25}{race_names[5]:<25}{race_names[6]:<25}{race_names[7]:<25}')
    print(f'{race_names[8]:<25}{race_names[9]:<25}{race_names[10]:<25}{race_names[11]:<25}')
    print(f'{race_names[12]:<25}{race_names[13]:<25}{race_names[14]:<25}{race_names[15]:<25}')
    print(f'{race_names[16]:<25}{race_names[17]:<25}{race_names[18]:<25}{race_names[19]:<25}')
    print(f'{race_names[20]:<25}{race_names[21]:<25}{race_names[22]:<25}\n')

    number = 0
    while not number:                                   # ERROR CHECK
        number = input('Enter a number: ')
        number = check_for_correct_int(number)

    race_results = 0
    starting_grid = 0

    # IF USER SELECTED A SINGLE RACE
    if not (number == 23):
        race_results, starting_grid = get_data(number - 1)  
    
        results = []
        x_axis = []
        y1_axis = []
        y2_axis = []

        # FILTERS THE DATA FROM THE LARGE DATA SETS INTO SMALL ARRAYS
        for i in range(1, len(starting_grid)): 
            driver_stats = [-1, -1, -1]

            split_name = str(starting_grid[i][3]).split()
            driver_stats[0] = split_name[2]
            x_axis.append(split_name[2])

            driver_stats[1] = int(starting_grid[i][1])
            y1_axis.append(int(starting_grid[i][1]))

            for j in range(1, len(race_results)):
                if(starting_grid[i][3] == race_results[j][3]):
                    if(race_results[j][1] == 'NC'):                    # ERROR CHECK
                        driver_stats[2] = len(starting_grid) - 1
                        y2_axis.append(len(starting_grid) - 1)
                    else:
                        driver_stats[2] = int(race_results[j][1])
                        y2_axis.append(int(race_results[j][1]))
            results.append(driver_stats) # [name, start, end]

        # GETS THE PERCENTAGE OF DRIVERS WITHIN 3 PLACES
        percentage = get_percentage(results, len(starting_grid) - 1)

        # PRINTS THE PERCENTAGE AND WHERE THE RACE WAS LOCATED
        location = race_names[number - 1].split()
        if len(location) == 3:
            location = location[1] + ' ' + location[2]
        else:
            location = location[1]
        print(f'\nThe percentage of drivers who finished within 3 places in {location} was: {percentage:.2f}%.\n')
        if len(starting_grid) - 1 != 20:
            print('Note that the graph does not show all 20 racers. This is because one or more racers dropped out before the race started.\n')

        # PLOTS THE DATA
        fig, ax = plt.subplots()
        ax.plot(x_axis, y1_axis, 'b.', label='Starting Grid')  # Plot the first data set
        ax.plot(x_axis, y2_axis, 'r.', label='Finish') # Plot the second data set

        # PLOTS A LINEAR REGRESSION LINE ON THE SAME PLOT
        x_axis_nums = range(1, len(y2_axis) + 1)
        slope, intercept = np.polyfit(x_axis_nums, y2_axis, 1)
        line = []
        for x in range(len(x_axis_nums)):
            line.append(slope * x_axis_nums[x] + intercept)
        ax.plot(x_axis, line, 'r-')

        # ADD A Y-AXIS TICK MARKS FOR EACH OF THE 20 PLACES
        plt.yticks(y1_axis)
        ax.set_ylim(ax.get_ylim()[::-1])

        # ADD LABELS AND A LEGEND
        ax.set_xlabel('Drivers')
        ax.set_ylabel('Places')
        ax.set_title('Starting Grid vs Resulting Placements in ' + location)
        ax.legend()
        plt.show()
    
    # IF THE USER WANTS TO SEE ALL RACES ON ONE PLOT
    else:
        all_results = []
        all_percentages = []
        all_race_names = []

        # FILTERS THE DATA FROM EACH LARGE RACE DATA SET INTO A 2D ARRAY OF RESULTS
        for x in range(len(race_names) - 1):
            race_results, starting_grid = get_data(x)
    
            results = []
            for i in range(1, len(starting_grid)):
                driver_stats = [-1, -1, -1]

                split_name = str(starting_grid[i][3]).split()
                driver_stats[0] = split_name[2]
                driver_stats[1] = int(starting_grid[i][1])

                for j in range(1, len(race_results)):
                    if(starting_grid[i][3] == race_results[j][3]):
                        if(race_results[j][1] == 'NC'):                    # ERROR CHECK
                            driver_stats[2] = len(starting_grid) - 1
                        else:
                            driver_stats[2] = int(race_results[j][1])

                results.append(driver_stats) # [name, start, end]
            all_results.append(results) # [[name, start, end], [name, start, end]]

            # GETS THE PERCENTAGE OF DRIVERS WITHIN 3 PLACES
            percentage = get_percentage(results, len(starting_grid) - 1)
            all_percentages.append(percentage)
            
            # ADDS THE LOCATION OF EACH RACE TO AN ARRAY
            location = race_names[x].split()
            if len(location) == 3:
                location = location[1] + ' ' + location[2]
            else:
                location = location[1]
            all_race_names.append(location)

        # CALCULATES AND PRINTS THE PERCENTAGE OF DRIVERS WITHIN 3 PLACES FOR THE ENTIRE SEASON
        avg_percentage = 0
        for k in range(len(all_percentages)):
            avg_percentage += all_percentages[k]
        avg_percentage /= len(all_percentages)
        print(f'\nThe percentage of drivers who finished within 3 places throughout 2022 was {avg_percentage:.2f}%.\n')

        # PLOTS THE PERCENTAGE OF EACH RACE
        fig, ax = plt.subplots()
        ax.plot(all_race_names, all_percentages, 'r.', label='Starting Grid')
        ax.set_xticks(all_race_names)
        ax.set_xticklabels(all_race_names, rotation=90)

        # ADD LABELS AND A LEGEND
        ax.set_xlabel('Location')
        ax.set_ylabel('Percentage')
        ax.set_title('Percentage of Drivers Finishing Within 3 Places in 2022 F1 Races')
        plt.subplots_adjust(bottom=0.4)

        plt.show()

# CHECKS TO SEE IF THE VALUE THE USER INPUTTED IS A NUMBER WITHIN THE RANGE 1-23
def check_for_correct_int(input):
    try:
        number = int(input)
    except ValueError:
        print('Input must be an integer between 1 and 23\n')
        return 0
    
    if(number < 1 or number > 23):
        print('Input must be an integer between 1 and 23\n')
        return 0

    return number

# CALCULATES AND RETURNS THE PERCENTAGE OF DRIVERS WITHIN 3 PLACES
def get_percentage(results, length):
    num_within_3 = 0
    num_total = length
    for i in range(len(results)):
        if (abs(results[i][1] - results[i][2])) < 4:
            num_within_3 += 1
    percentage = (num_within_3 / num_total) * 100

    return percentage

# READS DATA FROM THE FILES AND RETURNS TWO 2D ARRAYS WITH ALL DATA CONTAINED IN THE CSV FILES
def get_data(index):
    file_names = ['bahrain', 'saudi-arabia',  'australia', 'emilia-romagna', 'miami', 'spain', 'monaco', 'azerbaijan', 'canada', 'great-britain', 'austria', 'france', 'hungary', 'belgium', 'netherlands', 'italy', 'singapore', 'japan', 'united-states', 'mexico', 'brazil', 'abu-dhabi']
    result_file = './races/' + file_names[index] + '/race-result.csv'
    starting_file = './races/' + file_names[index] + '/starting-grid.csv'
    with open(result_file, 'r') as file:
        reader = csv.reader(file, delimiter=',')
        race_results = [row for row in reader] 
    with open(starting_file, 'r') as file:
        reader = csv.reader(file, delimiter=',')
        starting_grid = [row for row in reader]   

    return race_results, starting_grid

if __name__ == '__main__':
    main()