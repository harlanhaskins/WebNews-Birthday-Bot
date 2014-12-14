from flask import Flask, jsonify
import datetime
import nextbirthday

app = Flask(__name__)
_last_updated = datetime.datetime.utcnow()
_bday = None

def next_birthday():
    global _bday
    global _last_updated
    now = datetime.datetime.utcnow()
    delta = now - _last_updated
    if not _bday or delta.total_seconds() > (30 * 60):
        print("reassigning birthday")
        _bday = nextbirthday.next_birthday()
    return _bday

@app.route("/birthday", methods=["GET"])
def birthday():
    return jsonify(**next_birthday())

app.run(port=5555, host="0.0.0.0", debug=True)
