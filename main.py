from flask import Flask, render_template, request, redirect, url_for
import requests # For getting Steam ID


app = Flask(__name__)

@app.route("/")
def greeter():
    """Displays the greeter website."""
    return render_template("index.html")

@app.route("/", methods=["POST"])
def on_input_field():
    """Gets called whenever something is input on the input field in the greeter webpage."""

    steamID = get_steam_id(request.form["dotaID"])

    if steamID > 0:
        return redirect(url_for("profile", steamID = steamID), 302)
    else:
        return render_template("index.html", error="Failed to get Steam ID. Did you type it correctly?")


def get_steam_id(field_input):
    """Tries to get a valid SteamID to use with the opendota API with the provided input."""

    request_payload = {"action": "steamID", "id":field_input}
    steamid_request = requests.get("http://steamid.co/php/api.php", params=request_payload)
    
    try:
        if "error" in steamid_request.json().keys():
            return -1
        else:
            return int(steamid_request.json()["steamID64"]) - 76561197960265728 # Converts ID64 to ID32, which OpenDota uses for the API calls
    except ValueError:
        return -2

@app.route("/<int:steamID>")
def profile(steamID):
    return render_template("index.html")
