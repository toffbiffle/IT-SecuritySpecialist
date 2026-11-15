import re

class Room:
    """Represent a room in a building, each room have a name containing a floor and room number.

    Attributes:
        name (str):    Complete name 'room-1-2' where 1 is floor number and 2 is room number
        floor (int):   number representing the floor
        number (int):  number repersenting the room number
    
    The room name should not be changed after constructions, no such limits have been implemented.
    """
    name: str
    floor: int
    number: int

    def __init__(self, name: str) -> None:
        """Validate name and create a room from its name
        
        input: name: str - Room name, e.g 'room-1-2'

        raise:
            ValueError: If the name does not match the required format
        """
        if not self.validate_name(name):
            raise ValueError("Room name is not valid.")
        
        self.name = name
        _, floor, number  = self.name.split('-')
        self.floor = int( floor )
        self.number = int( number )

    def __str__(self) -> str:
        """Return the objects name."""
        return f'{self.name}'

    def __eq__(self, other: object) -> bool:
        """Compare room names, or return NotImplemented for other types."""
        if not isinstance(other, Room):
            return NotImplemented

        return self.name == other.name

    def __hash__(self) -> int:
        """Return a hash based on the room name."""
        return hash(self.name)
    
    def validate_name(self, name: str) -> bool:
        """Return if name has the correct format

        input: name: str ex. "room-1-2"
        output: bool: True if all checks is successfull. Else False
        """

        VALID_ROOM_NAME_STRUCTURE = r'^room-\d{1,2}-\d{1,2}$'

        # Validate structure and valid floor and room_numbers:
        if re.fullmatch( VALID_ROOM_NAME_STRUCTURE, name ) != None:
            _, floor, room_number = name.split("-")
            if int( floor ) <= 0 or int ( room_number ) <= 0:
                raise ValueError("[Room] Room is out of range.")
            return True
        else:
            return False