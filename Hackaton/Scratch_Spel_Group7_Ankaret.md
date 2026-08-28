# Game
## Ansvarsområde: 
Johan Persson - Projektledare  
Hugo Wittemyr - Game logic / Game State / Scratch xpert  
Skandar Ben Samir Chouchane - Sound  
Oscar Stenberg  - Game logic / Game control  
Marcus Karlsson -  Game logic / Game control  
Gabriel Svedar - Sprites / Graphics / Assets  

## Quick info
Typ av spel: Survival, Arena  
Features: Tre liv, Kill counter, Game Timer
## Win conditions
Målet är att överleva så länge som möjligt.
## Kontroller - "Hugo, Oscar & Marcus"
- [x] AWSD för att flytta på spelaren.
- [x] Muspekare för att sikta,
### Collision
- [X] Väggar / Boundries
- [X] Fienden
- [X] Projektiler

## Objekt uppbyggnadsförslag
### Char_obj
Health, Speed
### Player
PowerUps, Damage
### Enemy
Damage

# GameLoop:
Spelet börjar med att spelaren kommer in i en arena, fiender spawnar runt om.  
Man bekämpar fienderna genom att skjuta med diverse vapen.  
Spelaren kan röra sig runt med WASD och sikta med musen, vänsterklick skjuter en projektil.  
Högerklick är "special ability", consumable pickup, granat, limited amount.
## LJUD:  "Skandar"
- [x] Projectile hit wall
- [x] Player hit
- [x] Enemy hit
- [x] Player death
- [x] Enemy death
- [x] Weapon fired
- [x] Game Over
- [x] (Footsteps)
- [x] Next level, difficulty up.

# Ej implementerat
## Breakpoints:
Fienderna blir svårare efter x sekunder, ( mer liv ? )  
Fiendena blir svårare efter varje kill spelaren gör.  
Fienderna spawnar snabbare efter x sekunder  
## EXTRA features 
### Powerups  
#### Defensiva  
- Sköld  
- Extra liv? +2 (Max)?  
#### Offensiva  
- Faster attack speed (IAS) ( Permanent eller time based ?)  
- 2x Damage ( Permanent eller time based ?)  
#### Utility  
- Player Speed up ( Permanent eller time based ?)  
