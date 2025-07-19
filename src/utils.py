import urllib.parse
import requests, json
from bs4 import BeautifulSoup

def get_cover(url, width, height, format="jpg", crop_option=""):
    new_url = url.replace("{w}", str(width))
    new_url = new_url.replace("{h}", str(height))
    new_url = new_url.replace("{c}", crop_option)
    new_url = new_url.replace("{f}", format)
    return new_url

def convert_album_to_song_url(album_url):
    parsed = urllib.parse.urlparse(album_url)
    query_params = urllib.parse.parse_qs(parsed.query)
    song_id = query_params.get('i', [None])[0]

    if not song_id:
        return None

    parts = parsed.path.split('/')
    country = parts[1]
    title = parts[3]

    return f"https://music.apple.com/{country}/song/{title}/{song_id}"

def get_all_singles(url="https://music.apple.com/us/artist/king-princess/1349968534"):
    result = []
    url = url+"/see-all?section=singles"
    
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    items = soup.find('script', {'id': 'serialized-server-data'})
    our_json = json.loads(items.text)
    
    sections = our_json[0]['data']['sections'][0]['items']
        
    for i in sections:
        result.append((i['segue']['actionMetrics']['data'][0]['fields']['actionUrl']))
    
    return result