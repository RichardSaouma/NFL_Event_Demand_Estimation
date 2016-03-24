# NFL_Event_Demand_Estimation
Script to Schedule live scrapes of secondary-market NFL event ticket prices 

These scripts allow you to programmatically pull secondary-market ticket prices for events covered by stubhub 
into a local POSTGRESQL database


configs.py:         Stores your authentication data; stubhub API key, and local SQL access data 

nfldates.csv:       Two columns: date and stubhub eventID for all nfl games 

nflcreateSched.py:  Sorts all future events into a buckets depending on how far into the future the event takes place. 
                    Outputs a dictionary with each bucket and the events that fall within each bucket's timeframe, 
                    dictionary printed into nfl%s %(YEAR-MONTH-DAY,) in ####-##-## format 

nrl00.py:           Master program that identifies current day, fetches relevant nfl####-##-##.txt dictionary 
                    and deposits records into unique POSTGRESQL json table by event+recording-datetime. Also features error 
                    alerts from hotmail accounts to primary email 

nrl0del2.py:        Pseudo-Chron Script--Minimal script which indicates which buckets to query. 
                    Will call on nrl00.py to then do all the heavy lifting. Make as many copies as needed an schedule; 
                    i.e. windows task scheduler
