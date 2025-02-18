Instrukser til kjøring av scripter : 
1 - Åpne terminal og skriv pip install soccernet
2 - pip install openai-whisper
3 - pip install elasticsearch==7.10.1
4 - pip install ffmpeg
5 - pip install numpy==1.23.5
6 - pip install flask
7 - pip install psutil
8 - Åpne filutforsker, åpne «C-disken» og lag en mappe som heter «SoccerNetData».
9 - Gå tilbake til terminal i VS Code.
10 - Skriv python downloadVideo.py (Dette tar lang tid, anbefaler minst å laste ned kamper fra 2014-2015).
11 - Åpne nettleser og gå inn på: https://www.gyan.dev/ffmpeg/builds/
12 - Bla ned til «release build» og last ned zip under «latest release»
13 - Unzip FFmpeg-zip og lagre denne i «C-disken», samme sted som «SoccerNetData»
14 - Pass på å endre FFMPEG_PATH i «convert.py» filen slik at navn på mappe og filstruktur stemmer overens.
15 - Åpne søkefeltet i windows og søk etter miljø og velg «Rediger miljøvariabler for kontoen din».
16 - Trykk på «Path» slik at den blir markert og trykk rediger.
17 - Trykk «Bla gjennom».
18 - Lokaliser FFmpeg som du unzippet under «C-disken», under FFmpeg mappen velger du «bin» og trykker «Ok» på alle åpne vinduer.
19 - Restart maskin.
20 - Åpne VS Code terminal og skriv python convert.py for å konvertere videofiler.
21 - Ønsker du å bruke ferdig transkriberte whisper-filer fra SoccerNet, kan du hoppe over punkt 22. Dette lastes ned fra https://github.com/SoccerNet/sn-echoes. Lagre denne mappen under «SoccerNetData» mappen i «C-disken».
Vil du generere egne transkripsjoner kan du hoppe over dette punktet og gå videre
til 22.
22 - python transcribe_videos.py
23 - Åpne nettleser og last ned docker fra: https://docker.com/
24 - Restart maskin etter installasjon av docker og start docker programmet.
25 - Åpne terminal i VS Code og skriv denne kommandoen: 
docker run -d --name elasticsearch -p 9200:9200 -e "discovery.type=single-node" -e "xpack.security.enabled=false " docker.elastic.co/elasticsearch/elasticsearch:7.10.1
26 - Skriv python JsonMapper.py (Endre lokasjon på «commentary_base_dir» om du ønsker å bruke ferdig transkript fra github).
27 - python Database_Creator.py
28 - python indexer.py
29 - python app.py Hold inne “Ctrl” og venstre klikke på lenken for å vise programmet i nettleser.
