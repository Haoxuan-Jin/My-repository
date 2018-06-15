import requests
import os

base = 'http://localhost:1080/'
sd_id = 'SD_BHJXBDQK' ## CBTTC study ID
sd_link = base + '/genomic-files?study_id=' + sd_id

while sd_link:
    response = requests.get(sd_link).json()
    results = response['results']
    for result in results:
        print (result['file_name'], os.path.basename(result['_links']['biospecimen']))
    try:
        sd_link = base + response['_links']['next']
    except:
        break