#!/usr/bin/env python

import sys, getopt, requests, datetime, urllib, grequests


def call_reqs(i, len_all_urls, inner_urls, file_name):
    reqs = [ua[0] for ua in inner_urls]
    artists = [ua[1] for ua in inner_urls]
    
    sys.stdout.write(datetime.datetime.now().strftime('%d-%m-%Y-%H:%M:%S') + ' - ' + str(i) + '/' + str(len_all_urls) + ' ')

    resps = grequests.map(reqs)
    print '!'

    for j, resp in enumerate(resps):
        if not resp:
            continue

        if resp.status_code == requests.codes.ok:
            print artists[j], [ k['name'] for k in resp.json()['toptags']['tag'] if int(k['count']) >= 66 ]
            #with open(file_name, 'a+') as f:
            #    f.write('\n\n# ' + artists[j] + '\n')
            #    f.write(resp.text)
            #    f.flush()
            #    f.close()
        else:
            print unicode(artists[j], 'utf-8') + ' data could not be retrieved...\n\n' + resp.text


def main(argv=None):

    query_url = 'http://ws.audioscrobbler.com/2.0/?method=artist.gettoptags&artist={0}&api_key=b3cfcbda3d913b3d306609617e157b35&format=json'

    file_name = 'artists-genres-result-' + datetime.datetime.now().strftime('%d-%m-%Y-%H:%M:%S') + '.txt'

    all_urls = []
    inner_urls = []
    with open('artists-genres.txt', 'r') as input_file:
        
        artists = input_file.readlines()
        i = 0
        len_all_urls = (len(artists) / 100) + 1
        print 'We are going to make parallel requests ' + str(len_all_urls) + ' times'

        for artist in artists:
            artist = artist.replace('\n', '').strip()

            url = query_url.replace('{0}', unicode(urllib.quote(artist, ''), 'utf-8'))
            inner_urls.append( (grequests.get(url), artist) )

            if len(inner_urls) == 100:
                i += 1
                call_reqs(i, len_all_urls, inner_urls, file_name)
                inner_urls = []

        if inner_urls:
            i += 1
            call_reqs(i, len_all_urls, inner_urls, file_name)
            inner_urls = []
        

if __name__ == "__main__":
    sys.exit(main())


