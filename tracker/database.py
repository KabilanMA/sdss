import sqlite3

class Database:
    def __init__(self, database_name="./tracker/data/tracker.db"):
        self.database_name = database_name
        self.connection = None
        self.cursor = None
        self.execute('''CREATE TABLE IF NOT EXISTS file (id INTEGER PRIMARY KEY AUTOINCREMENT, file_name TEXT, file_size INTEGER, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, root_hash TEXT, chunk_count INTEGER)''')
        self.execute('''CREATE TABLE IF NOT EXISTS peer_file (id INTEGER PRIMARY KEY AUTOINCREMENT, file_id INTEGER, peer_ip TEXT, peer_port INTEGER, UNIQUE(file_id, peer_ip))''')
        

    def connect(self):
        if (self.connection == None):
            self.connection = sqlite3.connect(self.database_name)
        return self.connection
    
    def execute(self, query, auto_commit=True):
        if (self.cursor == None):
            if (self.connection == None):
                self.connect()
            self.cursor = self.connection.cursor()
        self.cursor.execute(query)
        
        if auto_commit:
            self.connection.commit()
            self.cursor.close()
            self.connection.close()
            self.cursor = None
            self.connection = None
            return None
        else:
            return self.cursor
    
    def commit(self):
        if (self.connection != None):
            self.connection.commit()
            if (self.cursor != None):
                self.cursor.close()
                self.cursor = None
    
    def fetch_file(self, file_name, root_hash=""):
        query = ""
        if (root_hash==""):
            query = 'SELECT * FROM file WHERE file_name="'+ file_name + '"'
        else:
            query = 'SELECT * FROM file WHERE file_name="'+ file_name + '" AND root_hash="'+ root_hash + '"'
        
        if (self.connection == None):
            self.connect()
        
        if (self.cursor == None):
            self.cursor = self.connection.cursor()
        
        self.cursor.execute(query)
        row = self.cursor.fetchone()
        return row
    
    def upload_file(self, file_name, file_size, root_hash, chunk_count):
        query = 'SELECT * FROM file WHERE file_name="'+ file_name + '"'
        if (self.connection == None):
            self.connect()
        if (self.cursor == None):
           self.cursor = self.connection.cursor()

        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        if (len(rows)>0):
            update_query = 'UPDATE file SET root_hash="' + root_hash + '", file_size="' + file_size  + '", chunk_count="' + chunk_count + '" WHERE file_name="' + file_name + '"'
            self.execute(update_query)
        else:
            insert_query = 'INSERT INTO file (file_name, file_size, root_hash, chunk_count) VALUES ("' + file_name + '", "' + file_size + '", "' + root_hash + '", "' + chunk_count + '")'
            self.execute(insert_query)
        row = self.fetch_file(file_name, root_hash)
        return row
    
    def update_file_peer(self, file_id, ip, port):
        query = 'INSERT OR REPLACE INTO peer_file (file_id, peer_ip, peer_port) VALUES ("' + file_id + '", "' + ip + '", "' + port + '")'
        
        if (self.connection == None):
            self.connect()
        if (self.cursor == None):
           self.cursor = self.connection.cursor()

        self.cursor.execute(query)

        self.commit()
        self.connection.close()
        self.cursor = None
        self.connection = None
    
    def get_file_peers(self, file_id):
        query = 'SELECT peer_ip, peer_port FROM peer_file WHERE file_id="' + file_id + '"'

        if (self.connection == None):
            self.connect()
        if (self.cursor == None):
           self.cursor = self.connection.cursor()

        self.cursor.execute(query)
        rows = self.cursor.fetchall()

        self.commit()
        self.connection.close()
        self.cursor = None
        self.connection = None

        return rows
    
    def fetch_all_filename(self):
        query = 'SELECT file_name, file_size FROM file'

        if (self.connection == None):
            self.connect()
        if (self.cursor == None):
           self.cursor = self.connection.cursor()

        self.cursor.execute(query)
        rows = self.cursor.fetchall()

        self.cursor.close()
        self.connection.close()
        self.cursor = None
        self.connection = None

        return rows
    
    def get_file_info(self, file_name):
        query = 'SELECT id, file_name, root_hash, chunk_count FROM file WHERE file_name="' + file_name + '"'

        if (self.connection == None):
            self.connect()
        if (self.cursor == None):
           self.cursor = self.connection.cursor()

        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        entry = rows[-1]
        chunk_count = entry[-1]
        root_hash = entry[-2]
        query = 'SELECT file_id, peer_ip, peer_port FROM peer_file WHERE file_id="' + str(entry[0]) + '"'
        self.cursor.execute(query)
        rows = self.cursor.fetchall()

        self.cursor.close()
        self.connection.close()
        self.cursor = None
        self.connection = None

        return rows, root_hash, chunk_count
