"""Tester för uppgift 4. Kör dem från den här mappen med: uv run pytest"""

import csv, pytest

# Det som testas hämtas från din lösning i solution.py.
from solution import Room, User, NoUniqueCulpritError, find_culprit, solution, parse_users, write_report

# Behöver dina egna tester fler namn från solution.py? Lägg till dem i raden ovan,
# t.ex. NoUniqueCulpritError, parse_users, load_rooms eller write_report.
# Använder du pytest.raises: skriv "import pytest" här också.


# En liten exempelbyggnad som testerna använder: 2 rum på våning 1 och 3 rum på
# våning 2. Du får använda hjälpfunktionerna i dina egna tester också.
def exempelrum():
    return [
        Room("room-2-2"),
        Room("room-1-1"),
        Room("room-2-3"),
        Room("room-1-2"),
        Room("room-2-1"),
    ]


def exempelanvandare():
    return [
        User("id1", "Anna", "01000"),
        User("id2", "Bo", "00010"),
        User("id3", "Cia", "00100"),
        User("id4", "Dan", "01000"),
    ]


def exempeldatorer():
    return {
        "pc-c": Room("room-2-1"),
        "pc-a": Room("room-1-1"),
        "pc-e": Room("room-2-3"),
        "pc-b": Room("room-1-2"),
        "pc-d": Room("room-2-2"),
    }


# Färdiga tester. De fastställer hur dina klasser och funktioner ska se ut, och
# testar bara det vanliga fallet. Att de blir gröna betyder inte att lösningen är klar.


def test_room():
    room = Room("room-2-3")
    assert room.name == "room-2-3"
    assert room.floor == 2
    assert room.number == 3
    assert str(room) == "room-2-3"


def test_user():
    user = User("id900", "Anna Exempel", "01101")
    assert user.id == "id900"
    assert user.name == "Anna Exempel"
    assert user.access == "01101"
    assert str(user) == "Anna Exempel (id900)"


def test_has_access():
    # Rummen skickas in i blandad ordning: metoden får inte lita på ordningen.
    rooms = exempelrum()
    user = User("id900", "Anna Exempel", "01101")
    assert user.has_access(Room("room-1-2"), rooms) is True
    assert user.has_access(Room("room-2-2"), rooms) is False
    assert user.has_access(Room("room-2-3"), rooms) is True


def test_find_culprit():
    # pc-d står i room-2-2 (plats 3): bara id2 har en etta där.
    skyldig = find_culprit(["id1", "id2", "id3"], "pc-d", exempelanvandare(), exempeldatorer())
    assert skyldig.name == "Bo"


def test_solution():
    # Kräver internet, och att SUSPECTS och COMPUTER är ifyllda i solution.py.
    namn = solution()
    assert type(namn) == str, "solution() should return a string"
    assert len(namn) > 0, "solution() should return a name"

    with open("rapport.csv", newline="", encoding="utf-8") as fil:
        rader = list(csv.reader(fil))
    assert rader[0] == ["id", "namn", "access", "status"]
    assert len(rader) > 1, "rapport.csv should have one row per suspect"

# ---------------------------------------------------------------------------
# Dina egna tester - skriv minst fem här under.
#
# Varje test är en egen funktion vars namn börjar med test_. Fem tester är fem nya
# funktioner, inte fem extra assert-rader. Dina tester ska fungera utan internet.
#
# Förslag (välj själv, och hitta gärna på fler):
#
#   has_access     - första och sista rummet i byggnaden
#   has_access     - våningar med olika antal rum (t.ex. 1, 3 och 2 rum)
#   has_access     - ValueError när access-koden har fel längd
#   has_access     - ValueError när rummet inte finns i byggnaden
#   Room           - ValueError när rumsnamnet inte ser ut som room-<våning>-<rum>
#   parse_users    - trasig data ger ValueError (saknad nyckel, fel typ, tecken
#                    som inte är 0 eller 1, något annat än en lista)
#   find_culprit   - ingen träff ger NoUniqueCulpritError
#   find_culprit   - flera träffar ger NoUniqueCulpritError
#   load_rooms     - läs en liten CSV-fil som du skriver med tmp_path
#   write_report   - rubrikraden, ordningen på raderna och texten i status
#
# Tips:
#   with pytest.raises(ValueError, match="access"):   # kräver "import pytest"
#       ...
#   def test_load_rooms(tmp_path):                    # tmp_path är en tillfällig mapp
#       fil = tmp_path / "rooms.csv"
#       fil.write_text("Room,Computer\n...")
# ---------------------------------------------------------------------------

# User added tests
# Room constructor raises ValueError if the name fail the structure constraint.
@pytest.mark.parametrize(
    "room_name",
    [
        "zoom-1-1",      # Wrong name
        "room-1-134",    # To high number in room number
        "room-122-2",    # To many floors
    ],
)
def test_USER_room_constructor_wrong_structure(room_name):
    with pytest.raises(ValueError):
        Room(room_name)

# test extra fields in user data, raise ValueError
def test_USER_parse_users_extra_fields_in_data():
    user = [{"id":"id001", "name":"Anna", "access":"01", "give_unlimited_access":"1"}]

    with pytest.raises(ValueError):
        parse_users(user)

def test_USER_str_returns_user_name_with_id(capsys):
    user = User( "id001", "Anna Andersson", "01010" )

    print( user )
    output = capsys.readouterr().out

    assert str( user ) == "Anna Andersson (id001)"
    assert output == "Anna Andersson (id001)\n"


# AI generated tests with uppgift.md as source.
@pytest.mark.parametrize(
    "access, room_name",
    [
        ("01", "room-1-1"),      # För kort kod: tre rum.
        ("0101", "room-1-1"),    # För lång kod: tre rum.
        ("010", "room-2-2"),     # Rummet finns inte i byggnaden.
    ],
)
def test_AI_has_access_rejects_invalid_input(access, room_name):
    rooms = [
        Room("room-2-1"),
        Room("room-1-2"),
        Room("room-1-1"),
    ]
    user = User("id1", "Anna", access)

    with pytest.raises(ValueError):
        user.has_access(Room(room_name), rooms)


@pytest.mark.parametrize(
    "data",
    [
        ["not a user object"],
        [{"name": "Anna", "access": "01"}],
        [{"id": "id1", "access": "01"}],
        [{"id": "id1", "name": "Anna"}],
        [{"id": 123, "name": "Anna", "access": "01"}],
        [{"id": "id1", "name": None, "access": "01"}],
        [{"id": "id1", "name": "Anna", "access": 1}],
        [{"id": "id1", "name": "Anna", "access": "012"}],
    ],
)
def test_AI_parse_users_rejects_invalid_data(data):
    with pytest.raises(ValueError):
        parse_users(data)

@pytest.mark.parametrize(
    "data",
    [
        None,
        {"id": "id1", "name": "Anna", "access": "01"},
    ],
)
def test_AI_parse_users_rejects_typeerror_data(data):
    with pytest.raises(TypeError):
        parse_users(data)


def test_AI_find_culprit_raises_when_no_suspect_has_access():
    computer_rooms = {"pc-a": Room("room-1-1")}
    users = [
        User("id1", "Anna", "0"),
        User("id2", "Bo", "0"),
        User("id3", "Cia", "1"),  # Has access but is not among the suspects
    ]

    with pytest.raises(NoUniqueCulpritError):
        find_culprit(
            ["id1", "id2"],
            "pc-a",
            users,
            computer_rooms,
        )


def test_AI_find_culprit_raises_when_multiple_suspects_have_access():
    computer_rooms = {"pc-a": Room("room-1-1")}
    users = [
        User("id1", "Anna", "1"),
        User("id2", "Bo", "1"),
    ]

    with pytest.raises(NoUniqueCulpritError):
        find_culprit(
            ["id1", "id2"],
            "pc-a",
            users,
            computer_rooms,
        )


def test_AI_write_report_preserves_suspect_order_and_access_status(tmp_path):
    path = tmp_path / "rapport.csv"

    computer_rooms = {
        "target-pc": Room("room-2-1"),
        "other-pc": Room("room-1-1"),
        "extra-pc": Room("room-2-1"),
    }
    users = [
        User("id1", "Åsa", "01"),
        User("id2", "Bertil", "10"),
        User("id3", "Örjan", "11"),
    ]
    suspects = ["id3", "id2", "id1"]

    write_report(
        str(path),
        suspects,
        "target-pc",
        users,
        computer_rooms,
    )

    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    assert rows == [
        {
            "id": "id3",
            "namn": "Örjan",
            "access": "11",
            "status": "har access",
        },
        {
            "id": "id2",
            "namn": "Bertil",
            "access": "10",
            "status": "saknar access",
        },
        {
            "id": "id1",
            "namn": "Åsa",
            "access": "01",
            "status": "har access",
        },
    ]