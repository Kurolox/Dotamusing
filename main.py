from flask import Flask, render_template, request
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

    if steamID:
        #TODO: Fetch opendota API
        return greeter()
    else:
        return greeter()


def get_steam_id(field_input):
    """Tries to get a valid SteamID to use with the opendota API with the provided input."""

    request_payload = {"action": "steamID", "id":field_input}
    steamid_request = requests.get("http://steamid.co/php/api.php", params=request_payload)
    
    try:
        if "error" in steamid_request.json().keys():
            return ""
        else:
            print(steamid_request.json()["steamID64"])
    except ValueError:
        return ""