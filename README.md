# Digital Disc Jockey
_This README was brought to you by ChatGPT. If something looks wrong, you're probably right. Feel free to submit a PR to fix its mistakes!_

Digital Disc Jockey is an innovative project that combines the nostalgia of a traditional record player with modern digital streaming capabilities. This project uses 3D-printed records embedded with NFC chips to control Spotify playback on a Raspberry Pi.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Hardware Requirements](#hardware-requirements)
- [Software Requirements](#software-requirements)
- [Setup and Installation](#setup-and-installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Overview

Digital Disc Jockey brings together the tactile experience of a record player and the convenience of digital music streaming. By scanning 3D-printed records with embedded NFC chips, users can control Spotify playback on their Raspberry Pi.

## Pictures
<img src="pics\record-on-player.jpg" alt="Digital Disc Jockey" width="250"/>

**Use hot glue or super glue to attach NFC tag**

<img src="pics\record-nfc.jpg" alt="Digital Disc Jockey" width="250"/>

<img src="pics\under.jpg" alt="Digital Disc Jockey" width="250"/>

## Features

- Play specific albums or playlists by placing 3D-printed records on the turntable.
- Shuffle tracks within an album or playlist.
- Customizable NFC records to map to different Spotify albums or playlists.

## Hardware Requirements

- Raspberry Pi (tested on Raspberry Pi Zero 2W)
- 2-4 8mm M2.5 screws to attach Pi to 3D printed model
- Hot Glue or Super Glue
- MFRC522 RFID/NFC Reader
- NFC tags (NTAG 215 recommended)
- 3D-printed record player model
- Speakers or audio output device connected to the Raspberry Pi

## Software Requirements

- Python 3
- Required Python libraries (listed in `requirements.txt`)

## Setup and Installation
### Hardware Setup

1. Connect the MFRC522 RFID reader to your Raspberry Pi. You can find various tutorials online for wiring the RFID reader to the Raspberry Pi GPIO pins.
2. Attach the Raspberry Pi to the 3D-printed record player model using 2-4 8mm M2.5 screws.
3. Attach the NFC tags to the 3D-printed records using hot glue or super glue. Ensure that the NFC tags are securely attached to the records.
4. Place the RFID reader onto its mounting standoffs. It can techincally hang on there by itself in most cases, but you can hit it with a dab of hot glue to keep it in place. Otherwise, I'm sure there are other 3D printed solutions to help it stay in place.

### Software Setup
I recommend SSHing into your Raspberry Pi for the following steps. On the Raspberry Pi Zero 2W, the desktop environment can be slow to respond.

1. Clone this repository to your Raspberry Pi:
   ```bash
   git clone https://github.com/AndrewBudziszek/digital-disc-jockey.git
   cd digital-disc-jockey
   ```

2. Create a virtual environment and activate it:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the required Python libraries:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up your Spotify application:
   - Create a new application on the Spotify Developer Dashboard: https://developer.spotify.com/dashboard/applications
   - Note down the Client ID, Client Secret, and set the Redirect URI to `http://localhost:8888/callback`.

5. Update the credentials in `rfid-record-player.py`:
   ```python
   CLIENT_ID = 'your-client-id'
   CLIENT_SECRET = 'your-client-secret'
   REDIRECT_URI = 'http://localhost:8888/callback'
   ```

The only thing you might want to use the desktop env for is to connect your bluetooth speaker to the Raspberry Pi. You can do this by clicking the bluetooth icon in the top right corner of the desktop and following the prompts to connect your speaker. 
### Getting Your Spotify Device ID

To control Spotify playback on your Raspberry Pi, you'll need the Device ID of the target Spotify Connect device (e.g., your Raspberry Pi, a smart speaker, or any other Spotify Connect-enabled device). Here's how you can obtain it:

1. Ensure that the target device is powered on and connected to the same network as your Raspberry Pi.
2. Open the Spotify app on your phone or computer.
3. Start playing any song.
4. Tap the "Devices Available" button (it looks like a speaker and a screen) at the bottom of the screen.
5. Note the name of the device you want to use (e.g., "My Raspberry Pi").

Next, you'll use the Spotify Web API to get the Device ID:

6. Open your web browser and go to the [Spotify Web API Console](https://developer.spotify.com/console/get-users-available-devices/).
7. Click on the "GET /v1/me/player/devices" endpoint.
8. Click on the "Get Token" button and log in to your Spotify account if prompted.
9. In the "Scopes" section, ensure that `user-read-playback-state` and `user-modify-playback-state` are checked.
10. Click on the "Request Token" button.
11. After obtaining the token, click on the "Try It" button.

The API response will display a list of your available devices. Look for your device in the list and note down the `id` field. This is your Spotify Device ID.

You can now use this `DEVICE_ID` in your `rfid-record-player.py` script to control Spotify playback.

## Usage

Run the script to perform the initial OAuth flow and save the token:
```bash
python3 rfid-record-player.py
```
You only need to do the OAuth flow once (or as often as the token expires). The token will be saved in a file named `token.json`.

1. Modify the `albumUrlDict` dictionary in `rfid-record-player.py` to map NFC tags to Spotify albums or playlists. You can get Spotify Album or Playlist URLs from the Spotify app or web player.
2. Place a 3D-printed record with an embedded NFC chip on the turntable.
3. The script will read the NFC chip, identify the corresponding Spotify album or playlist, and start playback.
4. To shuffle the tracks within an album, create an NFC record with "shuffle" in its data.
5. To run the script, use the following command:
```bash
python2 rfid-record-player.py
```

## Contributing

Contributions are welcome! Please fork this repository and submit pull requests with your improvements and new features.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.