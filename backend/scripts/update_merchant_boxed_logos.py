''' environment.py '''
import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

host = os.environ.get('MONGODB_HOST')
port = int(os.environ.get('MONGODB_PORT', 27017))

db_connection = MongoClient(host, port)

base_url = 'https://qwikwire-static-assets.s3-ap-southeast-1.amazonaws.com/client/{}/dashboard/{}-2x.png'
boxed_logos = [
    {
        'merchantId': '2ndoffice',
        'url': base_url.format('2ndoffice', '2nd-office')
    },
    {
        'merchantId': 'aboitizland',
        'url': base_url.format('aboitizland', 'aboitizland')
    },
    {
        'merchantId': 'accentline',
        'url': base_url.format('accentline', 'accentline')
    },
    {
        'merchantId': 'alphalandbalesin',
        'url': base_url.format('alphalandbalesin', 'alphaland-balesin-island-club')
    },
    {
        'merchantId': 'alphalandcityclub',
        'url': base_url.format('alphalandcityclub', 'alphaland-city-club')
    },
    {
        'merchantId': 'alveo',
        'url': base_url.format('alveo', 'alveo')
    },
    {
        'merchantId': 'amaia',
        'url': base_url.format('amaia', 'amaia-land')
    },
    {
        'merchantId': 'antel',
        'url': base_url.format('antel', 'antel-tanza')
    },
    {
        'merchantId': 'appleone',
        'url': base_url.format('appleone', 'apple-one')
    },
    {
        'merchantId' : 'avida',
        'url': base_url.format('avida', 'avida-land'),
    },
    {
        'merchantId' : 'axeia',
        'url': base_url.format('axeia', 'axeia'),
    },
    {
        'merchantId' : 'ayalalandpremier',
        'url': base_url.format('ayalalandpremier', 'ayala-land-premier'),
    },
    {
        'merchantId' : 'bookartpress',
        'url': base_url.format('bookartpress', 'book-art-press'),
    },
    {
        'merchantId' : 'centralcountry',
        'url': base_url.format('centralcountry', 'central-country-estate')
    },
    {
        'merchantId' : 'centuryproperties',
        'url': base_url.format('centuryproperties', 'century-properties')
    },
    {
        'merchantId' : 'citiglobal',
        'url': base_url.format('citiglobal', 'citiglobal')
    },
    {
        'merchantId' : 'diamondmediapress',
        'url': base_url.format('diamondmediapress', 'diamond-media-press')
    },
    {
        'merchantId' : 'doubledragon',
        'url': base_url.format('doubledragon', 'doubledragon')
    },
    {
        'merchantId' : 'edwardbalda',
        'url': base_url.format('edwardbalda', 'edward-balda')
    },
    {
        'merchantId' : 'empireeast',
        'url': base_url.format('empireeast', 'empire-east')
    },
    {
        'merchantId' : 'gramercy',
        'url': base_url.format('gramercy', 'gramercy')
    },
    {
        'merchantId' : 'htland',
        'url': base_url.format('htland', 'htland')
    },
    {
        'merchantId' : 'italpinas',
        'url': base_url.format('italpinas', 'italpinas')
    },
    {
        'merchantId' : 'knightsbridge',
        'url': base_url.format('knightsbridge', 'knightsbridge')
    },
    {
        'merchantId' : 'landco',
        'url': base_url.format('landco', 'landco')
    },
    {
        'merchantId' : 'magellansolutions',
        'url': base_url.format('magellansolutions', 'magellan-solutions')
    },
    {
        'merchantId' : 'megamilleniumroyalcorp',
        'url': base_url.format('megamillenniumroyalcorp', 'mega-millennium')
    },
    {
        'merchantId' : 'ndvlawoffice',
        'url': base_url.format('ndvlawoffice', 'ndv-law-offices')
    },
    {
        'merchantId' : 'northpineland',
        'url': base_url.format('northpineland', 'northpine-land')
    },
    {
        'merchantId' : 'phirstparkhomes',
        'url': base_url.format('phirstparkhomes', 'phirst-park-homes')
    },
    {
        'merchantId' : 'revolutionprecrafted',
        'url': base_url.format('revolutionprecrafted', 'revolution-precrafted')
    },
    {
        'merchantId' : 'sbcph',
        'url': base_url.format('sbcph', 'sbcph-incorporated')
    },
    {
        'merchantId' : 'socland',
        'url': base_url.format('socland', 'soc-land'),
    },
    {
        'merchantId' : 'strattonpress',
        'url': base_url.format('strattonpress', 'stratton-press')
    },
    {
        'merchantId' : 'theflatsamorsolo',
        'url': base_url.format('theflatsamorsolo', 'the-flats')
    },
    {
        'merchantId' : 'torrelorenzo',
        'url': base_url.format('torrelorenzo', 'torre-lorenzo')
    },
    {
        'merchantId' : 'vistaresidences',
        'url': base_url.format('vistaresidences', 'vista-residences')
    }
]

directory_db = db_connection.get_database('directory')
merchants_collection = directory_db.get_collection('merchants')

print('Starting merchants boxed logo update...')
for item in boxed_logos:
    query = {'merchantId': item['merchantId']}
    set_property = {
        '$set': { 'config.dashboard.boxedLogoImgSrc': item['url'] }
    }
    update_result = merchants_collection.update_one(query, set_property)
    update_msg = '{} - {}'.format(
        'DONE--' if update_result.modified_count == 1 else 'ERROR-',
        item['merchantId']
    )
    print(update_msg)

print('Merchants boxed logo update has been completed')
