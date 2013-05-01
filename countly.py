import RPi.GPIO as GPIO
import urllib2
import simplejson
import time
import datetime
import os

app_id = "YOUR APP ID"
api_key = "YOUR API KEY"
working_path = "/home/pi/scripts/countly/"

arrayWithDate = []
today = datetime.date.today()
arrayWithDate.append(today)
# get the date in YYYY-MM-DD by calling arrayWithDate[0]


pin = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.OUT)
GPIO.output(pin, True)

adsUrl = "https://cloud.count.ly/o?app_id=" + app_id + "&method=events&event=bannerViewDidLoadAd&api_key=" + api_key + "&action=refresh"
iAPCancelsUrl = "https://cloud.count.ly/o?app_id=" + app_id + "&method=events&event=clickedTheIAPCancelButton&api_key=" + api_key + "&action=refresh"
purchasesUrl = "https://cloud.count.ly/o?app_id=" + app_id + "&method=events&event=transactionComplete&api_key=" + api_key + "&action=refresh"

numberOfAdsRequest = urllib2.Request(adsUrl)
numberOfiAPCancelsRequest = urllib2.Request(iAPCancelsUrl)
numberOfPurchasesRequest = urllib2.Request(purchasesUrl)
opener = urllib2.build_opener()


#create the files if they don't exist
#adCount.txt
if (os.path.isfile(working_path + "adCount.txt")):
	print "adCount.txt exists. do nothing"
else:
	print "adCount.txt does not exist. creating it now"
	with open(working_path + "adCount.txt", "w") as f:
		f.write("0")

#cancelCount.txt
if (os.path.isfile(working_path + "cancelCount.txt")):
	print "cancelCount.txt exists. do nothing"
else:
	print "cancelCount.txt does not exist. creating it now"
	with open(working_path + "cancelCount.txt", "w") as f:
		f.write("0")

#purchaseCount.txt
if (os.path.isfile(working_path + "purchaseCount.txt")):
	print "purchaseCount.txt exists. do nothing"
else:
	print "purchaseCount.txt does not exist. creating it now"
	with open(working_path + "purchaseCount.txt", "w") as f:
		f.write("0")

#log.txt
if (os.path.isfile("/home/pi/scripts/countly/log.txt")):
	print "log.txt exists. do nothing"
else:
	print "log.txt does not exist. creating it now"
	open("/home/pi/scripts/countly/log.txt", "w")

#date.txt
if (os.path.isfile("/home/pi/scripts/countly/date.txt")):
	print "date.txt exists. read date from it:"
	with open("/home/pi/scripts/countly/date.txt", "r") as f:
		scriptDate = f.read()
		if (scriptDate == str(arrayWithDate[0])):
			print "they match!!"
		else:
			print "they don't match!! blanking out files"
			with open(working_path + "adCount.txt", "w") as f:
				f.write("0")
			with open(working_path + "cancelCount.txt", "w") as f:
				f.write("0")
			with open(working_path + "purchaseCount.txt", "w") as f:
				f.write("0")
			with open("/home/pi/scripts/countly/date.txt", "w") as f:
				f.write(str(arrayWithDate[0]))
else:
	print "date.txt does not exist. creating it now"
	with open("/home/pi/scripts/countly/date.txt", "w") as f:
		f.write(str(arrayWithDate[0]))

#download the mp3 file if it doesn't exist
if (os.path.isfile("/home/pi/scripts/countly/chaching.mp3")):
	print "mp3 exists. do nothing"
else:
	print "mp3 does not exist. creating it now"
	url = 'http://soundbible.com/grab.php?id=333&type=mp3'
 	 
	print "downloading with urllib2"
	f = urllib2.urlopen(url)
	data = f.read()
	with open("chaching.mp3", "wb") as code:
	    code.write(data)






logFileHandle = open("/home/pi/scripts/countly/log.txt", "a")



with open(working_path + "adCount.txt", "r") as f:
	adCount = int(f.read())

with open(working_path + "cancelCount.txt", "r") as f:
	cancelCount = int(f.read())

with open(working_path + "purchaseCount.txt", "r") as f:
	purchaseCount = int(f.read())

print "adCount: " + str(adCount)
print "cancelCount: " + str(cancelCount)
print "purchaseCount: " + str(purchaseCount)



def spinclockwise(spinningLength):
        speed = .0085
        #.008 is slow, nudge it up to make it faster
        # use .01874 to spin it the other way at roughly the same speed
        for i in range(1,spinningLength):
                delay = .02 - speed
                GPIO.output(pin,False)
                time.sleep(speed)
                GPIO.output(pin,True)
                time.sleep(.02-speed)


now = datetime.datetime.now()
year = str(now.year)
month = str(now.month)
day = str(now.day)

displayTime = str(now.year) + "-" + str(now.month) + "-" + str(now.day) + " " + str(now.hour) + ":" + str(now.minute).zfill(2) + ":" + str(now.second).zfill(2)

adCountJson = opener.open(numberOfAdsRequest)
parsedAdCount = simplejson.load(adCountJson)
cancelCountJson = opener.open(numberOfiAPCancelsRequest)
parsedCancelCount = simplejson.load(cancelCountJson)
purchaseCountJson = opener.open(numberOfPurchasesRequest)
parsedPurchaseCount = simplejson.load(purchaseCountJson)




# Get new counts, and account for when there are no values (new day).
if (len(parsedAdCount[0][year][month]) == 0):
	newAdCount = 0
else:
	newAdCount = parsedAdCount[0][year][month][day]['c']

if (len(parsedCancelCount[0][year][month]) == 0):
	newCancelCount = 0
else:
	newCancelCount = parsedCancelCount[0][year][month][day]['c']

if (len(parsedPurchaseCount[0][year][month]) == 0):
	newPurchaseCount = 0
else:
	newPurchaseCount = parsedPurchaseCount[0][year][month][day]['c']

adDifference = newAdCount-adCount
cancelDifference = newCancelCount-cancelCount
purchaseDifference = newPurchaseCount-purchaseCount

string_for_log = "\n" + displayTime
string_for_log += "\n" + str(adDifference) + " more ads shown. Total: " + str(newAdCount)
string_for_log += "\n" + str(cancelDifference) + " more cancels. Total: " + str(newCancelCount)
string_for_log += "\n" + str(purchaseDifference) + " more purchases. Total: " + str(newPurchaseCount) + "\n"


logFileHandle.write(string_for_log)


#check the ads and take actions
if (newAdCount > adCount):
	with open(working_path + "adCount.txt", "w") as f:
		f.write(str(newAdCount))
	
#check the cancels and take actions
if (newCancelCount > cancelCount):
	with open(working_path + "cancelCount.txt", "w") as f:
		f.write(str(newCancelCount))
	spinclockwise(cancelDifference*30);

#check the purchases and take actions
if (newPurchaseCount > purchaseCount):
	with open(working_path + "purchaseCount.txt", "w") as f:
		f.write(str(newPurchaseCount))
	spinclockwise(100)
	os.system('mpg321 -q chaching.mp3')


