# -----IMPORTS-----
import spotify
import keys
import urllib.parse, urllib.request, urllib.error, json

from google_images_search import GoogleImagesSearch
gapi = keys.google_api_key
cx = keys.google_project_cx
gis = GoogleImagesSearch(gapi, cx)


# -----FUNCTIONS-----

def get_an_image(q, num=1, offset=1, filename="imagelinks.csv"):
    """Parameters: q=query string
    Returns: None, write links to images in imagelinks.csv"""
    args = {"cx": cx, "q": q, "searchType": "image", "num": num, "start": offset, "safe": "off", "key": gapi, "alt": "json"}
    paramstr = urllib.parse.urlencode(args)

    baseurl = "https://customsearch.googleapis.com/customsearch/v1"
    request = "{}?{}".format(baseurl, paramstr)
    
    with urllib.request.urlopen(request) as response:
        response_str = response.read().decode()
        response_json = json.loads(response_str)

    with open(filename, "a", encoding="utf-8") as f:
        for picnumber in range(num):
            f.write(response_json["items"][picnumber]["link"])
            f.write("\n")
    
    return None


def clear_links(filename="imagelinks.csv"):
    """ Parameters: filename to clear
    Returns: None, empties file
    """
    with open(filename, "w", encoding="utf-8") as f:
        f.write("")

    return None


def images_based_on_list(keywordlist, filename="imagelinks.csv", vibe=""):
    """ Parameters: strings, vibe = string that can narrow down aesthetic of searches
    Returns: None, writes linkes of images into filename
    """
    for word in keywordlist:
        aestheticword = "aesthetic pinterest {} {}".format(word, vibe)
        get_an_image(aestheticword, filename=filename)

    return None


def main():
    x = ["love", "falling", "haze", "karma", "wanted"]
    clear_links()
    images_based_on_list(x, vibe="pink")