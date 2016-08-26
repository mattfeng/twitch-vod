#!/usr/bin/env python

import requests
import json
import datetime
import subprocess as sp
import sys
import signal

# check if the stream is online
liveurl = 'https://api.twitch.tv/kraken/streams/summit1g/'
livestream_url = 'http://twitch.tv/summit1g'
stream_req = requests.get(liveurl)
stream_data = json.loads(stream_req.text)

live = False
if stream_data['stream'] != None:
    live = True
    output = '[0] http://twitch.tv/summit1g/ (live)'
    print output

# get the VODs
NUM_VIDS = 10
if len(sys.argv) == 2:
    NUM_VIDS = int(sys.argv[1])

url = ('https://api.twitch.tv/kraken/channels/summit1g/videos?' + \
       'limit=%s&broadcasts=true') % NUM_VIDS

req = requests.get(url)
urldata = json.loads(req.text)

links = []
for i in xrange(NUM_VIDS):
    vid_info = urldata['videos'][i]
    vod_title = vid_info['title']
    vod_url = vid_info['url'].replace('secure.', '').replace('https', 'http')
    vod_game = vid_info['game']

    links.append(vod_url)

    vod_length = vid_info['length']
    vod_length_readable = datetime.timedelta(seconds=vod_length)
    output = '[%s] %s - %s (%s)' % (i + 1, vod_url[-11:], vod_game, vod_length_readable)
    print output

vod_index = int(raw_input('>>> ')) - 1
if vod_index == -1 and live:
    sp.call('livestreamer -p mpv %s source' % livestream_url, shell=True)
    quit()

sp.call('livestreamer --player-passthrough hls -p mpv %s source' \
        % links[vod_index], shell=True)

