import spotify as sp
import google

from flask import Flask, render_template, request

# Use flask --debug run to run code
# Create an instance of Flask
app = Flask(__name__)


# Create a view function for /
# Main page

@app.route("/")
def main():
    return render_template("base.html")


# View for the loading screen /loading

@app.route("/loading", methods=["GET", "POST"])
def loading_page():
    if request.method == "POST":
        id = request.form["spotify id"]
        idtype = request.form["typeofid"]
        if idtype == "album":
            cwdict = sp.album_common_words(id)
            cwtuplelist = sp.sort_words(cwdict)
            cwlist = sp.keywords_to_list(cwtuplelist)
            return cwlist
        elif idtype == "playlist":
            cwdict = sp.playlist_common_words(id)
            cwtuplelist = sp.sort_words(cwdict)
            cwlist = sp.keywords_to_list(cwtuplelist)
            return cwlist
    else:
        return "wrong HTTP request"

# Create a view function for /results

# @app.route("/results", methods=["GET", "POST"])
# def submit_page():
#     if request.method == "POST":
#         place = request.form["place"]
#         max_results = int(request.form["max_results"])
#         radius = float(request.form["radius"])
#         if "sort" in request.form:
#             sort = True
#         else:
#             sort = False
#         listobjects = functions.wikipedia_locationsearch(place, max_results, radius, sort)
#         # return [place, max_results, radius, sort]
#         # return listobjects
#         return render_template("results.html", listobjects=listobjects, place=place)
#     else:
#         return "Wrong HTTP Method"