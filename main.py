import redis
import json
import flask
import waitress
from flask import render_template

app = flask.Flask(__name__)

r = redis.Redis(host="localhost", port="6379", db=0)


@app.route("/getAllKeys", methods=['post'])
def get_keys_from():
    return json.dumps(r.keys("*"))


@app.route("/getVal/<key>")
def get_val_of(key):
    return app.response_class(
        response=json.dumps(json.loads(r.get(key)), indent=4, sort_keys=True),
        status=200,
        mimetype='application/json'
    )


@app.route("/")
def home():
    global r
    if r is None:
        r = redis.Redis(host="localhost", port="6379", db=0)
    keys = sorted([str(i)[1:].replace('\'',"") for i in r.keys("*")])
    return render_template('home.html', keys=keys)


if __name__ == "__main__":
    waitress.serve(app)
