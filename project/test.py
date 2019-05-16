import requests
from bs4 import BeautifulSoup
from pprint import pprint as pp


artist_name= 'blackpink'
songkick_key = 'XFK6hX8iZ4LjPg6l'
artist_res = requests.get('https://www.songkick.com/search?utf8=✓&type=initial&query='+artist_name).text
artist_doc = BeautifulSoup(artist_res, 'html.parser')
artist_url = artist_doc.find('p',{'class': 'summary'}).find('a')['href']
artist_id = artist_url.split('/')[2].split('-')[0]
artist_info = requests.get('https://api.songkick.com/api/3.0/artists/{}/calendar.json?apikey={}'.format(artist_id, songkick_key))
events = artist_info.json().get('resultsPage').get('results').get('event')
events= events[1]
pp(events)