# README

## Instrukser for kjøring av script

### 1. Installer nødvendige pakker
Åpne terminal og kjør følgende kommandoer:

```sh
pip install soccernet
pip install openai-whisper
pip install elasticsearch==7.10.1
pip install ffmpeg
pip install numpy==1.23.5
pip install flask
pip install psutil
```

### 2. Opprett mapper og last ned nødvendige filer
- Åpne filutforsker og opprett en mappe kalt **SoccerNetData** i `C:\`.
- Gå tilbake til terminalen i VS Code og kjør:

```sh
python downloadVideo.py
```
*(Dette tar lang tid. Det anbefales å laste ned kamper fra 2014-2015.)*

### 3. Installer og konfigurer FFmpeg
- Åpne nettleseren og gå til: [FFmpeg Builds](https://www.gyan.dev/ffmpeg/builds/)
- Bla ned til **release build**, last ned ZIP-filen under **latest release**.
- Pakk ut ZIP-filen og lagre den i `C:\` (samme sted som `SoccerNetData`).
- Oppdater **FFMPEG_PATH** i `convert.py` slik at banen stemmer overens.

### 4. Sett miljøvariabler for FFmpeg
- Åpne Windows-søk og skriv `miljøvariabler`.
- Velg **Rediger miljøvariabler for kontoen din**.
- Marker `Path`, klikk **Rediger** → **Bla gjennom** → Velg `bin`-mappen i FFmpeg-installasjonen.
- Klikk **OK** og lukk alle vinduer.
- **Restart maskinen**.

### 5. Konverter videoene
Åpne VS Code-terminal og kjør:

```sh
python convert.py
```

### 6. Bruke ferdige transkripsjoner (valgfritt)
Hvis du vil bruke ferdig transkriberte whisper-filer fra SoccerNet:

- Last ned fra: [SoccerNet sn-echoes](https://github.com/SoccerNet/sn-echoes)
- Lagre mappen under `C:\SoccerNetData`

### 7. Generere egne transkripsjoner (valgfritt)
Kjør følgende kommando:

```sh
python transcribe_videos.py
```

### 8. Installer og kjør Docker
- Last ned og installer Docker fra: [Docker](https://docker.com/)
- **Restart maskinen etter installasjon**.
- Start Docker-programmet og kjør:

```sh
docker run -d --name elasticsearch -p 9200:9200 -e "discovery.type=single-node" -e "xpack.security.enabled=false" docker.elastic.co/elasticsearch/elasticsearch:7.10.1
```

### 9. Kjør de siste Python-skriptene
```sh
python JsonMapper.py  # Oppdater lokasjon i filen om nødvendig
python Database_Creator.py
python indexer.py
python app.py
```

Hold inne **Ctrl** og klikk på lenken for å åpne programmet i nettleseren.

