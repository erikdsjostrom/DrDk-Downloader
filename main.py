import sys
import os
import re
import json
from urllib.request import urlretrieve
from urllib.request import urlopen


def main(url):
    def download(download_url, title):
        file_name = "{}.mp4".format(title)
        u = urlopen(download_url)
        try:
            # This is an ugly hack that seems to fix an issue
            # where it wouldn't create a file.
            # I should probably fix this ¯\ (ツ) /¯
            f = open(file_name, 'a+')
        except:
            # print("Can't open file")
            pass
        finally:
            f = open(file_name, 'wb')
        meta = u.info()
        file_size = int(meta["Content-Length"])
        print("Downloading: {} (Bytes: {})".format(title, file_size))

        file_size_dl = 0
        block_sz = 8192
        while True:
            buffer = u.read(block_sz)
            if not buffer:
                break

            file_size_dl += len(buffer)
            f.write(buffer)
            status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl *
                     100. / file_size)
            status = status + chr(8)*(len(status)+1)
            sys.stdout.write("\r" + status)
            sys.stdout.flush()

        f.close()

    try:
        sock = urlretrieve(url)
    except:
        print("[!] That's not a valid url")
        sys.exit()
    #Reads in the entire source of the page
    print("[+] Valid url, let's get to work")
    page_source = open(sock[0], encoding="utf-8").read()

    #Regex to find the name of the artist
    RE = re.compile('data-programme-name="(.*?)"')
    title = RE.findall(page_source)[0]

    #Regex for the the json link for the episode
    RE = re.compile('data-resource="(.*?)"')
    try:
    #Get the json link
        video_json_link = RE.findall(page_source)[0]
    except:
        #If it does not find a json link, there is no page
        print("[!] That's not a valid url")
        sys.exit()
    #Now it's time to get the json, parse it, and download the video
    sock = urlretrieve(video_json_link)
    video_json = open(sock[0], encoding="ISO-8859-1").read()
    info = json.loads(video_json)
    #I take the first link because thats the highest quality
    video_uri = info["Links"][0]["Uri"]

    download(video_uri, title)

    return None

if __name__ == '__main__':
    os.system('clc' if os.name == "nt" else 'clear')  # Clear the terminal
    url = input("[?] Hand me the url: ")
    main(url)
