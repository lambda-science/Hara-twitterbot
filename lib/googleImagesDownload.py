import time
import sys
import os
import urllib.request
from urllib.request import Request, urlopen
from urllib.request import URLError, HTTPError
from random import choice

# Downloading entire Web Document (Raw Page Content)
def download_page(url):
        try:
            headers = {}
            headers[
                'User-Agent'] = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
            req = urllib.request.Request(url, headers=headers)
            resp = urllib.request.urlopen(req)
            respData = str(resp.read())
            return respData
        except Exception as e:
            print(str(e))

# Finding 'Next Image' from the given raw page
def _images_get_next_item(s):
    start_line = s.find('rg_di')
    if start_line == -1:  # If no links are found then give an error!
        end_quote = 0
        link = "no_links"
        return link, end_quote
    else:
        start_line = s.find('"class="rg_meta"')
        start_content = s.find('"ou"', start_line + 1)
        end_content = s.find(',"ow"', start_content + 1)
        content_raw = str(s[start_content + 6:end_content - 1])
        return content_raw, end_content


# Getting all links with the help of '_images_get_next_image'
def _images_get_all_items(page):
    items = []
    while True:
        item, end_content = _images_get_next_item(page)
        if item == "no_links":
            break
        else:
            items.append(item)  # Append all the links in the list named 'Links'
            time.sleep(0.1)  # Timer could be used to slow down the request for image downloads
            page = page[end_content:]
    return items


############## Main Program ############

# Download Image Links and a single image
def downloadSingleImage(search_keyword):
	errorCount = 0
	dir_name = search_keyword

	# make a search keyword  directory
	try:
	    os.makedirs(dir_name)
	except OSError as e:
	    if e.errno != 17:
	        raise
	        # time.sleep might help here
	    pass

	j = 0
	url = 'https://www.google.com/search?safe=active&q=' + search_keyword + '&espv=2&biw=1366&bih=667&site=webhp&source=lnms&tbm=isch' + '&sa=X&ei=XosDVaCXD8TasATItgE&ved=0CAcQ_AUoAg'
	raw_html = (download_page(url))
	time.sleep(0.1)
	items = _images_get_all_items(raw_html)

	## To save imges to the same directory
	# IN this saving process we are just skipping the URL if there is any error
	k = 0
	while (k < 1):
	    requestedImage = choice(items)
	    try:
	        req = Request(requestedImage, headers={
	            "User-Agent": "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"})
	        response = urlopen(req, None, 15)
	        image_name = str(requestedImage[(requestedImage.rfind('/'))+1:])
	        if '?' in image_name:
	            image_name = image_name[:image_name.find('?')]
	        if ".jpg" in image_name or ".png" in image_name or ".jpeg" in image_name or ".svg" in image_name:
	            output_file = open(dir_name + "/" + str(k + 1) + ". " + image_name, 'wb')
	        else:
	            output_file = open(dir_name + "/" + str(k + 1) + ". " + image_name + ".jpg", 'wb')
	            image_name = image_name + ".jpg"

	        data = response.read()
	        output_file.write(data)
	        response.close()

	        k = k + 1

	    except IOError:  # If there is any IOError

	        errorCount += 1
	        print("IOError on image " + str(k + 1))
	        k = k + 1

	    except HTTPError as e:  # If there is any HTTPError

	        errorCount += 1
	        print("HTTPError" + str(k))
	        k = k + 1
	    except URLError as e:

	        errorCount += 1
	        print("URLError " + str(k))
	        k = k + 1

if __name__ == "__main__":
	# Taking command line arguments from users
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('-k', '--keywords', help='delimited list input', type=str, required=True)
	args = parser.parse_args()
	downloadSingleImage(args.keywords)