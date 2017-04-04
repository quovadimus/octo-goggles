#!/bin/bash

#examples of the various types of dashboard items from tipboard, corresponds to the layout examples yml page

url='localhost'
apikey=''


#Text Tile 2A
curl -s http://"$url":7272/api/v0.1/"$apikey"/push -X POST -d "tile=text" -d 'key=E1' -d 'data={"text": "Hello world!Simple text-tile designated to display... (surprise!) text."}'

#Sample config for Text  - color

curl -s http://"$url":7272/api/v0.1/"$apikey"/tileconfig/E1 -X POST -d 'value={"font_color": "#00FF00"}'
     
     
# Simple Percentage Tile 2B
curl -s http://$url:7272/api/v0.1/"$apikey"/push -X POST -d "tile=simple_percentage" -d 'key=E2' -d 'data={"title": "AV Report", "subtitle": "Systems Reporting Performance Issues", "big_value": "100%", "left_value": "97%", "left_label": "Cylance CPU Usage", "right_value": "189%", "right_label": "McAfee CPU Usage"}'

# Tile 2B configuration sample
curl http://$url:7272/api/v0.1/"$apikey"/tileconfig/E2 -X POST -d 'value={"big_value_color": "green", "fading_background": false}'

#Tile 2C - Listing

curl http://$url:7272/api/v0.1/"$apikey"/push -X POST -d "tile=listing" -d "key=E3" -d 'data={"items": ["BossMan: 5", "Product Owner: 0", "Grunt: 3", "Developer: 0"]}'

# Tile 2D - Bar Chart

curl http://$url:7272/api/v0.1/"$apikey"/push -X POST -d "tile=bar_chart" -d "key=E4" -d 'data={"title": "The A-Team",  "subtitle": "Velocity (Last tree sprints)", "ticks": ["n-2", "n-1", "Last (n)"], "series_list": [[49, 50, 35], [13, 45, 9]]}'

#Tile 2E Pie Chart

#curl http://$url:7272/api/v0.1/"$apikey"/push -X POST -d "tile=pie_chart" -d "key=2E" -d 'data={"title": "My title", "pie_data": [["Pie 1", 17], ["Pie 2", 25], ["Pie 3", 40], ["Pie4", 2], ["pie 5", 14]]}'

# pie Chart config option create legend

#curl -s http://"$url":7272/api/v0.1/"$apikey"/tileconfig/2E  -X POST -d 'value={"title": true, "legend": {"show": true, "location": "s"}}'

#Tile F Fancy Listing

curl http://$url:7272/api/v0.1/"$apikey"/push -X POST -d "tile=fancy_listing" -d "key=E5" -d 'data=[{"label": "My label 1", "text": "Lorem ipsum", "description": "such description" }, {"label": "My label 2", "text": "Dolor sit", "description": "yet another" }, {"label": "My label 3", "text": "Amet", "description": "" }]'
               
# Fancy Listing config options

curl -s http://"$url":7272/api/v0.1/"$apikey"/tileconfig/E5 -X POST -d 'value={"vertical_center": true, "1": {"label_color": "red", "center": true}, "3": {"label_color": "green", "center": true }}'               

# Cumulative Flow Listing
curl -s http://"$url":7272/api/v0.1/"$apikey"/push -X POST -d "tile=cumulative_flow" -d "key=E6" -d 'data={"title": "My title:", "series_list": [{"label": "label 1", "series": [ 0, 0, 0, 0, 1, 1, 2, 2, 1, 1, 1, 0, 0, 2, 0 ]}, {"label": "label 2", "series": [ 0, 5, 0, 0, 1, 0, 0, 3, 0, 0, 0, 7, 8, 9, 1 ]}]}'

# Cumulative Flow Customizations

curl -s http://"$url":7272/api/v0.1/"$apikey"/tileconfig/E6 -X POST -d 'value={"ticks": [[1, "mon"], [2, "tue"], [3, "wed"], [4, "thu"], [5, "fri"], [6, "sat"], [7, "sun"]]}'

#line_chart
curl -s http://"$url":7272/api/v0.1/"$apikey"/push -X POST -d "tile=line_chart" -d 'key=E7' -d 'data={"subtitle": "averages from last week", "description": "Sales in our
dept", "series_list": [[["23.09", 8326], ["24.09", 260630], ["25.09", 240933], ["26.09", 229639], ["27.09", 190240], ["28.09", 125272], ["29.09", 3685]], [["23.09", 3685], ["24.09", 125272], ["25.09", 190240], ["26.09", 229639], ["27.09", 240933], ["28.09", 260630], ["29.09", 108326]]]}'

# line chart customizations
curl http://localhost:7272/api/v0.1/"$apikey"/tileconfig/E7 -X POST -d 'value={"grid": {"drawGridLines": true, "gridLineColor": "#FFFFFF", "shadow": false, "background": "#000000", "borderWidth": 0}}'
