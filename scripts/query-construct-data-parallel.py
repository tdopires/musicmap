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
            if resp.text == '# Empty NT\n':
                continue

            with open(file_name, 'a+') as f:
                f.write('\n\n# ' + artists[j] + '\n')
                f.write(resp.text)
                f.flush()
                f.close()
        else:
            print unicode(artists[j], 'utf-8') + ' data could not be retrieved...\n\n' + resp.text


def main(argv=None):

    query_url = 'http://linkedbrainz.org/sparql?default-graph-uri=&query=construct+%7B%0D%0A++%3FARTIST+a+%3Chttp%3A%2F%2Fpurl.org%2Fontology%2Fmo%2FMusicArtist%3E+.%0D%0A++%3FARTIST+a+%3FSOLO_OR_GROUP+.%0D%0A++%3FARTIST+%3Chttp%3A%2F%2Fwww.w3.org%2F2000%2F01%2Frdf-schema%23label%3E+%3FARTIST_NAME+.%0D%0A++%3FARTIST+%3Chttp%3A%2F%2Fxmlns.com%2Ffoaf%2F0.1%2Fname%3E+%3FARTIST_NAME+.%0D%0A++%3FARTIST+%3Chttp%3A%2F%2Fpurl.org%2Fontology%2Fmo%2Fbiography%3E+%3FARTIST_DOCUMENT+.%0D%0A%0D%0A++%3FRELEASE+a+%3Chttp%3A%2F%2Fpurl.org%2Fontology%2Fmo%2FRecord%3E+.%0D%0A++%3FRELEASE+%3Chttp%3A%2F%2Fwww.w3.org%2F2000%2F01%2Frdf-schema%23label%3E+%3FRECORD_TITLE+.%0D%0A++%3FRELEASE+%3Chttp%3A%2F%2Fpurl.org%2Fdc%2Felements%2F1.1%2Ftitle%3E+%3FRECORD_TITLE+.%0D%0A++%3FRELEASE+%3Chttp%3A%2F%2Fpurl.org%2Fontology%2Fmo%2Fpublisher%3E+%3FARTIST+.%0D%0A++%3FRELEASE+%3Chttp%3A%2F%2Fpurl.org%2Fontology%2Fmo%2Ftrack_count%3E+%3FTRACK_COUNT+.%0D%0A%0D%0A++%3FRELEASING+a+%3Chttp%3A%2F%2Fpurl.org%2Fontology%2Fmo%2FTrack%3E+.%0D%0A++%3FRELEASING+%3Chttp%3A%2F%2Fwww.w3.org%2F2000%2F01%2Frdf-schema%23label%3E+%3FRELEASING_TITLE+.%0D%0A++%3FRELEASING+%3Chttp%3A%2F%2Fpurl.org%2Fdc%2Felements%2F1.1%2Ftitle%3E+%3FRELEASING_TITLE+.%0D%0A++%3FRELEASE+%3Chttp%3A%2F%2Fpurl.org%2Fontology%2Fmo%2Ftrack%3E+%3FRELEASING+.%0D%0A%0D%0A%7Dwhere+%7B%0D%0A++%3FARTIST+a+%3Chttp%3A%2F%2Fpurl.org%2Fontology%2Fmo%2FMusicArtist%3E+.%0D%0A++%3FARTIST+a+%3FSOLO_OR_GROUP+.%0D%0A++%3FARTIST+%3Chttp%3A%2F%2Fxmlns.com%2Ffoaf%2F0.1%2Fname%3E+%3FARTIST_NAME+.%0D%0A++%3FARTIST+%3Chttp%3A%2F%2Fxmlns.com%2Ffoaf%2F0.1%2FisPrimaryTopicOf%3E+%3FARTIST_DOCUMENT+.%0D%0A++%0D%0A++%3FRELEASE+%3Chttp%3A%2F%2Fpurl.org%2Fontology%2Fmo%2Frecord%3E+%3Frecord+.%0D%0A++%3FARTIST+%3Chttp%3A%2F%2Fxmlns.com%2Ffoaf%2F0.1%2Fmade%3E+%3FRELEASE+.++%0D%0A++%3FRELEASE+%3Chttp%3A%2F%2Fpurl.org%2Fdc%2Felements%2F1.1%2Ftitle%3E+%3FRECORD_TITLE+.+%0D%0A++%3Frecord+%3Chttp%3A%2F%2Fpurl.org%2Fontology%2Fmo%2Ftrack_count%3E+%3FTRACK_COUNT+.%0D%0A++%3Frecord+%3Chttp%3A%2F%2Fpurl.org%2Fontology%2Fmo%2Ftrack%3E+%3Ftrack+.+++%0D%0A++%3Ftrack+%3Chttp%3A%2F%2Fpurl.org%2Fontology%2Fmo%2Fpublication_of%3E+%3FRELEASING+.%0D%0A++%3FRELEASING+%3Chttp%3A%2F%2Fpurl.org%2Fdc%2Felements%2F1.1%2Ftitle%3E+%3FRELEASING_TITLE+.%0D%0A%0D%0A++filter+%28%3FARTIST_NAME+%3D+%22{0}%22%29%0D%0A%7D&format=text%2Fplain&timeout=0&debug=on'

    file_name = 'result' + datetime.datetime.now().strftime('%d-%m-%Y-%H:%M:%S') + '.txt'

    all_urls = []
    inner_urls = []
    with open('artists.txt', 'r') as input_file:
        
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
            call_requests(i, len_all_urls, inner_urls)
            inner_urls = []
        

if __name__ == "__main__":
    sys.exit(main())


