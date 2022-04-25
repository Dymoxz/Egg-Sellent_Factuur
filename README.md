
# Egg-sellent Auto Factuur

![image](https://user-images.githubusercontent.com/82333980/157761532-f301d2e4-6c8f-4609-a7d8-0232f05a7f86.png)  


>Egg-Sellent Auto Factuur is een python programma om automatisch een factuur voor Egg-Sellent te genereren

## Installatie

>1. Open ./Data/info.json
>2. Pas de onderstaande gegevens
```json
{
    "name": "Naam Achternaam",
    "adress": "Straat 69",
    "postcode/wp": "0000AA Stad",
    "rekening": "NL00BANK1234567890"
}
```
> V̶o̶l̶g̶ ̶v̶o̶o̶r̶ ̶d̶e̶ ̶z̶e̶k̶e̶r̶h̶e̶i̶d̶ ̶d̶e̶ ̶s̶t̶a̶p̶p̶e̶n̶ ̶i̶n̶ [B̶u̶g̶s̶](#Bugs)
> Het probleem in [Bugs](#Bugs) is hoogstwaarschijnlijk gefixed

## Gebruik
> 1. Zorg er voor dat je internet aan staat
> 2. Start "AutoFactuur.exe"
> 3. Vul alle gegevens in (Het ophalen van de transacties duurt ± 15 seconden (afhankelijk van het aantal transacties kan dit langer duren), als het programma blijft hangen na het inloggen is waarschijnlijk het  wachtwoord verkeerd ingevuld)
> 4. Het gegenereerde factuur staat in "./Facturen"

### Voorbeeld:

![image](https://user-images.githubusercontent.com/82333980/162535510-130fee31-3702-468d-919c-90c4f7433e4e.png)
![rsz_1rsz_2week-10](https://user-images.githubusercontent.com/82333980/158628757-2e216b8e-33e9-40a7-842e-087f415324c9.jpg)


## Bugs
> Als de console gelijk crashed ligt het waarschijnlijk aan "chromedriver.exe", om dit te voorkomen / op te lossen volg de volgende stappen:
> 1. Download van [ChromeDriver - WebDriver for Chrome (chromium.org)](https://chromedriver.chromium.org/) de versie die overeen komt met uw versie van chrome
> 2. Vervang de huidige chromedriver.exe (./Scripts/chromedriver.exe) met het nieuwe gedownloadde bestand

## Contributie
> Stuur mij een bericht of maak een pull request

## TO DO
> 1. Omzetten in een webapp
