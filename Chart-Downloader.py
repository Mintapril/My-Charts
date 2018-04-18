import requests
import os
from bs4 import BeautifulSoup
import re
from urllib import request

url_patterns = re.compile('/Mintapril/My-Charts/tree/master/.*')
def run():
    r = requests.get("https://github.com/Mintapril/My-Charts")
    r = r.text
    soup = BeautifulSoup(r, "lxml")
    urls = soup.find_all("a", href=url_patterns)
    url_list = []
    for url in urls:
        url = "https://github.com/" + url["href"]
        url_list.append(url)
    return url_list

def resolve(url_list):
    download_url_patterns = re.compile("/Mintapril/My-Charts/blob/master/.*")
    n = 0
    for url in url_list:
        r = requests.get(url)
        r = r.text
        soup = BeautifulSoup(r, "lxml")
        download_urls = soup.find_all("a", href=download_url_patterns)
        dict_file = {}
        for url_ in download_urls:
            url = "https://github.com/" + url_["href"].replace("blob", "raw")
            file_name = url_.get_text()
            dict_file[url] = file_name
        for url in dict_file:
            if ".sm" in url:
                r = requests.get(url)
                r = r.text
                for line in r.split("\n"):
                    if "#TITLE:" in line:
                        title = line.replace("#TITLE:", "").strip(";")
                    if "#ARTIST:" in line:
                        artist = line.replace("#ARTIST:", "").strip(";")
                dir_name = artist + " - " + title + "(mint)"
                if "\\" or "/" or ":" or "?" or '"' or "<" or ">" or "|" or "*" in dir_name:
                    dir_name = dir_name.replace("\\", "").replace(
                        "/", "").replace(":", "").replace("?", "").replace(
                            '"', "").replace("<", "").replace(">", "").replace(
                                "|", "").replace("*", "")
                os.makedirs(os.path.join("My-Charts", dir_name), exist_ok=True)
                for url in dict_file:
                    if ".old" in url:
                        continue
                    if os.path.exists(os.path.join("My-Charts", dir_name, dict_file[url])) is True:
                        continue
                    request.urlretrieve(url, os.path.join("My-Charts", dir_name, dict_file[url]))
        n = n + 1
        print("已下载" + str(n) + "首歌曲", end="\r")       


def get_md5(file_path):
  md5 = None
  if os.path.isfile(file_path):
    f = open(file_path,'rb')
    md5_obj = hashlib.md5()
    md5_obj.update(f.read())
    hash_code = md5_obj.hexdigest()
    f.close()
    md5 = str(hash_code).lower()
  return md5


if __name__ == '__main__':
    url_list = run()
    resolve(url_list)

