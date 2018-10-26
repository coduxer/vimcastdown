import wget
import json
import os
import argparse
from urllib.request import urlopen
from urllib.parse import urlparse

jsonurl = 'http://media.vimcasts.org/videos/index.json'

parser = argparse.ArgumentParser()
parser.add_argument('-o', '--outputfolder', default='.',
                    help='Set output foldet to which all the files\
                    will be saved')
parser.add_argument('-i', '--inputjson', default=None,
                    help='Manual set input.json file. \
                    By default the file is taken from: ' + jsonurl)
params = parser.parse_args()
if params.inputjson:
    with open(params.inputjson, 'r') as f:
        results = json.load(f)
else:
    results = json.load(urlopen(jsonurl))

savepath = params.outputfolder
length = len(str(len(results)))
len_format = '0{}d'.format(length)
for key in results:
    filename = format(int(key), len_format) + '_'
    url = results[key].get('quicktime', results[key].get('mp4', None))
    if url is None:
        raise Exception('error')

    url = url['url']
    urlpath = urlparse(url)
    filename += os.path.basename(urlpath.path)
    fullpath = savepath + filename
    if os.path.exists(fullpath):
        print('file: {} is already exist'.format(filename))
        continue

    print('url = {}'.format(url))
    print('filename = {}'.format(filename))
    wget.download(url, fullpath)
    print('')
