# Uppgift 4
## Result
The only suspect that had access to the room with the
now missing computer was: Robert Bennett

## How to run:
Run tests: uv run pytest -vv
Run solution: 
	uv sync
	uv run solution.py

## Assumptions
- **ERROR MESSAGES ARE INTENTIONALLY GENERIC TO AVOID EXPOSING INTERNAL DETAILS.**
- Supplied data is correct
- Room names never change during the execution of the program
- The supplied CSV has the structure Room,Computer and not the 
	other way around
- The access code for each user has the same length as available 
	rooms with computers in the building

## Analysis
AI summerized:

1. 
	Min kod förutsätter att rooms.csv innehåller alla rum i byggnaden som har minst en dator. Flera datorer kan finnas i samma rum, så koden tar bort dubbletter innan behörigheterna kontrolleras. Rummen sorteras numeriskt efter våning och sedan rumsnummer. Det innebär att våningarna inte behöver ha lika många rum och att CSV-raderna inte behöver ligga i sorterad ordning. Rumsnamnen ska följa formatet `room-<våning>-<rum>`, med värden från 1 till 99.
	
	<br />Koden förutsätter också att datornamnen identifierar datorerna entydigt och att CSV-filen har fungerande Room- och Computer-kolumner.

	<br />Behörighetskoderna måste motsvara exakt samma rumsuppsättning och sorteringsordning som CSV-datan. Om ett nytt rum läggs in i CSV-filen men användarnas koder inte uppdateras blir antalet unika rum större än kodernas längd. has_access() upptäcker då längdskillnaden och kastar ValueError, så programmet avbryter i stället för att använda felaktiga positioner.

	<br />Om längdkontrollen saknades skulle ett nytt rum mitt i sorteringsordningen förskjuta positionerna för efterföljande rum. Behörigheter skulle då kunna kopplas till fel rum. Längdkontrollen upptäcker däremot inte alla förändringar: om exempelvis ett rum tas bort och ett annat läggs till kan antalet rum vara oförändrat trots att kopplingen är fel. Om det nya rummet inte registreras i CSV-filen kan koden inte heller upptäcka att byggnaden har förändrats.
<br />
2. 
	Hämtningen kan misslyckas på grund av anslutningsproblem, en felaktig URL, långsam server, nekad åtkomst eller serverfel. Servern 	kan också svara med innehåll som inte är giltig JSON. Min hämtningsfunktion hanterar dessa fel genom att fånga relevanta undantag 	från requests och kasta RuntimeError med ett förklarande meddelande. Programmets startpunkt fångar dessa fel och skriver ut 		meddelandet utan en lång traceback.

	<br />Även giltig JSON kan innehålla felaktiga användaruppgifter. Därför kontrollerar parse_users() att datan är en lista, att varje post är en dictionary, att id, name och access finns och att värdena är strängar. Funktionen kontrollerar också att behörighetskoderna bara innehåller 0 och 1. När en användares behörighet kontrolleras verifierar has_access() dessutom att kodens längd motsvarar antalet unika rum.

	<br />Timeout är viktig för att en långsam eller otillgänglig server inte ska kunna lämna programmet väntande obegränsat. Koden använder timeout=5; detta ska dock inte beskrivas som en garanterad totalgräns på fem sekunder för hela hämtningen.

	<br />Datakontrollen är särskilt viktig i ett säkerhetsärende eftersom felaktigt underlag kan leda till att fel person pekas ut eller att någon felaktigt frias. Programmet ska därför avbryta när det upptäcker fel, inte tolka trasig information som en vanlig nekad behörighet. find_culprit() kräver dessutom exakt en matchning och kastar ett undantag vid noll eller flera möjliga skyldiga.

	Kontrollerna garanterar däremot inte att informationen är sann eller aktuell. En manipulerad behörighetskod med rätt längd och enbart tillåtna tecken passerar valideringen. Koden kontrollerar alltså format och viss intern överensstämmelse, men bevisar inte att källdatan är korrekt.