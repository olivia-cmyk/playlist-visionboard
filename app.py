# -----IMPORTS-----
import spotify as sp
import googleimage as goo
from flask import Flask, render_template, request

# Use flask --debug run to run code

# -----FLASK INSTANCE-----
app = Flask(__name__)


# -----MAIN PAGE VIEW FUNCTION /-----
@app.route("/")
def main():
    return render_template("base.html")


# -----LOADING PAGE VIEW FUNCTION /LOADING-----
@app.route("/loading", methods=["GET", "POST"])
def loading_page():
    if request.method == "POST":
        id = request.form["spotify id"]
        idtype = request.form["typeofid"]

        # Album or Playlist?
        if idtype == "album":
            cwdict = sp.album_common_words(id)
        elif idtype == "playlist":
            cwdict = sp.playlist_common_words(id)

        # Incase the ID is wrong:
        if cwdict is None:
            return render_template("invalid.html")

        cwtuplelist = sp.sort_words(cwdict)
        cwlist = sp.keywords_to_list(cwtuplelist)
        return render_template("loading.html", cwlist=cwlist)
    else:
        return "Wrong HTTP Request. Try again here: http://yaushi20.pythonanywhere.com/"


# -----COLLAGE PAGE VIEW FUNCTION /IMAGES-----
@app.route("/images", methods=["GET", "POST"])
def collage_page():
    if request.method == "POST":
        keywordlist = goo.csvtolist()

        # Generate links to images
        goo.clear_links()  # Clear imagelinks.csv 
        print("Cleared Links")
        goo.images_based_on_list(keywordlist)

        urllist = goo.csvtolist("imagelinks.csv")
        randw = goo.randomnumberw(50)
        randh = goo.randomnumberh(50)
        return render_template("images.html", urllist=urllist, randw=randw, randh=randh)
    else:
        return "Wrong HTTP Request. Try again here: http://yaushi20.pythonanywhere.com/"