import pandas as pd
import json
import re

def clean_station_code(value):
    if pd.isna(value):
        return None
    digits = ''.join(filter(str.isdigit, str(value)))
    return digits if len(digits) == 6 else None

def clean_station_name(value):
    if pd.isna(value):
        return None
    return value

def clean_distance(value):
    if pd.isna(value):
        return None
    match = re.search(r'(\d+)', str(value))
    return int(match.group(1)) if match else None


# gives tuples with format: (station_code, station_name, station_to, distance)
def stations_parse(xlsx_path):
    df = pd.read_excel(xlsx_path, sheet_name='Кзх', skiprows=7)

    valid_rows = []
    station_to = ""
    count = 0
    regionNum = 0
    for i in range(len(df)):
        station_code = clean_station_code(df.iloc[i, 1])  
        station_name = clean_station_name(df.iloc[i,2])
        distance_to = clean_distance(df.iloc[i, 3])  
        distance_back = clean_distance(df.iloc[i, 4])
        
        if  distance_to == 0:
            station_to = station_code

        if not (station_code is None or distance_to is None or station_name is None or station_to is None or distance_back is None):
            valid_rows.append([station_code, station_name, station_to,distance_to, distance_back])
            count += 1
            if distance_back == 0:
                station_from = station_code
                for j in range(len(valid_rows)-count, len(valid_rows)):
                    valid_rows[j].append(station_from)
        else:
            if station_code is not None:
                regionNum += 1
            count = 0
            station_to = ""
    
    
    return valid_rows

def fetchStationNamesAndIds(data):
    dic = {}
    for i in range(len(data)):
        station_id = data[i][0]
        station_name = data[i][1]
        if station_id in dic and station_name != dic[station_id]:
            print("Error:", "new station name: " + str(station_name), "station id: " + str(station_id), "old station name: " + str(dic[station_id]))
        dic[station_id] = station_name

    return dic
    

def fetchDistances(valid_rows):
    dic = {}
    for i in range(len(valid_rows)):
        station_id = valid_rows[i][0]
        station_to = valid_rows[i][2]
        distance_to = valid_rows[i][3]

        distance_back = valid_rows[i][4]
        station_back = valid_rows[i][5]
        appending_tuple = (station_to, distance_to)
        second_tuple = (station_back, distance_back)

        if station_id not in dic:
            dic[station_id] = [appending_tuple]
            dic[station_id].append(second_tuple)
        else:
            flag1 = False 
            flag2 = False
            for i in range(len(dic[station_id])):
                (id, distance) = dic[station_id][i]
                if id == station_id and distance_to == distance:
                    flag1 = True
                if id == station_back and distance == distance_back:
                    flag2 = True 
                if flag1 and flag2:
                    break
            if not flag1:
                dic[station_id].append(appending_tuple)
            if not flag2:
                dic[station_id].append(second_tuple)
        
    return dic


def save_to_json(data, output_path):
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    xlsx_path = "КЗХ_2024-07-29.xlsx"
    output_distances = "graph.json"
    output_names = "loc_id_map.json"
    
    try:
        rows = stations_parse(xlsx_path)

        # Names parsing
        names = fetchStationNamesAndIds(rows)
        save_to_json(names, output_names)

        # Distance parsing
        distances = fetchDistances(rows)
        save_to_json(distances, output_distances)

    except Exception as e:
        import traceback
        traceback.print_exc()