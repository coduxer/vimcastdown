import wget
import json
import os
import argparse
from urllib.parse import urlparse

parser = argparse.ArgumentParser()
parser.add_argument('-o', '--outputfolder', default='.', help='')
parser.add_argument('-i', '--inputjson', default='./index.json', help='')
params = parser.parse_args()
with open(params.inputjson, 'r') as f:
    results = json.load(f)

savepath = params.outputfolder
for key in results:
    filename = key + '_'
    url = results[key].get('quicktime', results[key].get('mp4', None))
    if url is None:
        raise Exception('error')

    url = url['url']
    urlpath = urlparse(url)
    filename += os.path.basename(urlpath.path)
    fullpath = savepath + filename
    if not os.path.exists(fullpath):
        print('file: {} is already exist'.format(filename))
        continue

    print('url = {}'.format(url))
    print('filename = {}'.format(filename))
    wget.download(url, fullpath)
    print('')
