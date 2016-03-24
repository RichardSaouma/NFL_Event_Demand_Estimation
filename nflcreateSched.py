# -*- coding: UTF-8 -*-
#Create Update Schedule
#
#Events are sorted in buckets depending on
#how soon they commence such that the closer
#the event date, the more often we sample prices

#Script relies on nfldates.csv and seasontix.csv which were each scraped once



from datetime import datetime

#Define today
now=datetime.strptime(str(datetime.today())[:10].replace("-","/"), "%Y/%m/%d")
nowday=str(datetime.today())[:10]

#Import dates and event_id
import csv
d={}
sd={}
with open('nfldates.csv') as f:
	z = csv.reader(f)
	for row in z:
		k, v = row
		d[v]=k 

with open('seasontix.csv') as f:
	z = csv.reader(f)
	for row in z:
		k, v = row
		sd[v]=k 


	
def date_format(cc):
	return datetime.strptime(cc, "%Y-%m-%d")
#Define buckets
A_bucket=range(0,1)
B_bucket=range(1,6)
C_bucket=range(6,11)
D_bucket=range(11,32)
E_bucket=range(32,200)

#def get_today_events_to_track():
A_event = [event for event, date in d.items() if (date_format(date) - now).days in A_bucket]	
B_event = [event for event, date in d.items() if (date_format(date) - now).days in B_bucket]
C_event = [event for event, date in d.items() if (date_format(date) - now).days in C_bucket]
D_event = [event for event, date in d.items() if (date_format(date) - now).days in D_bucket]
E_event = [event for event, date in d.items() if (date_format(date) - now).days in E_bucket]
todays_events={'A':A_event,'B':B_event,'C':C_event,'D':D_event,'E':E_event}
#	return todays_events

fw = open("nfl"+str(nowday)+".txt","wb") 
fw.write(str(todays_events))
fw.close()



