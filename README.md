### Data parsing
There is a description how station.xlsx were parsed

1. Analysis of xlsx file
    * data about stations were divided into regions
    * region list has two main stations and each station had distance according to these two main stations
    * there were whitespace between region lists
    * we had 4 necessary fields from region lists: station_id, station_name, distance_back, distance_to, other unwanted rows are ignored
      - station_id is the id of the considering station
      - station_name its name
      - distance_back is the distance to start station
      - distance_to is the distance to the end station 
    * if station has distance_back equals 0, it implies that it is start station
    * vice versa if distance_to equals 0, it implies that it is end station
2. Get station IDs:
    * For purposes of convenience we decided to store the station_ids separately from the file where distances between stations are stored 
    * Some station_name had several IDs, as example station: "ОП Ост. пункт 1177 км"
       because several stations in the different place had the same name
    * We decided to map the station_id -> station_name, not vice versa: station_name -> station_id
    * We parsed each line in xls file, and if 4 fields are not empty or corrupted
    * we collect the tuples of (station_id, station_name) in the list
      eventually saved it loc_id_map.json file in json format
3. Get station distances:
    * Each station must have at least 2 distances in its list, since it has two routes to targeted stations in region
    * More than 2 routes will be in case when there are several routes to different stations from one station
    * So the station_to is detected in the first entry in every region list where distance_to is equal 0
    * So the station_back is detected in the last entry in every region list where distance_back is equal 0
    * So the there is a map station_id -> [ \
        [station_to, distance_to], \
        [station_back, distance_back], \
        ..., \
        [another_station, distance_to_another_station] \
        ] 
    * If there are other routes in the same station, these routes will be appended to routes list of station 
    * Eventually it was saved to graph.json file in json format
