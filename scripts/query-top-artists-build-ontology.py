#!/usr/bin/env python

import sys, getopt, requests, datetime, urllib, json


def main(argv=None):

    countries_get_lastfm = []
    metros_get_lastfm = []

    with open('cities.txt', 'r') as input_file:
        countries_cities = input_file.readlines()

        for cc in countries_cities:
            cc = cc.replace('\n', '').strip()

            if cc and cc[0] != '-':
                countries_get_lastfm.append(cc)

            if cc and cc[0] == '-':
                c = countries_get_lastfm[len(countries_get_lastfm) - 1]
                metros_get_lastfm.append( (c, cc[1:].strip()) )


    artists = []
    with open('artists-with-uri.txt', 'r') as input_file:
        artists = json.loads(input_file.read())

    locations = []
    with open('locations-with-uri.txt', 'r') as input_file:
        locations = json.loads(input_file.read())

    query_url = 'http://ws.audioscrobbler.com/2.0/?method=geo.gettopartists&country={0}&api_key=b3cfcbda3d913b3d306609617e157b35&format=json&limit=200'

    i = 0

    for country in countries_get_lastfm:
        resp = requests.get(query_url.replace('{0}', unicode(urllib.quote(country, ''), 'utf-8')))

        if resp.status_code == requests.codes.ok:
            if resp.json().get('topartists'):
                
                for k in resp.json()['topartists']['artist']:

                    artist_uri = artists.get(k['name'].lower())
                    if artist_uri and locations.get(country):
                        i += 1
                        print '\n<' + artist_uri + '> mbo:top_player_in mbo:Relation_Artist_Location_' + str(i) + ' .'
                        print  'mbo:Relation_Artist_Location_' + str(i) + ' rdf:type mbo:Relation_Artist_Location , :NamedIndividual ;'
                        print  '                      mbo:has_location <' + locations.get(country) + '> ;'
                        print  '                      mbo:has_listeners ' + k['listeners'] + ' .'
            #else:
            #    print 'Error on ', country, ' - ', resp.json()
            

    query_url = 'http://ws.audioscrobbler.com/2.0/?method=geo.getmetroartistchart&country={0}&metro={1}&api_key=b3cfcbda3d913b3d306609617e157b35&format=json&limit=200'

    for country_metro in metros_get_lastfm:
        country = unicode(urllib.quote(country_metro[0], ''), 'utf-8')
        metro = unicode(urllib.quote(country_metro[1], ''), 'utf-8')
        resp = requests.get(query_url.replace('{0}', country).replace('{1}', metro))

        if resp.status_code == requests.codes.ok:
            
            resp_json = resp.json()
            if resp_json.get('topartists') and resp_json['topartists'].get('artist'):
                for k in resp_json['topartists']['artist']:
                    artist_uri = artists.get(k['name'].lower())
                    if artist_uri and locations.get(metro):
                        i += 1
                        print '\n<' + artist_uri + '> mbo:top_player_in mbo:Relation_Artist_Location_' + str(i) + ' .'
                        print  'mbo:Relation_Artist_Location_' + str(i) + ' rdf:type mbo:Relation_Artist_Location , :NamedIndividual ;'
                        print  '                      mbo:has_location <' + locations.get(metro) + '> ;'
                        print  '                      mbo:has_listeners ' + k['listeners'] + ' .'
                        
            #else:
            #    print 'Error on ', country, ' - ', resp.json()

    
    #file_name = 'top-artists-result' + datetime.datetime.now().strftime('%d-%m-%Y-%H:%M:%S') + '.txt'
    #with open(file_name, 'a+') as f:
        #for k in set_artists_countries:
        #    f.write(k[0].encode('utf8') + ' - ' + str(k[1]) + '\n')
        #for k in set_artists_metros:
        #    f.write(k[0].encode('utf8') + ' - ' + str(k[1]) + '\n')
        #f.flush()

if __name__ == "__main__":
    sys.exit(main())


