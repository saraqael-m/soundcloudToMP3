# SoundcloudToMP3
## Description
Includes a script to convert soundcloud songs / playlists / liked songs to mp3 files. I tried multiple different soundcloud converters for python but all seemed deprecated. That's why I decided to make one myself. It will download all the songs that aren't already in the directory, so it's great as a tool to renew the downloads if a soundcloud playlist has new songs added to it.

## Dependencies and Setup
**You need a Chromedriver and the Chrome browser for this to work. More infos later on!**
I tested this script only with [Python 3.7.9](https://www.python.org/downloads/release/python-379/) but all 3.7.x versions should definitely work. Newer versions probably work, but older versions might not.
Python modules you need (can be installed in cmd via "pip" command):
* selenium (pip install selenium)
* urllib3 (pip install urllib3)
* progressbar (pip install progressbar)
along with the preinstalled os, time, and sys modules.
Also, you have to have [Chrome](https://www.google.com/chrome/) (preferably version 91, because it was only tested with that) along with the corresponding [Chromedriver](https://chromedriver.chromium.org/downloads) (also preferably version 91).
The only things that have to be hardcoded are the two variables at the top of the script:
* **downloadPath** variable should be a string of the path to the download folder you want (if not configured it will be in the same dir as the script; for example: `r"C://user//saraqael-m//Documents//soundcloudMusic"`, two forward slashes instead of a backward slash)
* **executablePath** variable should be a string of the path to the chromedriver.exe (including the name of the .exe file at the end; if not configured it has to be in the same dir as the script; for example: `r"C://user//saraqael-m//Documents//chromedriver.exe"`)

## Usage
1. Navigate to the folder with the python script in it.
2. Open a terminal in that directory (either by typing "cmd" into the path in explorer or by inputting `cd C:\path\to\script` into cmd).
3. Run the command `python soundcloudDownloader.py [s/p/l] [url] ([downloadPath])`.
    * the first parameter can be s, p, or l, depending on if you want to download a **S**ong, a **P**laylist, or the **L**ikes of a person
    * the second parameter is always the link to that song / playlist / liked songs (for example a song: https://soundcloud.com/sunnexo/lost-umbrella-remix; if you want to download the likes, https://soundcloud.com/you/likes won't work, you have to replace "you" with your username, which can be found in the url in your profile)
    * the third parameter is optional but it can be used to directly set the downloadPath variable to decide where to the songs are downloaded

An example command in the terminal would now look like this:

`C:\user\saraqael-m\Documents\soundcloudMusic> python soundcloudDownloader.py s https://soundcloud.com/sunnexo/lost-umbrella-remix`

My script uses the website https://soundcloudtomp3.app/ to get its files from.
