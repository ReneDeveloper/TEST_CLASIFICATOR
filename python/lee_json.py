


import json

with open('test_json.json') as data_file:    
    data = json.load(data_file)
    for v in data.values():
        print(v['id_interno'])



