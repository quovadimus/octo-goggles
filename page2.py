import datetime
import dateutil.parser
import json
import os
import requests
import threading
from operator import itemgetter

JSS_URL = ''
JSS_URL_ADMIN = ''
JSS_USERNAME = '' #str(raw_input('Username: '))
JSS_PASSWORD = ''  #getpass.getpass()
JSS_SEARCH_ID = 191

TIPBOARD_URL = 'http://localhost:7272'
TIPBOARD_TOKEN = ''


def get_search_report():
    url = os.path.join(JSS_URL, 'JSSResource/computerreports/id/{}'.format(JSS_SEARCH_ID))
    headers = {'Accept': 'application/json'}
    auth = (JSS_USERNAME, JSS_PASSWORD)
    response = requests.get(url, headers=headers, auth=auth)
    response.raise_for_status()
    return response.json()['computer_reports']


def update_pie_chart(key, chart_data):
    print('Updating Tipboard tile {}'.format(key))
    form_data = {
        'tile': 'pie_chart',
        'key': key,
        'data': json.dumps({'pie_data': chart_data})
    }
    print(form_data)
    r = requests.post(os.path.join(TIPBOARD_URL, 'api/v0.1/{}/push'.format(TIPBOARD_TOKEN )), data=form_data)
    print('Status: {}, {}'.format(r.status_code, r.text))


def update_text(key, text_data):
    print('Updating Tipboard tile {}'.format(key))
    json_data = {'text': text_data}

    form_data = {
        'tile': 'text',
        'key': key,
        'data': json.dumps(json_data)
    }

    r = requests.post(os.path.join(TIPBOARD_URL, 'api/v0.1/{}/push'.format(TIPBOARD_TOKEN )), data=form_data)
    print('Status: {}, {}'.format(r.status_code, r.text))

def managed_unmanaged_clients(report_data):
    managed = 0
    unmanaged = 0
    for i in report_data:
        if i['Managed'] == 'Managed':
            managed += 1
        else:
            unmanaged += 1

    chart_data = [
        ['Managed ({})'.format(managed), managed],
        ['Unmanaged ({})'.format(unmanaged), unmanaged]
    ]
    update_pie_chart('2D', chart_data)

def checkin_status(report_data):
    checkin_0_to_14 = 0
    checkin_15_to_30 = 0
    checkin_31_over = 0
    skipped = 0
    now = datetime.datetime.now()
    for i in report_data:
        try:
            checkin_time = datetime.datetime.strptime(i['Last_Check_in'], '%Y-%m-%d %H:%M:%S')
        except:
            skipped += 1
            continue

        days_since = (now - checkin_time).days
        if days_since < 15:
            checkin_0_to_14 += 1
        elif 14 < days_since < 31:
            checkin_15_to_30 += 1
        else:
            checkin_31_over += 1

    chart_data = [
        ['Under 14 Days', checkin_0_to_14],
        ['15 to 30 Days', checkin_15_to_30],
        ['Over 31 Days', checkin_31_over],
        ['Skipped', skipped]
    ]
    update_pie_chart('2A', chart_data)


def filevault_enabled(report_data):
    fv2_enabled = 0
    fv2_disabled = 0
    skipped = 0
    top_non_compliant = []
    for i in report_data:
        if i['Managed'] != 'Managed':
            skipped += 1
            continue

        fv2_status = i['FileVault_2_Status']
        if fv2_status in ['Boot Partitions Encrypted', 'All Partitions Encrypted']:
            fv2_enabled += 1
        elif fv2_status in ['No Partitions Encrypted', 'N/A']:
            fv2_disabled += 1
            try:
                last_checkin = datetime.datetime.strptime(i['Last_Check_in'], '%Y-%m-%d %H:%M:%S')
            except:
                continue

            top_non_compliant.append([i['JSS_Computer_ID'], i['Computer_Name'], i['Username'], last_checkin])
        else:
            skipped += 1

    top_non_compliant_sorted = sorted([i for i in top_non_compliant], key=itemgetter(3))
    top_non_compliant_sorted = top_non_compliant_sorted[:15]
    text_list = []
    for i in top_non_compliant_sorted:
        url = os.path.join(JSS_URL_ADMIN, 'computers.html?id={}'.format(i[0]))
        text_list.append(
            'Computer {},  {},  {} <a href="{}" target="_blank">View in JSS</a>'.format(i[0], i[1].encode('utf-8'), i[2], url)
        )

    chart_data = [
        ['Enabled ({})'.format(fv2_enabled), fv2_enabled],
        ['Disabled({})'.format(fv2_disabled), fv2_disabled],
        ['Skipped ({})'.format(skipped), skipped]
    ]
    text_data = '<br>'.join(text_list)
    update_pie_chart('2B', chart_data)
    update_text('2C', text_data)


def root_enabled(report_data):
    enabled = 0
    disabled = 0
    skipped = 0
    for i in report_data:
        if i['Managed'] != 'Managed':
            skipped += 1
            continue

        if i['Master_Password_Set'] == 'false':
            disabled += 1
        else:
            enabled += 1

    chart_data = [
        ['Enabled ({})'.format(enabled), enabled],
        ['Disabled({})'.format(disabled), disabled],
        ['Skipped ({})'.format(skipped), skipped]
    ]
    update_pie_chart('2F', chart_data)
    

def sip_status(report_data):
    enabled = 0
    disabled = 0
    skipped = 0
    for i in report_data:
        if i['Managed'] != 'Managed':
            skipped += 1
            continue

        if i['SIP_Status'] == 'disabled':
            disabled += 1
        else:
            enabled += 1

    chart_data = [
        ['Enabled ({})'.format(enabled), enabled],
        ['Disabled({})'.format(disabled), disabled],
        ['Skipped ({})'.format(skipped), skipped]
    ]
    update_pie_chart('2E', chart_data)
    
    

def main():
    print('Reading data from Advanced Computer Search {}'.format(JSS_SEARCH_ID))
    report_data = get_search_report()
    #managed_unmanaged_clients(report_data)
    #checkin_status(report_data)
    #filevault_enabled(report_data)
    #root_enabled(report_data)
    sip_status(report_data)
	
if __name__ == '__main__':
    main()
