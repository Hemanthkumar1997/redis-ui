import redis
import json
import flask
import waitress
import logging
from flask import render_template
from flask_cors import CORS, cross_origin

app = flask.Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

try:
    r = redis.Redis(host="localhost", port="6379", db=0)
except Exception as e:
    logging.error("Could not connect to redis server", e)


@app.route("/getAllKeys", methods=['post'])
def get_keys_from():
    keys = []
    for each_key in r.keys("*"):
        keys.append(str(each_key).replace('\'', "").replace("b", ""))
    return app.response_class(
            response=json.dumps({"keys": keys}),
            status=200,
            mimetype='application/json'
        )


@app.route("/getVal/<key>")
def get_val_of(key):
    val = r.get(key)
    json_val = f"No data found for {key}"
    try:
        json_val = json.loads(val)
    except Exception as ex:
        print("Invalid Json: ", ex)
        if val is not None:
            json_val = str(val, "utf-8")

    return app.response_class(
        response=json.dumps(json_val, indent=4, sort_keys=True),
        status=200,
        mimetype='application/json'
    )


@app.route("/purge/<key>")
def delete_key(key):
    num_keys = r.delete(key)
    if num_keys == 0:
        status = 500
        message = "Invalid key"
    else:
        status = 200
        message = f"deleted {key}"

    response = {
        "status": status,
        "message": message
    }
    return app.response_class(
        response=json.dumps(response),
        status=200,
        mimetype='application/json'
    )


@app.route("/purgeAll/")
def delete():
    keys = sorted([str(i)[1:].replace('\'', "") for i in r.keys("*")])
    if len(keys) == 0:
        status = 500
        message = "No Keys to delete"
    else:
        r.flushall(asynchronous=True)
        status = 200
        message = "Deleted all the keys"

    response = {
        "status": status,
        "message": message
    }

    if len(keys) != 0:
        response["keys"] = keys

    return app.response_class(
        response=json.dumps(response),
        status=200,
        mimetype='application/json'
    )


@app.route("/")
@cross_origin()
def home():
    global r
    if r is None:
        r = redis.Redis(host="localhost", port="6379", db=0)
    try:
        keys = sorted([str(i)[1:].replace('\'', "") for i in r.keys("*")])
    except Exception as ex:
        keys = []
        logging.error("Could not fetch data from redis server", ex)
    return render_template('home.html', keys=keys)


if __name__ == "__main__":
    waitress.serve(app)
