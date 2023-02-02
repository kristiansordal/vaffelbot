# Vaffelbot

Vaffelbot er en Discord-bot skrevet i Python som erstatter den fysiske køen på InformatikkOrakel hver vaffeltorsdag.


## Installasjon

1. Installer Python (3.6 eller nyere).

2. Klon eller last ned dette repositoryet.

3. Opprett en ny fil ved navn .env, og legg inn bot-en sin token:
```
TOKEN=LIM_INN_TOKEN_HER
```

4. Åpne en terminal i samme mappe, og installer nødvendige biblioteker med kommandoen:
```
pip install -r requirements.txt
```

5. Kjør følgende kommando i terminalen for å starte bot-en:
```
python main.py
```


## Bruk

Bot-en bruker `$` som prefix for kommandoer.

Følgende kommandoer kan brukes av alle:
* $vaffel - Legger brukeren til i køen for vaffelbestilling
* $kø - Viser hvilken plass brukeren har i køen. Viser antall personer som er i køen ellers

Rollen 'Orakel' har i tillegg tilgang til følgende kommandoer:
* $vaffelstart - Åpner for vaffelbestilling
* $vaffelstopp - Stenger vaffelbestilling. $stekt kommandoen kan fremdeles brukes
* $stekt - Melder om at nye vaffler er stekt. Gir beskjed til de neste personene i køen
