import json
import requests

# These variables are going to be used below in the request commands
JSS_URL = ''
JSS_USER = ''
JSS_PASS = ''

TB_URL = 'http://localhost:7272'
TB_KEY = ''
# print() lines are the same as 'echo' in Bash
print("Pulling advanced computer search data from the JSS API...")

# In Python everything is an object - so variables don't use anything like '$' to say they're a variable, Python just knows
# You use the '+' sign to join strings together - below we're building the url for the JSS that was and will do it again later
r = requests.get(JSS_URL + '/JSSResource/computerreports/id/172', headers={'Accept': 'application/json'}, auth=(JSS_USER, JSS_PASS))

# Now we're going to go through the returned data and build a list of all the version numbers returned
# This one liner is short hand for a for loop which I've included below so you can see how it's building our list
macos_versions = [computer['Operating_System_Version'] for computer in r.json()['computer_reports']]

# macos_versions = []  # [] is another way of doing list()
# for computer in r.json()['computer_reports']:
#     macos_versions.append(computer['Operating_System_Version'])

# We need to get the total counts for each unique version - below we're using a Python dictionary to do that
# The basic idea in this for loop is that if the version (key) doesn't exist, add it with a value of 1
# but if the key already exists add 1 to the value
macos_version_counts = {}  # {} is another way of doing dict()
for v in macos_versions:
    if v not in macos_version_counts.keys():
        macos_version_counts[v] = 1
    else:
        macos_version_counts[v] += 1

print('macOS Version Count data: {}'.format(macos_version_counts))

# We're building another dictionary that will be the JSON data we push to Tipboard
# Again, there's a one-liner for the 'pie_data' key which is concerting the dictionary to a list of lists (which Tipboard wants)
# What this one-liner is doing is getting each key-value pair and turning them from {key: value} - a dict - to [key, value] - a list
# The for loop that does this is shown below so you can compare and see how that works
pie_chart_data = {
    'title': 'OSX El Cap',
    'pie_data': [[key, value] for key, value in macos_version_counts.items()]
}

# pie_data_list = []
# for key, value in macos_version_counts.items():
#     pie_data_list.append([key, value])

print("Updating Tipboard tile...")

# This request command is split onto multiple lines to be easier to read (Python allows this)
# You can see we're building the Tipboard URL with multiple '+' - be careful in some scripts you might double up slashes '//'
# the 'data=' keyword argument takes the data we are going to send to Tipboard (it's a part of requests)
# We are passing into it a dictionary containing the 'tile' we're targeting, the 'key' for that tile, and then Tipboard wants the JSON under another 'data' key
# To convert our 'pie_chart_data' to JSON, we're using json.dumps() inline
# requests automatically converts this whole dictionary into form data (in curl you used multiple '-f' args to pass each key)
r = requests.post(
    TB_URL + '/api/v0.1/' + TB_KEY + '/push',
    data={'tile': 'pie_chart', 'key': 'C', 'data': json.dumps(pie_chart_data)}
    )

# Finally, we print the status code and response from Tipboard so we can troubleshoot if needed
print(r.status_code, r.text)
