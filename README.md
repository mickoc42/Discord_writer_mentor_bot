# Pisarski Mentor Bot — README
Bot Discord do organizowania treningów pisarskich: publikuje zaplanowane zadania na kanale tekstowym i oferuje prosty minutnik z powiadomieniem dźwiękowym na kanale głosowym.
## Funkcje
- Harmonogram wiadomości:
    - Wysyła o pełnych godzinach zaplanowane komunikaty z dziennymi zadaniami, oznaczając @everyone.
    - Każda pozycja może mieć własne dni tygodnia i godzinę.
    - Zapobieganie duplikatom (każda pozycja wysyłana raz dziennie).

- Komenda minutnika:
    - `!timer <minuty>` — odlicza, aktualizuje wiadomość co minutę, na końcu wysyła komunikat i odtwarza krótki dźwięk na kanale głosowym użytkownika (jeśli jest połączony).

## Wymagania
- Python 3.13+
- Virtualenv
- Biblioteki:
    - discord.py
    - python-dotenv

- FFmpeg (do odtwarzania dźwięku w kanale głosowym)
- Pliki konfiguracyjne:
    - `.env` z tokenem bota
    - `data.json` z harmonogramem
    - `beep.mp3` — krótki dźwięk powiadomienia

- Uprawnienia i intenty w Discord Developer Portal:
    - Włącz “Message Content Intent”.
    - Uprawnienia w serwerze: Send Messages, View Channels, Mention Everyone (opcjonalnie), Connect, Speak.

## Instalacja i uruchomienie
1. Sklonuj repozytorium i przejdź do katalogu projektu.
2. Utwórz i aktywuj środowisko wirtualne:
    - Linux/macOS:
        - `python3 -m venv .venv`
        - `source .venv/bin/activate`

    - Windows (PowerShell):
        - `py -m venv .venv`
        - `.venv\Scripts\Activate.ps1`

3. Zainstaluj zależności:
    - `pip install discord.py python-dotenv`

4. Przygotuj pliki:
    - Utwórz `.env` w katalogu głównym i dodaj:
        - `DISCORD_TOKEN=twój_token_bota`

    - Umieść `beep.mp3` (krótkie powiadomienie dźwiękowe) w katalogu głównym projektu.
    - Utwórz `data.json` z harmonogramem (patrz niżej).

5. Skonfiguruj kanał docelowy:
    - Zaktualizuj identyfikator kanału tekstowego w konfiguracji/stałej kanału (CHANNEL_ID) na ID Twojego kanału.

6. Uruchom bota:
    - `python main.py`

Po starcie bot utworzy plik z logami działania. `discord.log`
## Format pliku data.json (harmonogram)
- Czas jest interpretowany w strefie czasowej systemu, w formacie HH:MM (24h).
- Dni tygodnia to angielskie nazwy: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday.

Przykład:
