import sqlite3

class Database:
    def __init__(self, database_name="tracker.db"):
        self.database_name = "tracker.db"
        self.connection = None
        self.cursor = None
        self.execute('''CREATE TABLE IF NOT EXISTS file (id INTEGER PRIMARY KEY AUTOINCREMENT, file_name TEXT, root_hash TEXT)''')
        

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
            query = 'SELECT * FROM file WHERE file_name="'+ file_name + '" LIMIT 1'
        else:
            query = 'SELECT * FROM file WHERE file_name="'+ file_name + '" AND root_hash="'+ root_hash + '" LIMIT 1'
        
        if (self.connection == None):
            self.connect()
        
        if (self.cursor == None):
            self.cursor = self.connection.cursor()
        
        self.cursor.execute(query)
        row = self.cursor.fetchone()
        print(row)
        print(type(row))
        return row
    
    def upload_file(self, file_name, root_hash):
        query = "INSERT INTO file (file_name, root_hash) VALUES ('" + file_name + "', '" + root_hash + "')"
        self.execute(query)
        print("Uploaded")
        row = self.fetch_file(file_name, root_hash)
        return row
        

# def connect(database_name="tracker.db"):
#     conn = sqlite3.connect
# # Connect to SQLite database (create it if it doesn't exist)
# conn = sqlite3.connect('example.db')

# # Create a cursor object to execute SQL commands
# cursor = conn.cursor()

# # Create a table
# cursor.execute('''CREATE TABLE IF NOT EXISTS users
#                   (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)''')

# # Insert data into the table
# cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", ('Alice', 30))
# cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", ('Bob', 25))
# cursor.execute("INSERT INTO users (name, age) VALUES (?, ?)", ('Charlie', 35))

# # Commit changes to the database
# conn.commit()

# # Query data from the table
# cursor.execute("SELECT * FROM users")
# rows = cursor.fetchall()

# # Print query results
# for row in rows:
#     print(row)

# # Close the cursor and connection
# cursor.close()
# conn.close()
