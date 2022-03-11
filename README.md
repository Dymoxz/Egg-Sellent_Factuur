
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
> Volg voor de zekerheid de stappen in [Bugs](#Bugs)

## Gebruik

> 1. Start "AutoFactuur.exe"
> 2. Vul alle gegevens in (Het inloggen duurt ± 45 seconden, als het programma crashed na deze tijd is waarschijnlijk het  wachtwoord verkeerd ingevuld)
> 3. Het gegenereerde factuur staat in "./Facturen"

### Voorbeeld:

![eggVoorbeel](https://user-images.githubusercontent.com/82333980/157862923-fcc18eb8-ef77-4a1f-8231-dc127167682d.png)
![rsz_1rsz_1week-10](https://user-images.githubusercontent.com/82333980/157864918-4daeed5e-25fc-4d98-be0c-a07633445847.jpg)



## Bugs
> Als de console gelijk crashed ligt het waarschijnlijk aan "chromedriver.exe", om dit te voorkomen / op te lossen volg de volgende stappen:
> 1. Download van [ChromeDriver - WebDriver for Chrome (chromium.org)](https://chromedriver.chromium.org/) de versie die overeen komt met uw versie van chrome
> 2. Vervang de huidige chromedriver.exe (./Scripts/chromedriver.exe) met het nieuwe gedownloadde bestand

## Contributie
> Stuur mij een bericht of maak een pull request

## TO DO
> 1. Er voor zorgen dat je je account op kan slaan, i.p.v. elke keer in moeten voeren
> 2. Mogelijk meerdere accounts op kunnen slaan(?)
> 3. Heel misschien een web app maken

## Licentie
[MIT](https://choosealicense.com/licenses/mit/)
