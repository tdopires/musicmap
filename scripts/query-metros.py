#!/usr/bin/env python

import sys, getopt, requests, datetime, urllib


def main(argv=None):

    query_url = 'http://ws.audioscrobbler.com/2.0/?method=geo.getmetros&country={0}&api_key=b3cfcbda3d913b3d306609617e157b35&format=json'

    with open('countries.txt', 'r') as input_file:
        countries = input_file.readlines()
        
    for country in countries:
        country = country.replace('\n', '').strip()

        resp = requests.get(query_url.replace('{0}', unicode(urllib.quote(country, ''), 'utf-8')))

        if resp.status_code == requests.codes.ok:
            print '\n\n' + country
            
            if isinstance(resp.json()['metros'], dict):
                
                r = resp.json()['metros']['metro']

                if isinstance(r, list):
                    for k in r:
                        print '- ' + k['name']
                else:
                    print '- ' + r['name']
        

if __name__ == "__main__":
    sys.exit(main())


