from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def greeter():
    return render_template("index.html")

@app.route("/", methods=["POST"])
def on_input_field():
    text = request.form["dotaID"]
    print(text)
    return greeter()