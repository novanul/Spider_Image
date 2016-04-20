
# -*- coding: utf_8 -*-

import os
import re
# import threading

from urllib import request
# from urllib import parse

from collections import deque

dir_win      = r'archive'

url_sum      = 0
url_index    = r'http://www.58pic.com/tupian/caihaibao.html'
url_ready    = deque()
url_analysed = set()

image_sum    = 0
image_had    = 0
image_ready  = []

regex_url_direct   = re.compile(r'(?<=href=")http://www\.58pic\.com/[/\-%\w]+?[/(\.html)]+?(?=")')
regex_url_redirect = re.compile(r'(?<=href=")/[/\-%\w]*?[/(\.html)]+?(?=")')
regex_img          = re.compile(r'(?<==")http://pic\.qiantucdn\.com/.*?(?=\.jpg!qt)')


def download_image_single(download_dirpath):# PATH
    global image_sum
    global image_had
    global image_ready


    try:
        os.makedirs(download_dirpath)
    except Exception:
        print('ERROR in dirpath!Maybe the dir had existed!That is {0}'.format(download_dirpath))
        image_ready = [] # useless?
        return None
        #if(download_dirpath == ''):
        #   download_dirpath = r'archive/unknown'

    for i,download_url in enumerate(image_ready):
        try:
            download_respond = request.urlopen(download_url) # This code need a timeout to word steadily,set timeout to 100s.
            download_jpg = download_respond.read()
        except Exception :
            print("ERROR in download")
            continue
        else:
            try:
                with open(download_dirpath + r'/image{0}.jpg'.format(image_had + i), 'wb') as file_jpg:
                    file_jpg.write(download_jpg)
            except Exception:
                print("ERROR in IO")
                #raise
                continue
            else:
                image_sum += 1
                print('--------Download Image Of {0}--------'.format(image_sum))

            """
            try:
                file_jpg = open(download_dirpath + r'/image{0}.jpg'.format(image_had + i), 'wb')
                file_jpg.write(download_jpg)
                file_jpg.close()
            except Exception:
                print("ERROR in IO")
                #raise
                continue
            finally:
                #file_jpg.close()
                image_sum += 1
                print('--------Download Image Of {0}--------'.format(image_sum))
            """

    print("----------{0} 's images had been download totally----------".format(download_dirpath))
    image_ready = [] # bad thing?
    image_had   = image_sum


def assign_threading():
    pass


def htmls_parse():
    global url_sum
    while url_ready:
        url_current = url_ready.popleft()
        if url_current in url_analysed:
            print("~~~~~~The page of {0} had been parsed before.~~~~~~".format(url_current))
            continue
        url_analysed.add(url_current)
        url_sum += 1
        print('----Start to parse {0}----'.format(url_current))

        try:
            url_response = request.urlopen(url_current)
        except Exception:
            print('ERROR in urlrequest')
            continue
        else:
            if 'html' not in url_response.getheader('Content-Type'):
                continue

        try:
            url_html = url_response.read().decode('GBK','ignore')
        except Exception:
            print('ERROR in decoding of GBK')
            continue

        url_content = regex_url_direct.findall(url_html)
        for url_aim in url_content:
            if url_aim not in url_analysed:
                url_ready.append(url_aim)

        url_content = regex_url_redirect.findall(url_html)
        for url_aim in url_content:
            url_aim = 'http://www.58pic.com' + url_aim
            if url_aim not in url_analysed:
                url_ready.append(url_aim)

        #Two types regexs cause that there may be more than two same urls appended into url_ready array

        image_content = regex_img.findall(url_html)
        if image_content != []:
            for image_aim in image_content:
                image_ready.append(image_aim + '_1024.jpg')

            print("---The {0}th page had been parse.---".format(url_sum))
            dir_aim = dir_win + '/' + url_current.split('/',3)[3].split('.')[0]
            download_image_single(dir_aim)
        else:
            print("~~{0} have no image!!~~".format(url_current))

        if(image_sum > 100000):#The max number of image
            print('--{0} jpgs got--'.format(image_sum))
            return None


def start_scratch():
    url_analysed.add(r'http://www.58pic.com/')
    #url_analysed.add(url_index)
    url_ready.append(url_index)
    os.makedirs('archive/unknown')
    htmls_parse()


start_scratch()


