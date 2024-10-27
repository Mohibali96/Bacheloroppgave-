import SoccerNet
from SoccerNet.Downloader import SoccerNetDownloader

# Initialize SoccerNetDownloader with the specified local directory
mySoccerNetDownloader = SoccerNetDownloader(LocalDirectory="C:\\SoccerNetData")

# Set the password for downloading videos
mySoccerNetDownloader.password = "s0cc3rn3t"

# Download the specified video files for the given splits
mySoccerNetDownloader.downloadGames(files=["1_720p.mkv", "2_720p.mkv"], split=["train", "valid", "test", "challenge"])
mySoccerNetDownloader.downloadGames(files=["1_224p.mkv", "2_224p.mkv"], split=["train", "valid", "test", "challenge"])