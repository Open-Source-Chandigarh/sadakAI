import os
import json
import csv

def json_to_csv(output_csv):
    folder_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'embedding_data')
    
    all_data = []

    for file_name in os.listdir(folder_path):
        if file_name.endswith('.json'):
            file_path = os.path.join(folder_path, file_name)
            
            with open(file_path, 'r') as json_file:
                data = json.load(json_file)
                if isinstance(data, list):
                    all_data.extend(data)
                else:
                    all_data.append(data)
    
    if all_data:
        keys = all_data[0].keys()
        
        with open(output_csv, 'w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=keys)
            writer.writeheader()
            for data in all_data:
                writer.writerow(data)

json_to_csv('app/chat/data/data.csv')