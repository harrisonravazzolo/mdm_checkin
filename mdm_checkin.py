## Python script used to identify devices that have not checked into the MDM service.
## This script requires the requests library item
## Note!! The error exepctions are not handled in a "useful" way. It was just a short cut to keep the script running. No data is returned.

import requests
import json

url = "https://{KandjiSubdomain}.clients.us-1.kandji.io/api/v1/devices/"

headers = {
  'Authorization': 'Bearer ###########', ##BEARER TOKEN GOES HERE##
  'Content-Type': 'application/json',
  'Accept': 'application/json'
}
#Raw data from api, not in json format
response = requests.get(url, headers=headers)

#Transform data into json
results = response.json()

#Initialize a list to append the device_ids to.
device_ids = []

#Iterate through the payload to append only device_ids
for device in range(len(results)):
   device_ids.append(results[device]['device_id'])


#
##
###
####
#Iterate through the list of 'device_ids'

#'target_date' for logic check starting in line 52. 
target_date = '2022-05-20'

#logic ran against each returned value
for i in range(len(device_ids)):
    #try/except for common errors found in this workflow.
    try:
        url_2 = 'https://{KandjiSubdomain}.clients.us-1.kandji.io/api/v1/devices/' + device_ids[i] + '/details'
        response_2 = requests.get(url_2, headers=headers)
        results_2 = response_2.json()
        #Asset tags set for devices locked and not in use. No other value in this return set to iterate on. Devices in this state are
        #marked with a 'DEPRECATED' tag in Kandji and excluded from the query.
        if results_2['general']['asset_tag'] == 'DEPRECATED':
            continue
        #Excluding the assests with the 'DEPRECATED' tag, logic check against the devices that fail the
        #'last_check_in' requirement and return those assets.  
        else:
            if results_2['mdm']['last_check_in'] <= target_date:
                print(results_2['general']['assigned_user']['email'] + ' ' + results_2['mdm']['last_check_in'])
            else:
                continue
    #Common errors thrown.     
    except requests.exceptions.JSONDecodeError:
        pass
    except TypeError:
        pass
    except KeyError:
        pass