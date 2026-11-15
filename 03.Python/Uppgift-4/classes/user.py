from .room import Room

class User:
    """Represent a user with id, name, access and which rooms it can access
    
    attribute:
        id: str - e.g "id001"
        name: str - e.g "Anna Andersson"
        access: str - e.g "010..." length is not limited or garanteed
    """
    id: str
    name: str
    access: str

    def __init__(self, id: str, name: str, access: str) -> None:
        """Store the users id, name and access code without validation."""

        self.id: str = id
        self.name: str = name
        self.access: str = access

    def __str__(self) -> str:
        """Return the users name and id"""
        return f'{self.name} ({self.id})'

    def has_access(self, room: Room, rooms: list[Room]) -> bool:
        """Check access to a room using the buildings room ordering

        input:
            room:  Room       - Room whose permission should be checked.
            rooms: list[Room] - All rooms in the building, unsorted
                                  Duplicate rooms could occur

        output:
            True  - If user has access to room
            False - If user does not have access to room
            
        raise:
            ValueError - If room doesnt exist in rooms
            ValueError - If user access is shorter or 
                            longer then the number of rooms
        """
        if room not in rooms:
            raise ValueError("[User] Room is not a part of the bulding.")

        # Sort rooms into the correct order by floor and then number
        sorted_unique_rooms = sorted(
            set( rooms ), 
            key=lambda _room: (
                _room.floor, 
                _room.number
            )
        )

        if len(self.access) != len(sorted_unique_rooms):
            raise ValueError("[User] Malformed permissions data.")
        
        room_index = sorted_unique_rooms.index( room )
        return self.access[room_index] == "1"