def solution(path):
    """Read the logfile at the supplied path, filter it and return the unique user_ids.
    
    Filter each row according to the rules:
    First column    = day           = 14
    Second column   = hour          = from 13 to 18 inclusive
    Third column    = direction     = out
    Fourth column   = user_id

    input: relative or absolute path to the logfile
    output: list of user_id
    """

    TARGET_DAY          = 14    #int: day to look for 1-31
    TARGET_MAX_HOUR     = 18    #int: hour has to be this or below
    TARGET_MIN_HOUR     = 13    #int: hour has to be this or above
    TARGET_DIRECTION    = "out" #str: direction of access, out or in

    output = []
    with open( path, "r", encoding="utf-8" ) as f:   # read mode and encoding is default but I prefere to be explicit
        data = f.readlines()                         # read every line from the file to memory

    for row in data:
        day, hour, direction, user_id = row.strip().split(" ")      # .split() is default on whitespace but i prefere the explicity

        if (
            int( day ) == TARGET_DAY
            and TARGET_MIN_HOUR <= int( hour ) <= TARGET_MAX_HOUR   # Check so that hour is between TARGET_MIN_HOUR and TARGET_MAX_HOUR
            and direction == TARGET_DIRECTION
        ):
            if user_id not in output:                               # Do not add duplicates to the list
                output.append( user_id )

    return output

def test_solution(tmp_path):
    ids = solution("access.log")
    assert len(ids) > 0, "No ID:s returned"
    assert all(type(id) == str for id in ids), "Not a string"
    assert all(len(id) > 4 for id in ids), "ID should contain at least 4 characters"
    assert all(id.isalnum() for id in ids), "ID should only contain letters a-z or numbers"

    # Ett litet exempel med en egen testfil (tmp_path är en tillfällig mapp från pytest).
    fil = tmp_path / "exempel.log"
    fil.write_text("14 14 out id001\n14 14 in id002\n")
    assert solution(str(fil)) == ["id001"]

    # En blandad logg.
    fil = tmp_path / "blandad.log"
    fil.write_text(
        "14 12 out id010\n"
        "14 13 out id011\n"
        "14 14 in id012\n"
        "14 15 out id013\n"
        "13 15 out id014\n"
        "14 17 out id013\n"
        "1 14 out id015\n"
        "14 18 out id012\n"
        "14 19 out id016\n"
    )
    assert sorted(solution(str(fil))) == ["id011", "id012", "id013"]


# Egna tester: skriv minst tre här (se test_solution för hur man skriver en testfil).
    # En tom logg.
    fil1 = tmp_path / "empty.log"
    fil1.write_text("")
    assert solution( str( fil1 ) ) == []

    # En fil med inga träffar
    fil2 = tmp_path / "no_target.log"
    fil2.write_text(
        "10 15 out id001\n"
        "14 09 out id002\n"
        "14 15 in id003\n"
    )
    assert solution( str( fil2 ) ) == []

    # Kolla så att id inte blir sann om det är i en substring
    fil3 = tmp_path / "no_target.log"
    fil3.write_text(
        "14 15 out id010\n"
        "14 15 out id0100\n"
        "14 15 out id010\n"
    )
    assert sorted( solution( str( fil3 ) ) ) == ["id010", "id0100"]

    # Kontrollera att de 4 id som faller under dag 14, mellan 13 och 18 som lämnat kontoret.
    ids = solution("access.log")
    assert sorted( ids ) == ["id001", "id007", "id009", "id015"]