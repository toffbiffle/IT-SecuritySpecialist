# Uppgift 3
## Result
Computer name: makar
lat: 59.8586, long: 17.6391
Closest city: Uppsala

## How to run:
Run tests: uv run pytest -vv solution.py
Run solution: uv run solution.py from the same folder 
                that holds tracking.json and solution.py

## Assumptions
Valid existing JSON file.
File contains a valid JSON string with computer_name as key and [latitude,longitude] as value.
A computer is considered isolated if it has no neighbours.
The function return a computer_name only if ONE can be determined as isolated. 
    Otherwise it will return a ValueError.

## Analysis of threshold value
A value of 0.001 degree is about 0.11 km north/south and 0.056-0.062 km east/west.
If I change the threshold to 0.0001, I get way to many location that assume that they dont have any neighbours.
On the other hand, if I change the threshold to 1 it would assume that every location has a neighbour close enough as 1 degree would mean within about 111 km.