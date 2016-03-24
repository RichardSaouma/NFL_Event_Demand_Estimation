# outside
import requests
import logging
#from pymongo import MongoClient
import json
from datetime import datetime
import dateutil.parser
import time
import email
import smtplib
import psycopg2
from psycopg2.extensions import AsIs
import ast
import os
##Mine
import configs
import stubhub_api

os.chdir('C:\mongodb\data\stub')
##Logging
nowlog = datetime.today()
nowlogg = str(nowlog)[0:19]+'log.txt'
nowlogg=nowlogg.replace(" ","-").replace(":","-")
logging.basicConfig(filename=nowlogg, level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')
logging.debug('Start of program')


####SQL
def createtable():
	nowtable = datetime.today()
	conn = psycopg2.connect(configs.postgresql_conn)
	cur = conn.cursor()
	strtime='NFL'+str(nowtable)[:-7].replace(":","-").replace(" ","-T").replace("-","")
	cur.execute("CREATE TABLE %s (id bigserial PRIMARY KEY, jdoc jsonb);",[AsIs(strtime)])
	conn.commit()
	return strtime


#Timestamp for data retreival	
def noww():
	return str(datetime.today())[:-7].replace(":","-").replace(" ","-T").replace("-","") 


#Strip down to the relevant events to check at this interval
def get_events_to_track(cover,todays_events):
	event_ids = []
	for i in cover:
		for e in todays_events[i]:
			event_ids.append(str(e))
	return event_ids


#First if-break command makes sure that if the listing is dead, the 
#system does not die	
def record_listings_for_event(event_id,reltab):
	eventIdh = event_id
	event_listings = stubhub_api.get_listings_for_event(event_id)
	if "INS04" in str(event_listings):
		print(str(event_id)+" is Bad")
	elif "u'eventId': None" in str(event_listings):
		print("No Listings for " + str(event_id))
	else:
		print("Passing results to db for " + str(eventIdh))
		record_listings_for_event0(event_listings,eventIdh,reltab)

def record_listings_for_event0(event_listings,eventIdh,reltab):
	listings_to_add = []
	try:
		for l in event_listings['listing']:
				listing = {"eventId": eventIdh,"errors": event_listings['errors'], "datetime": noww(),"seatNumbers": l['seatNumbers'],"currentPrice": l['currentPrice']['amount'],"currentPriceCur": l['currentPrice']['currency'],"FaceValuePrice": str(l['faceValue']),"DirtyTicketInd": l['dirtyTicketInd'],"listingId": l['listingId'],"sectionId": l['sectionId'],"sectionName": l['sectionName'],"sellerSectionName": ['sellerSectionName'],"zoneId": l['zoneId'],"zoneName": l['zoneName'],"splitVector": l['splitVector'],"listingAttributeList": str(l['listingAttributeList']),"row": l['row'],"deliveryTypeList": str(l['deliveryTypeList']),"deliveryFee": str(l['deliveryFee']),"serviceFee":l['serviceFee'],"seatNumbers": l["seatNumbers"],"quantity": l["quantity"]}
				listings_to_add.append(listing)
		for list in listings_to_add:
			conn = psycopg2.connect(configs.postgresql_conn)
			cur = conn.cursor()
			cur.execute("""INSERT INTO %s (jdoc) VALUES (%s)""",[AsIs(reltab),json.dumps(list)])
			conn.commit()
			conn.close()
			cur.close()
		print "Found " + str(len(listings_to_add)) + " to add for " + str(eventIdh)
	except KeyboardInterrupt:
		return
	except:
		 msg = email.message_from_string('warning')
		 msg['From'] = "*****@hotmail.com"
		 msg['To'] = "*****"
		 msg['Subject'] = "Trouble!!!event %s" % (eventIdh)  
		 s = smtplib.SMTP("smtp.live.com",587)
		 s.ehlo()
		 s.starttls() 
		 s.ehlo()
		 s.login('*****@hotmail.com', '**')
		 s.sendmail("**@hotmail.com", "**@**.ch", msg.as_string())
		 s.quit()
			
#Fire it up!
def initiate(cover,reltab):
	#Fetch the events to read record
	#Comes from the text file written by createSched.py once a day
	nowday=str(datetime.today())[:10]	
	with open("nfl"+str(nowday)+".txt", "rb")  as fo:
		s = fo.read()
		todays_events = ast.literal_eval(s)
	event_ids = get_events_to_track(cover,todays_events)
	for event_id in event_ids:
		record_listings_for_event(event_id,reltab)
		time.sleep(6)
#Drop table if no events to record
	if len(event_ids) == 0:
		conn = psycopg2.connect(configs.postgresql_conn)
		cur = conn.cursor()
		cur.execute("DROP TABLE IF EXISTS %s;",[AsIs(reltab)])
		conn.commit()
logging.debug('End of program')
	