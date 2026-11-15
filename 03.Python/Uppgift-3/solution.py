import pytest
import json
from itertools import combinations

def solution( path: str ) -> str:
    """Read JSON from path and determine if any key(computer_name) has any
        neighbour closer then the threshold in their vicinity.
    
    To get the expected output the algorithm need to find ONE single computer_name
    that is isolated from the rest. If none or more then one computer_name 
    is found the function will throw a ValueError.

    input: str  - path to JSON file containing multiple computer names 
                    in format: "computer_name": [lat,lon]
    output: str - computer_name if computer_name is found without a neighbour 
                    at or below threshold, 
    raise: 
        ValueError - if no isolated computer_name is found
        ValueError - if more then one computer_name is missing neighbours
    """
    data = read_JSON_from_file( path )
    has_close_neighbour = set()
    missing_neighbours = []

    # To avoid checking values more then once I use combinations to create unique checks between computer_names
    for computer_name_a, computer_name_b in combinations( data, 2 ):
        if computer_name_a in has_close_neighbour and computer_name_b in has_close_neighbour:
            continue

        if is_positions_close_together( data[computer_name_a], data[computer_name_b] ):
            has_close_neighbour.update( ( computer_name_a, computer_name_b ) )  # Add both to has_close_neigbour if True
        
    # Add the missing computer_name_a from has_close_neighbour to missing_neighbour
    for computer_name in data:
        if computer_name not in has_close_neighbour:
            missing_neighbours.append( computer_name )

    if len( missing_neighbours ) == 0:
        raise ValueError( "Every computer_name has a neighbour within the threshold." )
    elif len( missing_neighbours ) == 1: # If only one computer_name is missing neighbours we return it.
        return missing_neighbours[0]
    else:
        raise ValueError( "Too many computer_names without neighbours were found." )

# Skriv din hjälpfunktion här (med egen docstring).
def read_JSON_from_file( path: str ) -> dict[str, list]:
    """Fetch data from file at path
    
    input: str: path - filepath to JSON file
    output: dict: data - dictionary with data from JSON file
    """
    with open( path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

def is_positions_close_together(pos1: list[float], pos2: list[float], threshold: float=0.001 ) -> bool:
    """Return True if two geographic positions are within a coordinate tolerance.
    
        Takes three arguments, 
        First:  a list with two float values for lat,long
        Second: a list with two float values for lat,long
        Third: threshold in float to compare with, default to 0.001
    
        input:
            pos1, pos2 - list  - two positions each, lat and long
            threshold  - float - 0.001 is about 110 m north/south and 56-62 m east-west
                                    at these latitude values which feels as reasonable limits.
    
        output: bool - True if the absolute difference between both positions(lat & long) is at or below threshold

        raise:
            ValueError: If either position does not contain exactly two values.
        """
    # Check so that pos1 and pos2 have the correct amount of values, 2.
    if len( pos1 ) > 2 or len( pos2 ) > 2:
        raise ValueError("One or both of pos1 and pos2 have too many values.")
    elif len( pos1 ) < 2 or len( pos2 ) < 2:
        raise ValueError("One or both of pos1 and pos2 have too few values")

    lat1 = pos1[0]
    lon1 = pos1[1]
    
    lat2 = pos2[0]
    lon2 = pos2[1]

    if abs( lat1 - lat2 ) <= threshold and abs( lon1 - lon2 ) <= threshold:
        return True
    else: 
        return False
    
    #return abs( lat1 - lat2 ) <= threshold and abs( lon1 - lon2 ) <= threshold

def test_solution(tmp_path) -> None:
    namn = solution("tracking.json")
    assert type(namn) == str, "solution() should return a string"
    with open("tracking.json") as fil:
        assert namn in json.load(fil), "The name should be one of the computers in the file"

    # Ett litet exempel med en egen testfil (tmp_path är en tillfällig mapp från pytest).
    fil = tmp_path / "exempel.json"
    fil.write_text(
        json.dumps(
            {
                "a": [59.3291, 18.0681],
                "b": [59.3293, 18.0687],
                "c": [57.7089, 11.9746],
            }
        )
    )
    assert solution(str(fil)) == "c"

def test_ingen_ensam(tmp_path):
    # Här står alla datorer på samma plats, så det finns ingen stulen dator att hitta.
    # Funktionen ska inte gissa. Det här testet godtar vilket undantag som helst:
    # i dina egna tester ska du vara mer exakt.
    fil = tmp_path / "ingen.json"
    fil.write_text(json.dumps({"a": [59.3291, 18.0681], "b": [59.3293, 18.0687]}))
    with pytest.raises(Exception):
        solution(str(fil))

# Egna tester: skriv minst tre här (se test_solution för hur man skriver en testfil).
# 3st egna tester i den här filen betyder 3st nya funktioner och inte enbart 3st extra assert rader
def test_no_file():
    with pytest.raises(FileNotFoundError):
        solution("")

def test_no_data(tmp_path):
    fil = tmp_path / "no_data.json"
    fil.write_text( json.dumps({}) )
    with pytest.raises(ValueError):
        solution( str(fil) )

def test_multiple_isolated_computer_names(tmp_path):
    fil = tmp_path / "multiple_hits.json"
    fil.write_text(
        json.dumps(
            {
                "a": [57.7092, 11.9742], 
                "b": [59.3292, 18.0689], 
                "c": [55.6045, 13.0033], 
                "d": [59.5886, 17.6391],
            }
        )
    )
    with pytest.raises(ValueError):
        solution(str(fil))

def test_coordinates():
    assert is_positions_close_together( [57.7092, 11.9742], [57.7093, 11.9740], threshold=0.001 ) == True
    assert is_positions_close_together( [59.8586, 17.6391], [54.485, 13.942], threshold=0.001 ) == False

def test_new_position_func():
    assert is_positions_close_together([0,0],[0,0]) == True
    assert is_positions_close_together([0,0],[15,0]) == False
    assert is_positions_close_together([0,0],[0,15]) == False

# -------------------- AI generated tests -----------------------

@pytest.mark.parametrize(
    "pos2, expected",
    [
        pytest.param([0.0009, 0.0009], True, id="bada_innanfor"),
        pytest.param([0.001, 0.0], True, id="latitud_pa_gransen"),
        pytest.param([0.0, 0.001], True, id="longitud_pa_gransen"),
        pytest.param([0.0011, 0.0], False, id="bara_latitud_utanfor"),
        pytest.param([0.0, 0.0011], False, id="bara_longitud_utanfor"),
    ],
)
def test_positionsgrans_och_symmetri(pos2, expected):
    pos1 = [0.0, 0.0]

    assert is_positions_close_together(
        pos1, pos2, threshold=0.001
    ) is expected

    assert is_positions_close_together(
        pos2, pos1, threshold=0.001
    ) is expected

@pytest.mark.parametrize(
    "invalid_position",
    [
        pytest.param([], id="inga_koordinater"),
        pytest.param([59.3291], id="en_koordinat"),
        pytest.param([59.3291, 18.0681, 10.0], id="tre_koordinater"),
    ],
)
def test_position_med_fel_antal_koordinater(invalid_position):
    valid_position = [59.3291, 18.0681]

    with pytest.raises(ValueError):
        is_positions_close_together(invalid_position, valid_position)

    with pytest.raises(ValueError):
        is_positions_close_together(valid_position, invalid_position)

def test_endast_en_dator_returneras(tmp_path):
    data = {
        "ensam": [59.3291, 18.0681],
    }

    fil = tmp_path / "en_dator.json"
    fil.write_text(json.dumps(data), encoding="utf-8")

    assert solution(str(fil)) == "ensam"

def test_gemensam_granne_och_en_isolerad(tmp_path):
    data = {
        "a": [59.0, 18.0],
        "b": [59.0008, 18.0],
        "c": [58.9992, 18.0],
        "d": [55.6, 13.0],
    }

    fil = tmp_path / "gemensam_granne.json"
    fil.write_text(json.dumps(data), encoding="utf-8")

    assert solution(str(fil)) == "d"

if __name__ == "__main__":
    try:
        result = solution("tracking.json")
        print( result )
    except FileNotFoundError as e:
        print( e )