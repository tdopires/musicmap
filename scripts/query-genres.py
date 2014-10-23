#!/usr/bin/env python

import sys, getopt, requests, datetime, urllib, grequests, json

def call_reqs(i, len_all_urls, inner_urls, genres_set, artist_genres):
    reqs = [ua[0] for ua in inner_urls]
    artists = [ua[1] for ua in inner_urls]
    
    sys.stdout.write(datetime.datetime.now().strftime('%d-%m-%Y-%H:%M:%S') + ' - ' + str(i) + '/' + str(len_all_urls) + ' ')

    resps = grequests.map(reqs)
    print '!'

    for j, resp in enumerate(resps):
        if not resp:
            continue

        if resp.status_code == requests.codes.ok:
            if resp.json()['toptags'].get('tag') and isinstance(resp.json()['toptags']['tag'], list):
                genres = [ k['name'] for k in resp.json()['toptags']['tag'] if k['count'] and int(k['count']) >= 66 ]

                for genre in genres:
                    genres_set.add(genre)

                artist_genres[artists[j]] = genres
                
        else:
            print unicode(artists[j], 'utf-8') + ' data could not be retrieved...\n\n' + resp.text


def main(argv=None):

    query_url = 'http://ws.audioscrobbler.com/2.0/?method=artist.gettoptags&artist={0}&api_key=b3cfcbda3d913b3d306609617e157b35&format=json'

    file_name = 'artists-genres-result-' + datetime.datetime.now().strftime('%d-%m-%Y-%H:%M:%S') + '.txt'

    genres_set = set([])
    artist_genres = {}

    artists_uris = []
    with open('artists-with-uri.txt', 'r') as input_file:
        artists_uris = json.loads(input_file.read())

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
                call_reqs(i, len_all_urls, inner_urls, genres_set, artist_genres)
                inner_urls = []

        if inner_urls:
            i += 1
            call_reqs(i, len_all_urls, inner_urls, genres_set, artist_genres)
            inner_urls = []


    #for genre in genres_set:
    #    print 'mbo:' + genre.replace(' ', '_').lower() + ' rdf:type <http://purl.org/ontology/mo/Genre> , :NamedIndividual ; '
    #    print '                rdfs:label "' + genre.title() + '"^^xsd:string .'

    for artist_name in artist_genres.keys():
        artist_uri = artists_uris.get(artist_name.lower())
        if artist_uri:
            genres = artist_genres[artist_name]

            for genre in genres:
                n_genre = genre.replace('/', '_').replace('-', '_')
                if n_genre.title() in ["Folk Rock", "Dance", "Heavy Metal", "Classic Rock", "Alternative Rock", "Mpb", "Electrohouse", "Folk", "Indie Rock", "Indie Pop", "Instrumental", "Metalcore", "Indie", "Punk Rock", "Salsa", "Opera", "Trap", "Rock", "Dubstep", "Blues", "Techno", "Pop Rock", "Gospel", "Punk", "Hard Rock", "Electronic", "Forro", "Classical", "Death Metal", "Samba", "Rap", "Trance", "Hip-Hop", "Metal", "Jazz", "Hip Hop", "Country", "Pop", "Funk", "Sertanejo", "Ska", "Thrash Metal", "Orchestral", "Bossa Nova", "Reggae"]:
                    print '<' + artist_uri + '> <mbo:from_genre> mbo:' + genre.replace(' ', '_').lower() + ' .'
        

if __name__ == "__main__":
    sys.exit(main())


