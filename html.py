import json 
from xml.etree import ElementTree as ET

html = ET.Element('html')
body = ET.Element('body')
html.append(body)

title = ET.Element('h1')
title.text = 'Bloodstock Reviser Previews'
body.append(title)

artist_table = ET.Element('table', attrib={'style': 'border:1px solid #ccc'})
artist_table_head_row = ET.Element('tr')
artist_table_head_name = ET.Element('th')
artist_table_head_tracks = ET.Element('th')
artist_table_head_row.append(artist_table_head_name)
artist_table_head_row.append(artist_table_head_tracks)
artist_table.append(artist_table_head_row)

artists_in = json.load(open('bands_final.json', 'r'))
for artist in artists_in:
    print(artist['name'])
    artist_table_row = ET.Element('tr')
    artist_table_row_name = ET.Element('td', attrib={'style': 'border-bottom:1px solid #ccc'})
    artist_table_row_name.text = artist['name']
    artist_table_row_tracks = ET.Element('td', attrib={'style': 'border-bottom:1px solid #ccc'})
    for track in artist['top_tracks']:
        if track['preview_url']:
            artist_table_row_tracks_a = ET.Element('a', attrib={'style': 'display:block', 'href': track['preview_url']})
        else:
            artist_table_row_tracks_a = ET.Element('span', attrib={'style': 'display:block'})

        artist_table_row_tracks_a.text = track['name']
        artist_table_row_tracks.append(artist_table_row_tracks_a)

    artist_table_row.append(artist_table_row_name)
    artist_table_row.append(artist_table_row_tracks)
    artist_table.append(artist_table_row)

body.append(artist_table)

with open('boa-revision.html', 'w') as out_file:
    ET.ElementTree(html).write(out_file, encoding='unicode', method='html')