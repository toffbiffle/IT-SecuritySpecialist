from typing import Any
import re, csv, requests

SUSPECTS: list[str] = ["id001", "id007", "id009", "id015"]
COMPUTER: str = "makar"  # room-3-2
USER_ACCESS_URL = "https://gist.github.com/Grokzen/11ddfa83c0f0d379d33d7abbfdd1c77e"


# Classes:
class User:
    """Represent a user and their room access code.

    attribute:
        id: str         - The user's identifier, e.g "id001"
        name: str       - The user's name, e.g "Anna Andersson"
        access: str     - The room access code. Each character corresponds to
                            one unique room in floor and room number order.
                            e.g "010..." length is not limited or garanteed
    The constructor stores the supplied values without validating them.
    """

    id: str
    name: str
    access: str

    def __init__(self, id: str, name: str, access: str) -> None:
        """Initialize a user without validating the supplied values.

        input:
            id:     str - user id in format 'id000'
            name:   str - user name in format 'firstname lastname'
            access: str - user access code in format '01010...'
                            length should be the same as the number of rooms in
                            the building. Unvalidated.
        """
        self.id: str = id
        self.name: str = name
        self.access: str = access

    def __str__(self) -> str:
        """Return the user's name and id in the format 'name (id)'."""
        return f"{self.name} ({self.id})"

    def has_access(self, room: Room, rooms: list[Room]) -> bool:
        """Check whether the user has access to a room.

        Rooms are made unique by name and sorted numerically by floor and
        room number before the corresponding access character is checked.
        Only the charecter '1' grants access.

        input:
            room:  Room       - Room whose access permission is checked.
            rooms: list[Room] - All rooms in the building, in any order.
                                  Duplicate rooms could occur.

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
            # Sorting by tuple make it sort in a lexicographic order, first floor then number.
            set(rooms),
            key=lambda _room: (_room.floor, _room.number),
        )

        # If the length of the access code doesn't add up with the number of
        # unique rooms we have a major security problem.
        if len(self.access) != len(sorted_unique_rooms):
            raise ValueError("[User] Permissions data is of the wrong length.")

        # Find the correct index of room in the sorted list of unique rooms
        room_index = sorted_unique_rooms.index(room)
        return self.access[room_index] == "1"


class Room:
    """Represent a room identified by its name.

    Attributes:
        name (str):    Complete name 'room-1-2' where 1 is floor number
                        and 2 is room number
        floor (int):   The floor number extracted from the name
        number (int):  The room number extracted from the name.

    Rooms are compared and hashed by name. Do not change the name after
    using a room as a dictionary key or adding it to a set. Attribute
    immutability is not enforced.
    """

    name: str
    floor: int
    number: int

    def __init__(self, name: str) -> None:
        """Validate a room name and extract its floor and room number.

        input: name: str - A name in the format 'room-<floor>-<number>'.
                            Each numeric component must contain one or two decimal
                            digits and represent a value greater then zero.

        raise:
            ValueError: If the name has an invalid format or either numeric
                        component represents zero.
        """
        if not self.validate_name(name):
            raise ValueError("Room name is not valid.")

        self.name = name
        _, floor, number = self.name.split("-")
        self.floor = int(floor)
        self.number = int(number)

    def __str__(self) -> str:
        """Return the room's name."""
        return f"{self.name}"

    def __eq__(self, other: object) -> bool:
        """Compare this room with another object by room name.

        input: object - The object to compare with this room.

        output:
            bool: Wheater the names match when other is a Room.
            TypeError: If other is not a Room.
        """
        if not isinstance(other, Room):
            raise TypeError("[Room] Unable to compare with object.")

        # Two rooms with the same name should be considered the same room.
        return self.name == other.name

    def __hash__(self) -> int:
        """Return a hash based on the room's name."""
        return hash(self.name)

    def validate_name(self, name: str) -> bool:
        """Check the format and numeric components of a room name.

        input:  name: str - The room name to validate.
        output: bool: True if the name matches 'room-<floor>-<number>',
                        each numeric component contains one or two decimal digits,
                        and both values are greater then zero. False if the
                        format does not match.

        raise:
            ValueError: If the format matches but either numeric component
                        represents zero.
        """
        VALID_ROOM_NAME_STRUCTURE = r"^room-\d{1,2}-\d{1,2}$"

        # Validate structure of name so we can extract floor and room number from it.
        if re.fullmatch(VALID_ROOM_NAME_STRUCTURE, name) != None:
            _, floor, room_number = name.split("-")
            if int(floor) == 0 or int(room_number) == 0:
                raise ValueError(
                    "[Room] Floor or room number must be greater than zero."
                )
            return True
        else:
            return False


# Custom Exceptions
class NoUniqueCulpritError(Exception):
    """Indicate that zero or multiple suspected users have room access."""

    pass


# Functions:
def parse_users(data: object) -> list[User]:
    """Validate decoded JSON data and create a User for each entry.

    expected data format: [{id:,name:,access:}...]

    input:
        data: object - Expected to be a list of dictionaries containing
                        the keys 'id', 'name', and 'access'. All dictionary values,
                        including values of additional fields, must be strings.
                        Access codes may contain only '0' and '1'.

    output: list[User] - Users in the same order as the input entries.
                            Additional fields are ignored when creating the users.

    raise:
        TypeError:  If data is not a list.
        ValueError: If an entry is not a dictionary, a required key is missing,
                        a value is not a string, or an access code contains
                        a character other than '0' or '1'.
    """
    users: list[User] = []

    if not isinstance(data, list):
        raise TypeError("User data is of the wrong type.")

    if not all(isinstance(item, dict) for item in data):
        raise ValueError("Each user have to be of the correct type.")

    # check if id, name and access exist in the dict
    required_keys = {"id", "name", "access"}
    if not all(required_keys.issubset(item) for item in data):
        raise ValueError("Some of the required data for each user is missing.")

    # check if any fields exist outside the required ones.
    if any(set(item) - required_keys for item in data):
        raise ValueError("User data contains extra fields.")

    # check if dict.value is a string
    if not all(isinstance(value, str) for item in data for value in item.values()):
        raise ValueError("Some field has the wrong type in user data.")

    # check if dict[access] contains anything other then 0 or 1
    if not all(character in "01" for item in data for character in item["access"]):
        raise ValueError("Permission data is has the wrong value.")

    for item in data:
        users.append(User(item["id"], item["name"], item["access"]))

    return users


def load_rooms(path: str) -> dict[str, Room]:
    """Read a UTF-8 CSV and map computer names to rooms.

    input: str - Path to a CSV file containing the case-sensitive
                column names 'Room' and 'Computer' Additional
                columns are allowed.

    output: dict[str, Room] - Computer names mapped to their rooms.
                                Multiple computers may belong to the same room.

    raise:
        OSError: If the file cannot be opened or read
        UnicodeDecodeError: If the file cannot be decoded as UTF-8.
        csv.Error: If the CSV reader encounters a parsing error.
        PermissionError: If the file can't be read due to permissions.
        ValueError: if required columns or values are missing,
            a computer name occurs more than once, or a room name is invalid.
    """
    output: dict[str, Room] = {}

    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        if not {"Room", "Computer"}.issubset(reader.fieldnames or []):
            raise ValueError(f"{path}: Need to contain Room and Computer columns.")

        for row in reader:
            room_name = row["Room"]
            computer_name = row["Computer"]

            if not room_name or not computer_name:
                raise ValueError("Missing value in csv file.")

            if computer_name in output:
                raise ValueError("Duplicate computer name in csv.")

            output[computer_name] = Room(room_name)

    return output


def find_culprit(
    suspects: list[str],
    computer: str,
    users: list[User],
    computer_rooms: dict[str, Room],
) -> User:
    """Return the only suspected user with access to the computer's room.

    input:
        suspects:       list[str]       - id of the suspected users
        computer:       str             - name of the computer being investigated
        users:          list[User]      - available users and their access code.
        computer_rooms: dict[str, Room] - computer names mapped to rooms.

    output: User - The only suspected user with access to the target room.

    raise:
        ValueError - If the computer is missing from computer_rooms or a checked user's
                    access code has the wrong length.
        NoUniqueCulpritError - If zero or more then one culprit have access to the target room.
    """
    # Remove the computer names and create a list from the dict
    all_possible_rooms: list[Room] = list(computer_rooms.values())
    only_suspected_users: list[User] = [user for user in users if user.id in suspects]

    if computer not in computer_rooms:
        raise ValueError("Computer isnt a part of the data over registerd computers.")

    # Get Room from computer_rooms with the missing computers name
    room_with_missing_computer: Room = computer_rooms[computer]

    culprit: list[User] = [
        user
        for user in only_suspected_users
        if user.has_access(room_with_missing_computer, all_possible_rooms)
    ]

    if len(culprit) == 0:
        raise NoUniqueCulpritError("No suspect had access to the room.")

    if len(culprit) > 1:
        raise NoUniqueCulpritError("More then one culprit had access to the room.")

    return culprit[0]


def write_report(
    path: str,
    suspects: list,
    computer: str,
    users: list[User],
    computer_rooms: dict[str, Room],
) -> None:
    """Write a CSV report of suspected users room access.

    The file is overwritten on every execution and contains the columns
    id', 'namn', 'access' and 'status'. Status values are 'har access'
    or 'saknar access'.

    Matching users are written in suspect ID order. Suspect IDs with
    no matching user are omitted (POSSIBLE AREA OF IMPROVEMENT?). The
    report does not require a uniquely identified culprit.

    input:
        path:           str             - Where to save the report
        suspects:       list            - id of suspected users
        computer:       str             - name of the computer being investigated
        users:          list[User]      - available users and their access code
        computer_rooms: dict[str,Room]  - computer names mapped to rooms

    raise:
        OSError:    If the file cannot be opened or written.
        KeyError:   If the computer is missing and a matching user is processed.
        ValueError: If a checked user's access code has the wrong length.
    """
    room_with_missing_computer: Room = computer_rooms[computer]

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "namn", "access", "status"])

        row_to_print = []
        for user_id in suspects:
            for _user in users:
                if _user.id == user_id:
                    row_to_print.extend([_user.id, _user.name, _user.access])

                    if _user.has_access(
                        room_with_missing_computer,
                        list(computer_rooms.values()),
                    ):
                        row_to_print.append("har access")
                    else:
                        row_to_print.append("saknar access")
            writer.writerow(row_to_print)
            row_to_print = []


def fetch_all_users_data_from_url(url: str) -> object:
    """Fetch and decode JSON user data from URL with '/raw' appended

    The request uses timeout=5 and checks the HTTP status before
    decoding the response. The decoded data is not validated here.

    input: url: str - The base URL of the user data, without the '/raw' suffix.

    output: object  - The decoded JSON value, to be decoded by parse_users.

    raise:
        RuntimeError - If the requests fails or the response is not valid JSON
    """
    try:
        with requests.get(
            url + "/raw", timeout=5
        ) as r:  # Add /raw to the url to get the JSON data and not the HTML
            r.raise_for_status()
            return r.json()

    except requests.exceptions.Timeout as e:
        raise RuntimeError(f"Unable to fetch data within the Timeout limit: {e}")

    except requests.exceptions.ConnectionError as e:
        raise RuntimeError(f"Unable to connect: {e}")

    except requests.exceptions.HTTPError as e:
        if e.response is None:
            raise RuntimeError("An HTTP error occured, but no response was available.")
        status = e.response.status_code

        if status == 404:
            message = "URL to user data Not Found (HTTP 404)."
        elif status in (401, 403):
            message = (
                f"Server refused connection or acces to user data (HTTP {status})."
            )
        elif 500 <= status < 600:
            message = f"Internal server error (HTTP {status})."
        else:
            message = f"Requests failed with HTTP-status {status}."

        raise RuntimeError(message)

    except (
        requests.exceptions.MissingSchema,
        requests.exceptions.InvalidSchema,
        requests.exceptions.InvalidURL,
    ) as e:
        raise RuntimeError(f"Url is is not valid {e}.")

    except requests.exceptions.JSONDecodeError as e:
        raise RuntimeError(f"Unable to decode the JSON response: {e}.")

    except requests.exceptions.RequestException as e:
        raise RuntimeError(
            f"Unable to fetch user data due to an unexpected request error. {e}"
        )


def collect_evidence() -> dict[str, Any]:
    """Fetch and validate user data and load computer room mappings.

    User data is fetched from USER_ACCESS_URL. Room data is read from
    the local file 'rooms.csv'.

    sources:
        users           - internet: requests.get()  - fetch_user_permissions_from_url()
        rooms           - file:     rooms.csv       - load_rooms()
        suspects        - constant: hardcoded       - SUSPECTS
        computer_name   - constant: hardcoded       - COMPUTER

    output:
        data_collection: dict[str, Any] - A dict containing
            'users' as list[User] and 'rooms' as dict[str, Room]

    raise:
        RuntimeError: If fetching or decoding the user data fails.
        TypeError: If the decoded user data is not a list.
        ValueError: If user data or room data fails validation.
        OSError: If the room file cannot be opened or read.
        UnicodeDecodeError: If the room file is not valid UTF-8.
        csv.Error: If the CSV reader encounters a parsing error.

    """
    evidence_collection = {
        "suspects": SUSPECTS,
        "computer_name": COMPUTER,
        "users": [],
        "rooms": {},
    }

    evidence_collection["users"] = parse_users(
        fetch_all_users_data_from_url(USER_ACCESS_URL)
    )
    evidence_collection["rooms"] = load_rooms("rooms.csv")

    return evidence_collection


def solution() -> str:
    """Collect evidence, write the report, and return the culprit's name.

    The report is written to 'rapport.csv' before attempting to identify
    a unique culprit. SUSPECTS and COMPUTER determine the investigation.

    output: str: big_bad_evil_guy - The name of the uniquely identified culprit if applicable.

    raise:
        RuntimeError: If fetching or decoding the user data fails.
        TypeError: If the decoded user data is not a list.
        ValueError: If data validation fails, the target computer is
            missing during culprit identification, or a checked access
            code has the wrong length.
        KeyError: If report generation encounters a missing target computer.
        OSError: If an input or output file cannot be opened, read, or written.
        UnicodeDecodeError: If the room file is not valid UTF-8.
        csv.Error: If a CSV operation fails.
        NoUniqueCulpritError: If zero or multiple suspected users have
            access to the target room.
    """
    evidence = collect_evidence()

    write_report(
        "rapport.csv",
        evidence["suspects"],
        evidence["computer_name"],
        evidence["users"],
        evidence["rooms"],
    )

    big_bad_evil_guy = find_culprit(
        evidence["suspects"],
        evidence["computer_name"],
        evidence["users"],
        evidence["rooms"],
    )

    return big_bad_evil_guy.name


# Testerna ligger i test_solution.py. Kör dem med: uv run pytest

if __name__ == "__main__":
    try:
        name = solution()
    except (
        RuntimeError,
        OSError,
        ValueError,
        NoUniqueCulpritError,
        PermissionError,
    ) as e:
        print(f"[Solution] Unhandled error: {e}")
    else:
        print(name)
