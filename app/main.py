from twitch_class import *
from sqlite3_class import *

from flask import Flask, jsonify, request

app = Flask(__name__)




@app.route("/streamers", methods=["GET"])
def get_streamers():
    sqlite_handler = SqliteHandler()
    sqlite_handler.open_connection("db/twitch.db")  
    ret = sqlite_handler.get_streamers()
    sqlite_handler.close_connection()
    return jsonify(ret)

@app.route("/streamers/<username>", methods=["GET"])
def get_streamer(username):
    sqlite_handler = SqliteHandler()
    sqlite_handler.open_connection("db/twitch.db")
    ret = sqlite_handler.get_streamer(username)
    sqlite_handler.close_connection()
    return jsonify(ret)

@app.route("/streamers", methods=["POST"])
def post_streamer():
    username = request.args.get('username')
    twitch_handler = TwitchHandler()
    twitch_handler.authenticate()
    ret = twitch_handler.fetch_streamer(username)['data']
    if not ret:
        return json.dumps("Streamer not found in Twitch API")
    
    streamer = ret[0]
    row = TwitchHandler.convert_twitch_to_db_format(streamer)
    sqlite_handler = SqliteHandler()
    sqlite_handler.open_connection("db/twitch.db")
    sqlite_handler.add_streamer(row)
    sqlite_handler.close_connection()
    return json.dumps(username + "'s data added to database")

@app.route("/streamers/<username>", methods=["DELETE"])
def del_streamer(username):
    sqlite_handler = SqliteHandler()
    sqlite_handler.open_connection("db/twitch.db")
    sqlite_handler.remove_streamer(username)    
    sqlite_handler.close_connection()
    return json.dumps(username + " removed from Database")

@app.route("/subscriptions/<username>", methods=['POST'])
def subscribe(username):
    twitch_handler = TwitchHandler()
    twitch_handler.authenticate()
    streamer = twitch_handler.fetch_streamer(username)
    twitch_handler.subscribe_to_event(int(streamer['data'][0]['user_id']))
    return json.dumps("200")

@app.route("/subscriptions/callback", methods=['POST'])
def callback():

    data = request.get_json()
    twitch_handler = TwitchHandler()
    twitch_handler.authenticate()
    streamer = twitch_handler.fetch_streamer(data['event']['broadcaster_user_name'])
    stream = ( int(streamer['data'][0]['user_id']), 
            data['event']['broadcaster_user_name'],
            streamer['data'][0]['title'],
            data['event']['started_at']
            )
    sqlite_handler = SqliteHandler()
    sqlite_handler.open_connection("db/twitch.db")
    sqlite_handler.add_stream(stream)    
    sqlite_handler.close_connection()
    return json.dumps("200")

@app.route("/streamers/<string:username>/streams", methods=['GET'])
def get_streams(username):
    sqlite_handler = SqliteHandler()
    sqlite_handler.open_connection("db/twitch.db")
    ret = sqlite_handler.get_streams(username) 
    sqlite_handler.close_connection()
    return jsonify(ret)


if __name__ == "__main__":

    sqlite_handler = SqliteHandler()
    sqlite_handler.open_connection("db/twitch.db")
    sql_requests = ["""
    CREATE TABLE IF NOT EXISTS streamers (
    id integer PRIMARY KEY,
    platform text DEFAULT "Twitch",
    username text NOT NULL,
    streaming_url text,
    profil_pic_url text );""",
    """CREATE TABLE IF NOT EXISTS streams (
    id_stream integer PRIMARY KEY,
    username text NOT NULL,
    session_title text,
    session_start text); """
    ]
    for sql_req in sql_requests:
        sqlite_handler.create_table(sql_req)
    twitch_handler = TwitchHandler()
    twitch_handler.authenticate()
    streamers = twitch_handler.fetch_streamers(10, TwitchHandler.params['after'])

    for streamer in streamers:
        row = TwitchHandler.convert_twitch_to_db_format(streamer)
        #sqlite_handler.add_streamer(row)


    sqlite_handler.close_connection()

    app.run(host='0.0.0.0', port=6000)


    
    


