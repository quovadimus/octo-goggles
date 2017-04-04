import json
import requests
import datetime
import os


JSS_URL = ''
JSS_URL_ADMIN = ''
JSS_USERNAME = '' #str(raw_input('Username: '))
JSS_PASSWORD = ''  #getpass.getpass()
JSS_SEARCH_ID = #id number

TIPBOARD_URL = 'http://localhost:7272'
TIPBOARD_TOKEN = ''


print("Pulling advanced computer search data from the JSS API...")
r = requests.get(JSS_URL + '/JSSResource/computerreports/id/161', headers={'Accept': 'application/json'}, auth=(JSS_USERNAME, JSS_PASSWORD))

macos_versions = [computer['Operating_System_Version'] for computer in r.json()['computer_reports']]

macos_version_counts = {} 
for v in macos_versions:
    if v not in macos_version_counts.keys():
        macos_version_counts[v] = 1
    else:
        macos_version_counts[v] += 1


elcap_count = 0
sierra_count = 0

computer_report = r.json()['computer_reports']

for computer in computer_report:
    if computer['Operating_System_Version'].startswith('10.11'):
        elcap_count += 1
    elif computer['Operating_System_Version'].startswith('10.12'):
        sierra_count += 1

today_date = datetime.datetime.now().strftime('%m.%d')

elcap_update = [today_date, elcap_count]
sierra_update = [today_date, sierra_count]

print elcap_update
print sierra_update


print('macOS Version Count data: {}'.format(macos_version_counts))

# A JSON file will now be at that path
# Load it to modify it

with open('/Users/admin/.tipboard/chart_data.json', 'r') as f:
	loaded_data = json.load(f)

# Now you can modify it and save the changes using the same method above!
print(loaded_data)

loaded_data['series_list'][0]  # This is your Sierra count
loaded_data['series_list'][1]  # This is your El Cap count

loaded_data['series_list'][0].append(sierra_update)
loaded_data['series_list'][1].append(elcap_update)

print(loaded_data)
# 
def update_line_chart(key, loaded__data):
    print('Updating Tipboard tile {}'.format(key))
    form_data = {
        'tile': 'line_chart',
        'key': key,
        'data': json.dumps(loaded_data)
    }
    print(form_data)
    r = requests.post(os.path.join(TIPBOARD_URL, 'api/v0.1/{}/push'.format(TIPBOARD_TOKEN )), data=form_data)
    print('Status: {}, {}'.format(r.status_code, r.text))


update_line_chart('2G', loaded_data)
 
