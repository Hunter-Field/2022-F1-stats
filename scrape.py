# install pandas ('pip install pandas')
# install lxml ('pip install lxml')
import pandas as pd
import csv
import os

race_names = ['bahrain', 'saudi-arabia', 'australia', 'emilia-romagna', 'miami', 'spain', 'monaco', 'azerbaijan',
'canada', 'great-britain', 'austria', 'france', 'hungary', 'belgium', 'netherlands', 'italy', 'singapore',
'japan', 'united-states', 'mexico', 'brazil', 'abu-dhabi']
race_links = ['/1124/bahrain/' , '/1125/saudi-arabia', '/1108/australia', '/1109/italy', '/1110/miami' , 
    '/1111/spain', '/1112/monaco', '/1126/azerbaijan', '/1113/canada', '/1114/great-britain', '/1115/austria', 
    '/1116/france', '/1117/hungary', '/1118/belgium', '/1119/netherlands', '/1120/italy', '/1133/singapore', 
    '/1134/japan', '/1135/united-states', '/1136/mexico', '/1137/brazil', '/1138/abu-dhabi']
race_data = ['race-result', 'starting-grid']
data_links = ['/race-result.html', '/starting-grid.html']

def main():
    for i in range(len(race_names)):
        for j in range(len(race_data)):
            file_location = './races/' + race_names[i] + '/' + race_data[j] + '.csv'
            os.makedirs(os.path.dirname(file_location), exist_ok=True) # creates the directory if it doesn't exist
            data_field = get_data(i, j)[0]
            data_field.to_csv(file_location, index=False)
    print('\nWeb scraping finished!\n')
    

def get_data(race, page):
    data_field = pd.read_html('https://www.formula1.com/en/results.html/2022/races' + race_links[race] + data_links[page])
    return data_field


if __name__ == '__main__':
    main()