raspberry-countly
=================

Python script for pulling events from Countly. Extra fun with servos and mp3 files.

Download the script to /home/pi/scripts/countly/ and modify the App Id and API key appropriately.

The script will create the files it needs to track the events, and it will download the mp3 file (http://soundbible.com/333-Cash-Register-Cha-Ching.html).

Unfortunately, for now, the script is hardcoded for three particular events that I have defined for my Countly profile. If you want to use this script, you will need to make some less-than-trivial modifications so that it reads your Countly events.