# coding: utf-8

from flask import Flask, request, json, g, render_template
import sqlite3

DATABASE = '/tmp/infobip.db'

app = Flask(__name__)

@app.route('/api/v3/sendsms/json', methods=['POST'])
def send_message():

    query_db('''CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                sender text,
                recipient text,
                message text
            )''')

    content_type = request.headers.get("Content-Type", "")

    if request.headers.get("Content-Type") != "application/json":
        raise Exception(u'Expected "application/json" content-type, got "%s"' % content_type)

    data = json.loads(request.data)

    check_required(data, ("authentication", "messages"))

    check_required(data["authentication"], ("username", "password"))

    messages = data.get("messages")

    check_list(messages, "messages")

    message = messages[0]

    check_required(message, ("sender", "text", "recipients"))

    recipients = message["recipients"]

    check_list(recipients, "recipients")

    recipient = recipients[0]

    check_required(recipient, ("gsm",))

    results = []

    results.append(send_sms(message["sender"], recipient["gsm"], message["text"]))

    return json.dumps({"results": results})

@app.route('/messages', methods=['GET'])
def get_messages():
    messages = query_db("SELECT * FROM messages ORDER BY id DESC LIMIT 10")

    return render_template('messages.html', messages=messages)


def send_sms(sender, recipient, message):

    message_id = insert_db(u"INSERT INTO messages VALUES (?,?,?,?)", args=(None, sender, recipient, message))

    return {
        "status": str(0),
        "messageid": str(message_id),
        "destination": str(recipient),
    }


def check_required(array, params):
    if not isinstance(array, dict):
        raise Exception(u'Expected dict')

    for param in params:
        if param not in array:
            raise Exception(u'Field "%s" is missing' % param)


def check_list(array, field):
    if not isinstance(array, list) or len(array) == 0:
        raise Exception(u'Field "%s" is missing or empty' % field)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = dict_factory
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def insert_db(query, args=()):
    db = get_db()
    cur = db.execute(query, args)
    cur.close()
    db.commit()

    return cur.lastrowid


def dict_factory(cursor, row):
    d = {}
    for idx,col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
