# Amstelhaege
Dicht bij Ouderkerk aan de Amstel wordt een nieuwe wijk gebouwd. De wijk zal bestaande uit vrijstaande huizen en oppervlakte water. De gemeente overweegt drie varianten van de wijk: één met 20 huizen, één met 40 huizen en één met 60 huizen. Een huis is meer waard, wanneer hij meer vrijstand heeft. Er zijn verschillende typen huizen (eengezinswoning, bungalow en maison) met verschillende hoeveelheden verplichte vrijstand en verschillende rekenpercentages. Verder zijn er nog enkele restricties:
-  Een huis mag niet op water staan, maar zijn vrijstand wel.
-  De verplichte vrijstand moet binnen de kaart vallen. Dit geldt niet voor extra vrijstand. 
Het doel van het probleem is om een valide indeling van de wijk te vinden die een zo hoog mogelijke waarde oplevert. 

## Vereisten
De codebase is geschreven in Python 3.7. Benodigde packages voor het runnen van de code staan vermeld in requirement.txt. Deze kunnen in één keer worden geinstalleerd aan de hand van het volgende command:

`pip install -r requirements.txt`

## Gebruik
De code kan worden gerund door het aanroepen van een command met de volgende structuur:

`python main.py {map_name} {quantity} {algorithm}`

- map_name -> dit betreft welke kaart er wordt gebruikt, wat de ligging van het water bepaalt. Opties zijn: wijk_1, wijk_2 of wijk_3.
- quantity -> dit betreft hoeveel huizen zullen worden geplaats in de wijk. Opties zijn: 20, 40 of 60.
- algorithm -> dit betreft welk algoritme je wilt runnen. Opties zijn: random/r, greedy/gr, random_hill_climber/r_hc en greedy_hill_climber/gr_hc. 
  
  Afhankelijk van het gekozen algoritme kan via een prompt worden gevraagd naar overige parameters.
  - Random: het aantal iteraties voor het runnen van het algoritme.
  - Greedy: het greedy type (random of strategy). Bij random zal het eerste huis op een random plek in de wijk worden geplaatst en bij strategy wordt geprobeerd het eerste huis in een van de hoeken van de wijk te plaatsen.
  - Hillclimber: het hillclimber type (rotation of switch). Rotation probeert per iteratie een huis om te draaien en switch probeert per iteratie twee verschillende type huizen om te wisselen.

## Structuur
De volgende lijst beschrijft de belangrijkste mappen en files van het project:
- /code: bevat alle code van het project
  - /code/classes: bevat code voor de benodigde classes voor de case (grid, house, water)
  - /code/algorithms: bevat code voor de gebruikte algoritmes (randomize, greedy, hillclimber)
  - /code/visualization: bevat code voor het maken van visualisatie van de wijk en andere grafieken met matplotlib 
- /data: bevat alle input en output data
  - /data/output: bevat de geproduceerde visualisaties en csv-bestanden voor de verschillende wijken
  - /data/wijken: bevat databestanden voor de verschillende wijken die nodig zijn voor visualiseren van de wijk
  
## Auteurs
- Seike Appold
- Fleur Tervoort
- Anne Zonneveld
