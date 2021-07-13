
# USAGE:
#
# in cmd, dir with python file: "python soundcloudDownload.py [s/p/l/m] [songURL] ([downloadPath])"
# downloadPath is optional, s = song, p = playlist, l = likes (all likes from specific person)

import os, time, sys
import urllib.request
import progressbar
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

downloadPath = os.path.dirname(os.path.abspath(__file__))
executablePath = os.path.dirname(os.path.abspath(__file__)) + "//chromedriver.exe"

def start(downloadPath, executablePath):
	global driver
	options = Options()
	options.headless = True
	prefs = {"download.default_directory":downloadPath,"directory_upgrade":True}
	options.add_experimental_option("prefs",prefs)
	options.add_experimental_option("excludeSwitches", ["enable-logging"])
	driver = webdriver.Chrome(options=options, executable_path=executablePath)

def downloadSong(songURL, downloadPath, downloadedSongs):
	global driver
	driver.get("https://soundcloudtomp3.app/download/?url="+songURL)
	downloadButton = driver.find_element_by_id("dlMP3")
	title = str(downloadButton.get_attribute("title")[9:-4])
	titleNEW = toAlphTitle(title)
	# if song is already downloaded dont download, if not download
	if titleNEW not in downloadedSongs:
		print("Downloading: "+title)
		downloadButton.click()
		time.sleep(2)
	else:
		print("Already downloaded: "+title)

def downloadSongFast(songURL, downloadPath, downloadedSongs):
	global driver, pbar
	driver.get("https://soundcloudtomp3.app/download/?url="+songURL)
	downloadButton = driver.find_element_by_xpath("//a[@title='Righ Click -> Save Link As']")
	title = toDirTitle(str(driver.find_element_by_id("dlMP3").get_attribute("title")[9:-4]))
	titleNEW = toAlphTitle(title)
	# if song is already downloaded dont download, if not download
	pbar = None
	if titleNEW not in downloadedSongs:
		print("Downloading: "+title)
		urllib.request.urlretrieve(downloadButton.get_attribute("href"), downloadPath+"\\"+title+".mp3", show_progress)
	else:
		print("Already downloaded: "+title)

def downloadedSongs(downloadPath):
	os.chdir(downloadPath)
	songs = []
	for file in os.listdir(downloadPath):
		if file.endswith(".mp3"):
			title = toAlphTitle(file[:-4])
			songs.append(title)
	return songs

def toAlphTitle(s):
	newS = ""
	for c in s:
		n = ord(c)
		if (n > 64 and n < 91) or (n > 96 and n < 123): # only letters
			newS += c
		else:
			newS += "-"
	return newS

def toDirTitle(s):
	unwantedChars = [i for i in str("#%&{}\\$!':@<>*?/+`|="+'"')]
	newS = ""
	for c in s:
		if c in unwantedChars:
			newS += "_"
		else:
			newS += c
	return newS

def scrollDown():
	global driver
	last_height = driver.execute_script("return document.body.scrollHeight")
	while True:
	    # Scroll down to bottom
	    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
	    # Wait to load page
	    time.sleep(.75)
	    # Calculate new scroll height and compare with last scroll height
	    new_height = driver.execute_script("return document.body.scrollHeight")
	    if new_height == last_height:
	        break
	    last_height = new_height

def show_progress(block_num, block_size, total_size):
    global pbar
    if pbar is None:
        pbar = progressbar.ProgressBar(maxval=total_size)
        pbar.start()

    downloaded = block_num * block_size
    if downloaded < total_size:
        pbar.update(downloaded)
    else:
        pbar.finish()
        pbar = None

def downloadPlaylist(playlistURL, downloadPath):
	global driver
	driver.get(playlistURL)
	element_present = EC.presence_of_element_located((By.CLASS_NAME, "listenDetails__trackList"))
	trackList = WebDriverWait(driver, 10).until(element_present)
	toDownload = []
	scrollDown()
	print("Found songs:")
	for i in trackList.find_elements_by_css_selector("*"):
		try:
			if i.get_attribute("class") == "trackItem__trackTitle sc-link-dark sc-link-primary sc-font-light":
				songURL = i.get_attribute("href")
				print(songURL)
				toDownload.append(songURL)
		except:
			pass
	print()
	print("Starting to download:")
	songs = downloadedSongs(downloadPath)
	for i in toDownload:
		downloadSongFast(i, downloadPath, songs)

def downloadLikes(likesURL, downloadPath):
	global driver
	driver.get(likesURL)
	toDownload = []
	time.sleep(1)
	scrollDown()
	print("Found songs:")
	for i in driver.find_element_by_class_name("l-fixed-top-one-column").find_elements_by_css_selector("*"):
		try:
			if i.get_attribute("class") == "sound__coverArt":
				songURL = i.get_attribute("href")
				print(songURL)
				toDownload.append(songURL)
		except:
			pass
	print()
	print("Starting to download:")
	songs = downloadedSongs(downloadPath)
	for i in toDownload:
		downloadSongFast(i, downloadPath, songs)

if __name__ == "__main__":
	print()
	try:
		dtype = str(sys.argv[1])
		durl = str(sys.argv[2])
	except IndexError:
		if dtype != "m":
			print("Key argument missing.")
			raise TypeError("Download type or url were not given.")
	try:
		dpath = str(sys.argv[3])
	except IndexError:
		dpath = downloadPath
		print("Download path was automatically set to "+str(downloadPath))

	start(dpath, executablePath)
	
	if dtype == "s":
		downloadSongFast(durl, dpath, downloadedSongs(dpath))
	elif dtype == "p":
		downloadPlaylist(durl, dpath)
	elif dtype == "l":
		downloadLikes(durl, dpath)
	else:
		print("No such download type.")

	time.sleep(.1)
	driver.quit()
