import sqlite3
from sqlite3 import Error
from datetime import datetime

class SqliteHandler:
    def __init__(self):
        self.conn = None
    
    def open_connection(self, db_file):
        try:
            self.conn = sqlite3.connect(db_file, check_same_thread=False)
            print(sqlite3.version)
        except Error as e:
            print(e)

    def close_connection(self):
        if self.conn:
            self.conn.close()

    def create_table(self, sql_request):
        try:
            c = self.conn.cursor()
            c.execute(sql_request)
        except Error as e:
            print(e)

    def add_streamer(self, streamer):
        sql = ''' INSERT INTO streamers(id,platform,username,streaming_url,profil_pic_url)
            VALUES(?,?,?,?,?) '''
        cur = self.conn.cursor()
        cur.execute(sql, streamer)
        self.conn.commit()

    def get_streamers(self):
        sql = ''' SELECT * FROM streamers ;'''
        cur = self.conn.cursor()
        cur.execute(sql,)
        rows = cur.fetchall()

        ret =  []
        for row in rows:
            streamer = {}
            streamer['platform'] = row[1]
            streamer['username'] = row[2]
            streamer['stream_url'] = row[3]
            streamer['profil_picture_url'] = row[4]
            ret.append(streamer)
            print(streamer['username'], row[0])
        return ret

    def get_streamer(self, username):
        sql = ''' SELECT * FROM streamers WHERE username = ? '''
        cur = self.conn.cursor()
        cur.execute(sql, (username,))
        rows = cur.fetchall()

        ret =  []
        for row in rows:
            streamer = {}
            streamer['platform'] = row[1]
            streamer['username'] = row[2]
            streamer['stream_url'] = row[3]
            streamer['profil_picture_url'] = row[4]
            ret.append(streamer)
        return ret

    def remove_streamer(self, username):
        sql = 'DELETE FROM streamers WHERE username=?'
        cur = self.conn.cursor()
        cur.execute(sql, (username,))
        self.conn.commit()

    
    def get_streams(self, username):
        sql = ''' SELECT * FROM streams WHERE username=?;'''
        cur = self.conn.cursor()
        cur.execute(sql, (username,))
        rows = cur.fetchall()

        ret =  []
        for row in rows:
            stream = {}
            stream['title'] = row[2]
            stream['startDate'] = row[3]
            date = datetime.strptime(stream['startDate'], '%Y-%m-%dT%H:%M:%S.%fZ')
            stream['startDateTS'] = datetime.timestamp(date)
            ret.append(stream)
        return ret

    def add_stream(self, stream):
        sql = ''' INSERT INTO streams(id_stream, username, session_title, session_start)
            VALUES(?,?,?,?) '''
        cur = self.conn.cursor()
        cur.execute(sql, stream)
        self.conn.commit()

if __name__ == "__main__":
    sqlite_handler = SqliteHandler()
    sqlite_handler.open_connection(r"db\twitch.db")

    sql_request = """
    CREATE TABLE IF NOT EXISTS streamers (
	id integer PRIMARY KEY,
    platform text DEFAULT "Twitch",
	username text NOT NULL,
	streaming_url text,
	profil_pic_url text );  
    """
    sqlite_handler.create_table(sql_request)

    streamer = (44409342445, "Twitch", "loltyler1", "www.twitch.tv/" + "loltyler1", "https://static-cdn.jtvnw.net/previews-ttv/live_user_jelty-{width}x{height}.jpg")
    sqlite_handler.add_streamer(streamer)
    #sqlite_handler.remove_streamer(44409342445)
    print(sqlite_handler.get_streamers())
    sqlite_handler.close_connection()
