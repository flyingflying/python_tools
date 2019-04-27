#!/usr/bin/python
#coding=utf-8

"""
This tool is designed for downloading pictures from 
baidu tieba (https://tieba.baidu.com/index.html).
Since it is a web spider, this tool may not work 
well in the future. 
"""

import requests, time, os
from bs4 import BeautifulSoup
from progressbar import ProgressBar 

tieba_url = "https://tieba.baidu.com/p/4954852253"

def get_pics_list( tieba_url ):

	def download_parse_html_page( url ):
		html_content = requests.get( url )
		if html_content.status_code != 200:
			raise Exception( "Please check tieba url." )
		soup = BeautifulSoup( html_content.text, "lxml" )
		return soup

	def get_img_list( soup ):
		img_list = soup.select(".BDE_Image")
		img_list = [ "http://imgsrc.baidu.com/forum/pic/item/" + img["src"].split("/")[-1] 
		             for img in img_list]
		return img_list	

	soup = download_parse_html_page(tieba_url)
	pages = int(soup.select(".l_reply_num > span")[1].text)
	img_list = get_img_list(soup)

	for i in range(1, pages):
		url = tieba_url + "?pn=%d" % (i + 1)
		soup = download_parse_html_page( url )
		img_list.extend( get_img_list(soup) )
		time.sleep(1)

	return img_list

def download_pics( img_url, save_path ):
	img_content = requests.get(img_url, stream = True)
	with open( save_path, "wb" ) as f:
		for chunk in img_content.iter_content( chunk_size = 32 ):
			f.write(chunk)

if __name__ == '__main__':
	img_list = get_pics_list( tieba_url )

	progress = ProgressBar()

	os.mkdir("./pics")
	for i in progress( range( len(img_list) ) ):
		download_pics( img_list[i], "./pics/%03d.jpg" % (i + 1) )
		time.sleep(1)

	# for i, img in enumerate(img_list):
	# 	download_pics( img_url, "./pics/%03d.jpg" % (i + 1) )
	# 	time.sleep(1)

