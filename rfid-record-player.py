import os
import json
import mfrc522
import random
from time import sleep
import RPi.GPIO as GPIO
import spotipy
from spotipy.oauth2 import SpotifyOAuth


# Create an object of the MFRC522 class
mfrc522 = mfrc522.MFRC522()
DEVICE_ID = "DEVICE_ID"
CLIENT_ID = "CLIENT_ID"
CLIENT_SECRET = "CLIENT_SECRET"
REDIRECT_URI = "http://localhost:8888/callback"
TOKEN_FILE = "token.json"
scope = "user-read-playback-state user-modify-playback-state"

# Writing to NFC tags is limiting. We will use self defined album "codes" to reference Spotify URLs.
albumUrlDict = [
    {
        "album": "damn",
        "url": "https://open.spotify.com/album/4eLPsYPBmXABThSJ821sqY?si=ffb28ac0e5ae4db6",
    },
    {
        "album": "tpab",
        "url": "https://open.spotify.com/album/7ycBtnsMtyVbbwTfJwRjSP?si=99556104b50c48b9",
    },
    {
        "album": "daft-ram",
        "url": "https://open.spotify.com/album/4m2880jivSbbyEGAKfITCa?si=e6742cdd5ce744f8",
    },
    {
        "album": "minecraft",
        "url": "https://open.spotify.com/album/3Gt7rOjcZQoHCfnKl5AkK7?si=hiTnfXtPSRC_8enDgg1vxw",
    },
    {
        "album": "sams-town",
        "url": "https://open.spotify.com/album/4o3RJndRhHxkieQzQGhmbw?si=c475fc9e81a74923",
    },
    {
        "album": "maad-city",
        "url": "https://open.spotify.com/album/3DGQ1iZ9XKUQxAUWjfC34w?si=rgABcs8sQyeZVbe5NFdobg",
    },
    {
        "album": "dualipa",
        "url": "https://open.spotify.com/album/1Mo92916G2mmG7ajpmSVrc?si=LpgLdRBgRAaBfgklPob1_w",
    },
]


def parse_uri_from_spotify_url(url):
    split_url = url.split("https://open.spotify.com/album/")[1]
    split_url = split_url.split("?si=")[0]
    return split_url


def get_token():
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as file:
            token_info = json.load(file)
        return token_info
    else:
        auth_url = sp_oauth.get_authorize_url()
        print(
            f"Navigate to the following URL and authorize the application: {auth_url}"
        )
        response = input(
            "You're going to see an error screen. THAT'S GOOD! Paste the full URL of the error screen here: "
        )
        code = sp_oauth.parse_response_code(response)
        token_info = sp_oauth.get_access_token(code)
        with open(TOKEN_FILE, "w") as file:
            json.dump(token_info, file)
        return token_info


def refresh_token(token_info):
    token_info = sp_oauth.refresh_access_token(token_info["refresh_token"])
    with open(TOKEN_FILE, "w") as file:
        json.dump(token_info, file)
    return token_info


sp_oauth = SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=scope,
)

token = get_token()

if sp_oauth.is_token_expired(token):
    token = refresh_token(token)

sp = spotipy.Spotify(auth=token["access_token"])


# Main function
def main():
    currentAlbum = ""
    print("Ready to scan!")
    while True:
        try:
            # Scan for tags
            (status, TagType) = mfrc522.MFRC522_Request(mfrc522.PICC_REQIDL)

            # If a tag is found
            if status == mfrc522.MI_OK:
                # Get the UID of the tag
                (status, uid) = mfrc522.MFRC522_Anticoll()

                # If the UID is successfully obtained
                if status == mfrc522.MI_OK:
                    # Select the tag
                    mfrc522.MFRC522_SelectTag(uid)

                    # Read data from the tag
                    data = [
                        elem for index in [6] for elem in mfrc522.MFRC522_Read(index)
                    ]
                    result = "".join([chr(charcode) for charcode in data])
                    print("Searching for", result)
                    if "shuffle" in result:
                        print("Shuffling...\n")
                        numberOfSongsInAlbum = sp.album_tracks(
                            currentAlbum, limit=50, offset=0
                        )["total"]
                        randomTrackNumber = random.randint(0, numberOfSongsInAlbum - 1)
                        sp.start_playback(
                            device_id=DEVICE_ID,
                            context_uri="spotify:album:" + currentAlbum,
                            offset={"position": randomTrackNumber},
                        )
                    for album in albumUrlDict:
                        if album["album"] in result:
                            if currentAlbum == album["url"]:
                                print("Album already playing\n")
                                break
                            currentAlbum = album["url"]
                            print("Starting to play", album["album"], "\n")
                            parsed_uri = parse_uri_from_spotify_url(album["url"])
                            sp.start_playback(
                                device_id=DEVICE_ID,
                                context_uri="spotify:album:" + parsed_uri,
                            )
                            break
                    sleep(2)
                else:
                    print("Error obtaining UID\n")
        except KeyboardInterrupt:
            print("Exiting...")
            GPIO.cleanup()
            mfrc522.MFRC522_StopCrypto1()
            break
        except Exception as e:
            print(e)
            print("Error reading tag\n")
            sleep(1)


if __name__ == "__main__":
    main()
