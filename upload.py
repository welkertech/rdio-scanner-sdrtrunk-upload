from datetime import datetime
import time
import requests
import re
import os

system = "000000000"
apikey = "000000000"
url = "https://server/api/call-upload/"
frequency = "000000000"
RecordingsPath = "C:\\Users\\user\\SDRTrunk\\recordings\\"

def main():
	while True:

		fileList = os.listdir(RecordingsPath)
		fileList.sort(reverse=False)
		if len(fileList) > 0:
			upload(fileList[0])

		time.sleep(0.1)



def upload(mp3file):
	talkgroup = re.search(r'.*TO_(\d+).*', mp3file).group(1)

	#not all files have a from, so we are going to try to get it, if it fails, just return the talk group.
	try:
		source = re.search(r'.*FROM_(\d+)', mp3file).group(1)
	except:
		source = talkgroup

	time = mp3file[0:14]

	isoTime = str(datetime.strptime(time, '%Y%m%d_%H%M%S').isoformat())



	values = {
				'key': apikey,
				'dateTime': isoTime ,
				'frequencies' : frequency,
				'frequency' : frequency,
				'source' : source,
				'talkgroup' : talkgroup,
				'system': system
				}


	upload = open(RecordingsPath + mp3file,'rb')

	files = {'audio': (mp3file, upload, 'audio/mp3')}
	try:
		r = requests.post(url, files=files, data=values)
		print ("----------New Call-----------")
		print (isoTime)
		print (mp3file)
		print (r.content)
		upload.close()
		os.remove(RecordingsPath + mp3file)
	except:
		print ("Upload Failed")
		
	
	

if __name__ == "__main__":
    main()