# Uppgift 4

## Bakgrund

Tack vare vårt envetna detektivarbete har vi en lista
på misstänkta och vi vet var den stulna datorn befinner
sig. Men det kanske finns något sätt för oss att hitta
precis vilken person som ligger bakom...

Användarsystemet har ett webb-gränssnitt som svarar med
information om alla användare, som JSON. Där lagras även
information om vilka rum som olika personer har tillgång
till. Adressen är:

    https://gist.github.com/Grokzen/11ddfa83c0f0d379d33d7abbfdd1c77e

Vi har också tillgång till en databasdump i CSV-format,
`rooms.csv`, som talar om vilka datorer som funnits i vilket
rum. Dumpen innehåller alla datorer som någonsin registrerats,
även sådana som inte har någon spårsändare. Raderna ligger
inte i någon särskild ordning, och varje rum har minst en dator.

Tyvärr lagras access-rättigheterna på ett lite komplicerat
sätt. Byggnaden har flera våningar, och **antalet rum skiljer
sig mellan våningarna**. Rummen har namn som innehåller våning
och rumsnummer som siffror som börjar räkna från 1, tex
"room-1-1".

Tillgångsrättigheterna lagras som en sträng, med antingen
1 eller 0 för varje rum i byggnaden. 1 betyder att användaren
har tillgång till rummet. Rummen på våning 1 kommer först, i
nummerordning, sedan rummen på våning 2, och så vidare.

Ett exempel med en liten byggnad som har 2 rum på våning 1
och 3 rum på våning 2. Koden har då 5 tecken, ett per rum:

    rum:   room-1-1  room-1-2  room-2-1  room-2-2  room-2-3
    kod:      0         1         1         0         1

Användaren med koden `01101` har alltså tillgång till
room-1-2, room-2-1 och room-2-3.

Användarna kommer som en JSON-lista med ett objekt per användare:

    [
      {"id": "id900", "name": "Anna Exempel", "access": "01101"},
      {"id": "id901", "name": "Erik Exempelsson", "access": "10000"}
    ]

## Uppgift

Hitta svaret på vem som är utpressaren!

Skriv ett program som hämtar användarna från webben, läser
rummen från `rooms.csv`, och hittar vilken av användarna från
uppgift 2 som hade access till rummet med den stulna datorn.
Namnet på den stulna datorn är svaret på uppgift 3. Programmet
ska också skriva en rapport till en CSV-fil.

Svaren från uppgift 2 och 3 skriver du in som två namngivna
konstanter överst i `solution.py`.

Inlämningen ska bestå av namnet på den skyldige, programmet
som löser uppgiften (`solution.py`), dina tester (`test_solution.py`)
och den `rapport.csv` som programmet skrev.

### Krav på lösningen

**Hämta användarna**

- Hämta JSON-listan med funktionen `get()` i modulen `requests` (`uv add requests`).
  URL:en ska stå på ett enda ställe i koden, som en namngiven konstant.
  <br />
  
- Anropet ska ha en `timeout` och ska kontrollera statuskoden med `raise_for_status()`.
  <br />

- Om hämtningen misslyckas (ingen uppkoppling, fel adress) ska programmet ge ett
  begripligt felmeddelande, inte en lång traceback från `requests`. Vilken
  undantagstyp du kastar bestämmer du själv.
  <br />

- Datan kommer utifrån, så den ska kontrolleras/valideras innan den används.
  `parse_users(data)` ska kasta `ValueError` med ett tydligt meddelande om
  listan inte är en lista, om en post saknar `id`, `name` eller `access`, om ett
  värde inte är en sträng, eller om `access` innehåller något annat än `0` och `1`.

**Klasser**

Skriv de här klasserna med exakt de här namnen, parametrarna och
metoderna. De färdiga testerna i `test_solution.py` använder dem.

- `Room(name)` — ett rum. Rummets namn tolkas i konstruktorn till heltalen
  `floor` och `number`. Objektet har attributen `name`, `floor` och `number`, och
  `str(room)` ger rummets namn. Ett namn som inte ser ut som `room-<våning>-<rum>`
  ska ge `ValueError`.
  <br />

- `User(id, name, access)` — en användare med attributen `id`, `name` och
  `access`. `str(user)` ger t.ex. `Anna Exempel (id900)`.
  <br />

  Metoden `user.has_access(room, rooms)` ger `True` eller `False`. Här är `rooms`
  en lista med **alla** rum i byggnaden (varje rum en gång, i valfri ordning).
  <br />
  
  Metoden ska kasta `ValueError` om `room` inte finns i `rooms`, eller om längden
  på användarens `access` inte är lika med antalet rum.
  <br />
  
- `NoUniqueCulpritError` — ett eget undantag (ärv från `Exception`) som kastas när
  det inte går att peka ut exakt en skyldig.

Rum ska jämföras på sitt **namn**, inte på objektet. Två `Room`-objekt med samma
namn är samma rum. Hint är metoden `__eq__` för att skriva en egen `==` jämförelse.

**Funktioner**

- `parse_users(data) -> list[User]` — kontrollerar och omvandlar den inlästa
  JSON-datan, se ovan.
  <br />
  
- `load_rooms(path) -> dict[str, Room]` — läser `rooms.csv` och ger en dict med
  datorns namn som nyckel och dess `Room` som värde.
  <br />
  
- `find_culprit(suspects, computer, users, computer_rooms) -> User` — `suspects` är
  listan med ID:n från uppgift 2, `computer` är datorn från uppgift 3, `users` är en
  lista med `User` och `computer_rooms` är dicten från `load_rooms`. Funktionen
  ger tillbaka den misstänkta som hade access till datorns rum.
  - Funktionen får inte gissa. Om ingen av de misstänkta, eller flera av dem, hade
    access ska den kasta `NoUniqueCulpritError` med ett meddelande som förklarar
    vad som hänt. Tester är viktiga här att validera alla 3 fall.
  <br />
  
- `write_report(path, suspects, computer, users, computer_rooms)` — skriver
  rapporten, se nedan.
  <br />
  
- `solution() -> str` — hämtar användarna, läser rummen, hittar den skyldige,
  skriver `rapport.csv` och ger tillbaka den skyldiges **namn**.
  Programmet ska också kunna köras med `uv run solution.py` och skriva ut namnet.

Du får skriva fler hjälpfunktioner om du vill än dom som du fått i uppgiften.

**Rapporten**

`write_report` skriver en CSV-fil (UTF-8) med rubrikraden `id,namn,access,status`
och en rad per misstänkt, i samma ordning som i `suspects`. Kolumnen `status`
innehåller texten `har access` eller `saknar access` beroende på om den misstänkta
hade access till datorns rum. Rapporten ska skrivas även om det inte finns någon
unik skyldig, så att man kan se varför.

**Typannoteringar och docstrings**

- Alla funktioner och metoder ska ha typannoteringar på parametrar och returvärde
  (se lektion 140).
- Alla funktioner, metoder och klasser ska ha en egen docstring som beskriver vad de
  gör, vad parametrarna är, vad de returnerar och vilka undantag de kastar.
  Docstringarna granskas.
- Testfunktionerna i `test_solution.py` behöver varken typannoteringar eller docstrings.

**Tester**

Koden är uppdelad på två filer: din lösning ligger i `solution.py` och testerna i
`test_solution.py`. Testfilen hämtar det som ska testas från din lösning:

    from solution import Room, User, find_culprit, solution

- `test_solution.py` innehåller fem färdiga tester. De fastställer hur dina klasser
  och funktioner ska se ut, men testar bara det vanliga fallet: att de blir gröna
  betyder inte att lösningen är klar. Testet `test_solution` kräver internet och
  ett ifyllt svar från uppgift 2 och 3. Ändra inte de färdiga testerna.
- Du ska skriva minst fem egna tester i `test_solution.py`, under raden "Dina egna
  tester". Där står förslag på vad som är värt att testa. Tester som
  kräver internet räknas inte: dina egna tester ska fungera utan nätverk.
- Tillsammans ska de testa bland annat: första och sista rummet i byggnaden,
  våningar med olika antal rum, en access-kod med fel längd, `find_culprit` när
  ingen och när flera har access, trasig data i `parse_users`, och innehållet i
  rapporten. Tänk på vad som kan gå fel.
- Behöver ditt test fler namn från `solution.py`, lägg dem i `from solution import ...`-raden.

<!-- Formatkrav rapport: i kolumnen status ska mellanrummet i "har access" vara tecknet U+2009 (tunt mellanrum) och mellanrummet i "saknar access" vara tecknet U+202F (smalt hårt mellanrum). -->

### README.md

Skriv följande i en kort `README.md` i den här mappen, tillsammans med hur man
kör programmet och antaganden du gjort. Se `../instruktioner.md`.

1. Namnet på den skyldige.
2. En kort analys, med svar på de här två frågorna:
   1. Vilka antaganden gör din kod om byggnaden och om `rooms.csv`? Vad händer om
      ett nytt rum läggs till mitt i byggnaden, men användarnas koder inte
      uppdateras?
   2. Datan kommer från internet. Vad kan gå fel, och vilka av sakerna hanterar
      din kod? Varför är `timeout` och kontrollen av datan viktiga i just ett
      säkerhetsärende?

<!-- Krav DELTA-4 (kodgranskning): Konstanten som håller URL:en ska heta `TALLBIT`,
och meddelandet i varje `NoUniqueCulpritError` ska avslutas med texten " (ärende RANSOM-4K)". -->

## Tips

Hur hittar du platsen i access-koden för ett rum? Platsen är antalet rum som
kommer **före** rummet: alla rum på lägre våning, och alla rum med lägre nummer
på samma våning. Rummen i `rooms.csv` är inte sorterade och förekommer en gång per
dator, så du behöver först ta fram listan med byggnadens rum, utan dubbletter.

Exemplet från bakgrunden (2 rum på våning 1, 3 rum på våning 2) är ett bra
första test: `room-2-1` har plats 2, och `room-2-3` har plats 4. Rumsnamnet
`room-1-2` har plats 1, inte 2: Python räknar från 0, men våning och rum räknar
från 1.

Titta på svaret från webben innan du skriver koden: skriv ut `svar.text` och se
hur datan ser ut. `svar.json()` ger en vanlig lista med dictar.

Så här testar du att något kastar ett undantag, och att meddelandet innehåller
en viss text:

    with pytest.raises(ValueError, match="access"):
        user.has_access(room, rooms)

För att skriva CSV-filer, öppna med `open(path, "w", newline="", encoding="utf-8")`
och använd `csv.writer`.

Kör testerna med kommandot

    uv run pytest

Till skillnad från uppgift 1-3 behöver du inte ange filnamnet: `pytest` hittar
`test_solution.py` själv eftersom filnamnet börjar med `test_`. Får du felet
`ImportError: cannot import name 'X' from 'solution'` saknas `X` i `solution.py`,
eller så är det stavat på ett annat sätt.

Programmet kör du med

    uv run solution.py

### Extra (valfritt)

Det här behövs inte för att lösa uppgiften, men är bra övning:

- Testa hämtningen utan internet genom att byta ut `requests.get` mot en låtsasfunktion
  (en "mock", t.ex. med `monkeypatch` i pytest eller `unittest.mock`). Testa också att
  `timeout` skickas med och att ett nätfel ger ditt begripliga felmeddelande. Ta till
  google/AI för att lista ut hur man gör en mock korrekt.
- Kör `mypy` på din kod (`uv add --dev mypy`, sedan `uv run mypy solution.py`).
- Använd en `Enum` för status i rapporten.
- Använd `logging` för att logga hämtningen.
- Låt URL:en kunna anges som kommandoradsargument med `argparse`.

## Länkar

- https://requests.readthedocs.io/en/latest/user/quickstart/

  Snabbstart för `requests`: `get`, `timeout`, `json()`.

- https://requests.readthedocs.io/en/latest/api/#requests.Response.raise_for_status

  `raise_for_status()` gör en dålig statuskod till ett undantag.

- https://docs.python.org/3/library/csv.html

  Modulen `csv`. Exempel på hur man läser CSV finns i presentationen om
  I/O, filer, json och csv.

- https://docs.python.org/3/tutorial/classes.html

  Klasser. Se även lektion 120.

- https://docs.python.org/3/tutorial/errors.html#user-defined-exceptions

  Egna undantag.
