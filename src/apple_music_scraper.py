from bs4 import BeautifulSoup
import requests, json
from utils import *


def room_scrape(link="https://music.apple.com/us/room/6748797380"):
    result = []
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    rspn = requests.get(link, headers=headers)
    sup = BeautifulSoup(rspn.text, "html.parser")
    items = sup.find('script',{"id":"serialized-server-data"})
    our_json = json.loads(items.text)
    sections = our_json[0]['data']['sections']
    
    for i in sections:
        if "copper-track-swoosh" in i['id']:
            items = i['items']
            break
        else:
            items = []
    
    for i in items:
        song_url = i['playAction']['actionMetrics']['data'][0]['fields']['actionUrl']
        result.append(convert_album_to_song_url(song_url))
    
    return result

def playlist_scrape(link="https://music.apple.com/us/playlist/new-music-daily/pl.2b0e6e332fdf4b7a91164da3162127b5"):
    result = []
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    rspn = requests.get(link, headers=headers)
    sup = BeautifulSoup(rspn.text, "html.parser")
    items = sup.find('script',{"id":"serialized-server-data"})
    our_json = json.loads(items.text)
    sections = our_json[0]['data']['sections']
    
    for i in sections:
        if "track-list" in i['id']:
            items = i['items']
            break
        else:
            items = []

    for i in items:
        song_url = i['playAction']['actionMetrics']['data'][0]['fields']['actionUrl']
        result.append(convert_album_to_song_url(song_url))
    
    return result

def search(keyword="sasha sloan"):
    result = {
        'artists':[],
        'albums':[],
        'songs':[],
        'playlists':[],
        'videos':[]
    }
    link = "https://music.apple.com/us/search?term="+keyword
    
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    
    rspn = requests.get(link, headers=headers)
    soup = BeautifulSoup(rspn.text, "html.parser")
    items = soup.find('script', {'id': 'serialized-server-data'})
    our_json = json.loads(items.text)
    sections = our_json[0]['data']['sections']
    
    for i in sections:
        if "artist" in i['id']:
            artists = i
        elif "album" in i['id']:
            albums = i
        elif "song" in i['id']:
            songs = i
        elif "playlist" in i['id']:
            playlists = i
        elif "music_video" in i['id']:
            videos = i

    try:
        artists_result = []
        
        for i in artists['items']:
            artist = i['title']
            try:                
                image_url = i['artwork']['dictionary']['url']
                image_width = i['artwork']['dictionary']['width']
                image_height = i[0]['artwork']['dictionary']['height']
                artwork = get_cover(image_url, image_width, image_height)
            except:
                artwork = ""

            url = i['contentDescriptor']['url']
            artists_result.append({'title':artist, 'url':url, 'image':artwork})
        result['artists'] = artists_result
        
    except:
        pass


    try:
        albums_result = []
        
        for i in albums['items']:
            song = i['titleLinks'][0]['title']
            artist = i['subtitleLinks'][0]['title']
            try:
                image_url = i['artwork']['dictionary']['url']
                image_width = i['artwork']['dictionary']['width']
                image_height = i[0]['artwork']['dictionary']['height']
                artwork = get_cover(image_url, image_width, image_height)
            except:
                artwork = ""

            url = i['contentDescriptor']['url']
            albums_result.append({'title':song, 'artist':artist, 'url':url, 'image':artwork})
        result['albums'] = albums_result
        
    except:
        pass


    try:
        songs_result = []
        
        for i in songs['items']:
            song = i['title']
            artist = i['subtitleLinks'][0]['title']
            try:
                image_url = i['artwork']['dictionary']['url']
                image_width = i['artwork']['dictionary']['width']
                image_height = i[0]['artwork']['dictionary']['height']
                artwork = get_cover(image_url, image_width, image_height)
            except:
                artwork = ""

            url = i['contentDescriptor']['url']
            songs_result.append({'title':song, 'artist':artist, 'url':url, 'image':artwork})
        result['songs'] = songs_result
    except:
        pass



    try:
        playlists_result = []
        
        for i in playlists['items']:
            song = i['titleLinks'][0]['title']
            artist = i['subtitleLinks'][0]['title']
            try:
                image_url = i['artwork']['dictionary']['url']
                image_width = i['artwork']['dictionary']['width']
                image_height = i[0]['artwork']['dictionary']['height']
                artwork = get_cover(image_url, image_width, image_height)
            except:
                artwork = ""

            url = i['contentDescriptor']['url']
            playlists_result.append({'title':song, 'artist':artist, 'url':url, 'image':artwork})
        result['playlists'] = playlists_result
    except:
        pass


    try:
        videos_results = []
        
        for i in videos['items']:
            song = i['titleLinks'][0]['title']
            artist = i['subtitleLinks'][0]['title']
            try:
                image_url = i['artwork']['dictionary']['url']
                image_width = i['artwork']['dictionary']['width']
                image_height = i[0]['artwork']['dictionary']['height']
                artwork = get_cover(image_url, image_width, image_height)
            except:
                artwork = ""

            url = i['contentDescriptor']['url']
            videos_results.append({'title':song, 'artist':artist, 'url':url, 'image':artwork})
        result['videos'] = videos_results
    except:
        pass
    
    return result

def song_scrape(url="https://music.apple.com/us/song/california/1821538031"):
    result = {
        'title':'',
        'image':'',
        'kind':'',
        'album': {
            'title':'',
            'url':''
        },
        'artist': {
            'title':'',
            'url':''
        },
        'more':[],
        'preview-url':''
    }
    
    rspn = requests.get(url)
    soup = BeautifulSoup(rspn.text, "html.parser")
    items = soup.find('script', {'id': 'serialized-server-data'})
    our_json = json.loads(items.text)
    
    song_details = our_json[0]['data']['sections'][0] 
        
    result['title'] = song_details['items'][0]['title']
    
    image_url = song_details['items'][0]['artwork']['dictionary']['url']
    image_width = song_details['items'][0]['artwork']['dictionary']['width']
    image_height = song_details['items'][0]['artwork']['dictionary']['height']
    
    result['image'] = get_cover(image_url, image_width, image_height)
    
    result['kind'] = song_details['presentation']['kind']
    result['album']['title'] = song_details['items'][0]['album']
    result['album']['url'] = song_details['items'][0]['albumLinks'][0]['segue']['actionMetrics']['data'][0]['fields']['actionUrl']
    result['artist']['title'] = song_details['items'][0]['artists']
    result['artist']['url'] = song_details['items'][0]['artistLinks'][0]['segue']['actionMetrics']['data'][0]['fields']['actionUrl']
        
    json_tag = soup.find("script", {"id": "schema:song", "type": "application/ld+json"})
    data = json.loads(json_tag.string)

    preview_url = data['audio']['audio']['contentUrl']
    result['preview-url'] = preview_url
    
    more_songs = our_json[0]['data']['sections'][-1]['items']
    
    more_songs_list = []
    
    for i in more_songs:
        more_songs_list.append(i['segue']['actionMetrics']['data'][0]['fields']['actionUrl'])
    
    result['more'] = more_songs_list
    
    return result

def album_scrape(url="https://music.apple.com/us/album/1965/1817707266?i=1817707585"):
    result = {
        'title':'',
        'image':'',
        'caption':'',
        'artist': {
            'title':'',
            'url':''
        },
        'songs':[],
        'info':'',
        'more':[],
        'similar':[],
        'videos':[]
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    rspn = requests.get(url, headers=headers)
    soup = BeautifulSoup(rspn.text, "html.parser")
    items = soup.find('script', {'id': 'serialized-server-data'})
    our_json = json.loads(items.text)
    sections = our_json[0]['data']['sections']
    
    index=0
    for i in sections:
        if "album-detail" in i['id']:
            album_detail_index = index
        elif "track-list " in i['id']:
            track_list_index = index
        elif "video" in i['id']:
            video_index = index
        elif "more" in i['id']:
            more_index = index
        elif "you-might-also-like" in i['id']:
            similar_index = index
        elif "track-list-section" in i['id']:
            track_list_section_index = index
        index+=1
    
    try:
        result['title'] = sections[album_detail_index]['items'][0]['title']
    except:
        pass
    
    try:
        image_url = sections[album_detail_index]['items'][0]['artwork']['dictionary']['url']
        image_width = sections[album_detail_index]['items'][0]['artwork']['dictionary']['width']
        image_height = sections[album_detail_index]['items'][0]['artwork']['dictionary']['height']
        result['image'] = get_cover(image_url, image_width, image_height)
    except:
        pass
    
    try:
        result['caption'] = sections[album_detail_index]['items'][0]['modalPresentationDescriptor']['paragraphText']
    except:
        pass
    
    try:
        result['artist']['title'] = sections[album_detail_index]['items'][0]['subtitleLinks'][0]['title']
        result['artist']['url'] = sections[album_detail_index]['items'][0]['subtitleLinks'][0]['segue']['actionMetrics']['data'][0]['fields']['actionUrl']
    except:
        pass
    
    try:
        album_songs = sections[track_list_index]['items']
        for i in album_songs:
            result['songs'].append(convert_album_to_song_url(i['contentDescriptor']['url']))
    except:
        pass
    
    try:
        result['info'] = sections[track_list_section_index]['items'][0]['description']
        more_songs = sections[more_index]['items']
        for i in more_songs:
            result['more'].append(i['segue']['actionMetrics']['data'][0]['fields']['actionUrl'])
    except:
        pass
    
    try:
        similar_songs = sections[similar_index]['items']
        for i in similar_songs:
            result['similar'].append(i['segue']['actionMetrics']['data'][0]['fields']['actionUrl'])
    except:
        pass
    
    try:
        videos = sections[video_index]['items']
        for i in videos:
            result['videos'].append(i['contentDescriptor']['url'])
    except:
        pass
            
    return result

def video_scrape(url="https://music.apple.com/us/music-video/gucci-mane-visualizer/1810547026"):
    result = {
        'title': '',
        'image': '',
        'artist': {
            'title': '',
            'url': ''
        },
        'video-url': '',
        'more': [],
        'similar':[]
    }

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    items = soup.find('script', {'id': 'serialized-server-data'})
    our_json = json.loads(items.text)
    
    sections = our_json[0]['data']['sections']
    
    for i in sections:
        if "music-video-header" in i['id']:
            music_video_header = i
        elif "more-by-artist" in i['id']:
            more = i
        elif "more-in-genre" in i['id']:
            similar = i
    
    try:
        result['title'] = music_video_header['items'][0]['title']
    except:
        pass
    
    try:
        image_url = music_video_header['items'][0]['artwork']['dictionary']['url']
        image_width = music_video_header['items'][0]['artwork']['dictionary']['width']
        image_height = music_video_header['items'][0]['artwork']['dictionary']['height']
        result['image'] = get_cover(image_url, image_width, image_height)
    except:
        pass
    
    try:
        result['artist']['title'] = music_video_header['items'][0]['subtitleLinks'][0]['title']
        result['artist']['url'] = music_video_header['items'][0]['subtitleLinks'][0]['segue']['actionMetrics']['data'][0]['fields']['actionUrl']
    except:
        pass
    
    try:
        json_tag = soup.find("script", {"id": "schema:music-video", "type": "application/ld+json"})
        data = json.loads(json_tag.string)
        result['video-url'] = data['video']['contentUrl']
    except:
        pass
    
    try:
        for i in more['items']:
            result['more'].append(i['segue']['actionMetrics']['data'][0]['fields']['actionUrl'])
    except:
        pass
    
    try:
        for i in similar['items']:
            result['similar'].append(i['segue']['actionMetrics']['data'][0]['fields']['actionUrl'])
    except:
        pass
    
    return result

def artist_scrape(url="https://music.apple.com/us/artist/king-princess/1349968534"):
    result = {
        'title':'',
        'image':'',
        'latest':'',
        'top':[],
        'albums':[],
        'singles_and_EP':[],
        'playlists':[],
        'videos':[],
        'similar':[],
        'appears_on':[],
        'more_to_see':[],
        'more_to_hear':[],
        'about':'',
        'info':'',
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    
    rspn = requests.get(url, headers=headers)
    soup = BeautifulSoup(rspn.text, "html.parser")
    items = soup.find('script', {'id': 'serialized-server-data'})
    our_json = json.loads(items.text)

    sections = our_json[0]['data']['sections']
    
    for i in sections:
        if "artist-detail-header-section" in i['id']:
            artist_detail = i
        elif "latest-release-and-top-songs" in i['id']:
            latest_and_top = i
        elif "full-albums" in i['id']:
            albums = i
        elif "playlists" in i['id']:
            playlists = i
        elif "music-videos" in i['id']:
            videos = i
        elif "singles" in i['id']:
            singles = i
        elif "appears-on" in i['id']:
            appears_on = i
        elif "more-to-see" in i['id']:
            more_to_see = i
        elif "more-to-hear" in i['id']:
            more_to_hear = i
        elif "artist-bio" in i['id']:
            bio = i
        elif "similar-artists" in i['id']:
            similar = i
    
    try:
        result['title'] = artist_detail['items'][0]['title']
    except:
        pass
    
    try:
        image_url = artist_detail['items'][0]['artwork']['dictionary']['url']
        image_width = artist_detail['items'][0]['artwork']['dictionary']['width']
        image_height = artist_detail['items'][0]['artwork']['dictionary']['height']
        result['image'] = get_cover(image_url, image_width, image_height)
    except:
        pass
            
    try:
        result['latest'] = latest_and_top['pinnedLeadingItem']['item']['segue']['actionMetrics']['data'][0]['fields']['actionUrl']
    except:
        pass

    try:
        for i in latest_and_top['items']:
            result['top'].append(i['segue']['actionMetrics']['data'][0]['fields']['actionUrl'])
    except:
        pass

    try:
        for i in albums['items']:
            result['albums'].append(i['segue']['actionMetrics']['data'][0]['fields']['actionUrl'])
    except:
        pass

    try:
        result['singles_and_EP'] = get_all_singles(url)
    except:
        pass

    try:
        for i in playlists['items']:
            result['playlists'].append(i['segue']['actionMetrics']['data'][0]['fields']['actionUrl'])
    except:
        pass

    try:
        for i in videos['items']:
            result['videos'].append(i['segue']['actionMetrics']['data'][0]['fields']['actionUrl'])
    except:
        pass

    try:
        for i in similar['items']:
            result['similar'].append(i['segue']['actionMetrics']['data'][0]['fields']['actionUrl'])
    except:
        pass

    try:
        for i in appears_on['items']:
            result['appears_on'].append(i['segue']['actionMetrics']['data'][0]['fields']['actionUrl'])
    except:
        pass

    try:
        for i in more_to_see['items']:
            result['more_to_see'].append(i['segue']['actionMetrics']['data'][0]['fields']['actionUrl'])
    except:
        pass

    try:
        for i in more_to_hear['items']:
            result['more_to_hear'].append(i['segue']['actionMetrics']['data'][0]['fields']['actionUrl'])
    except:
        pass

    try:
        result['about'] = bio['items'][0]['modalPresentationDescriptor']['paragraphText']
    except:
        pass

    try:
        result['info'] = bio['items'][0]['modalPresentationDescriptor']['headerSubtitle']
    except:
        pass

    return result
