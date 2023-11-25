import json
import os
from datetime import datetime

def update_editions(file_path):

    datetime_format='%Y-%m-%d'
    edition_increment=15

    try:
        # print(os.listdir())
        with open(file_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {'updation_date': None, 'editions': {}}

    # Get the current and stored date
    current_date = datetime.date(datetime.now())
    last_updated_date=datetime.date(datetime.strptime(data['updation_date'],datetime_format))
  
    # If the current date is greater from the stored date, update editions
    if current_date==last_updated_date:
        print('Editions are up to date')

    elif (current_date > last_updated_date): #6==Sunday
        data['updation_date'] = current_date.strftime(datetime_format)

        if datetime.weekday(current_date)!=6:

            for location, edition in data['editions'].items():
                data['editions'][location] = edition + edition_increment

                print("Updated editions")

        else:
            value=data['editions']['RABIBAR']
            data['editions']['RABIBAR'] = value + 15

        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)

def get_editions(file_path='editions.json'):
    
    update_editions(file_path)

    with open(file_path, 'r') as file:
        data = json.load(file)

        return data

if __name__ == '__main__':
    json_file_path = 'src/storage/editions.json'
    print(get_editions(json_file_path))
