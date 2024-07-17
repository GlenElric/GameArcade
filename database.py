import mysql.connector
def __init__(self):
    self.host = 'localhost'
    self.username = 'root'
    self.password = 'glenelric'
    self.database = 'game_arcade'

    # Create a connection to the MySQL server
    cnx = mysql.connector.connect(
        user=self.username,
        password=self.password,
        host=self.host
    )

    # Create a cursor object
    cursor = cnx.cursor()

    # Create the database if it doesn't exist
    cursor.execute("CREATE DATABASE IF NOT EXISTS game_arcade")

    # Close the cursor and connection
    cursor.close()
    cnx.close()

    # Now, connect to the 'game_arcade' database
    self.cnx = mysql.connector.connect(
        user=self.username,
        password=self.password,
        host=self.host,
        database=self.database
    )

    self.cursor = self.cnx.cursor()

    # Create tables if they don't exist
    self.create_tables()

class Database:
    def __init__(self):
        self.host = 'localhost'
        self.username = 'root'
        self.password = 'glenelric'
        self.database = 'games_arcade'

        self.cnx = mysql.connector.connect(
            user=self.username,
            password=self.password,
            host=self.host
        )

        self.cursor = self.cnx.cursor()

        # Create database if it doesn't exist
        self.create_database()

        # Connect to the database
        self.cnx.database = self.database
        self.cursor.execute("USE {}".format(self.database))

        # Create tables if they don't exist
        self.create_tables()

    def create_database(self):
        self.cursor.execute("CREATE DATABASE IF NOT EXISTS {}".format(self.database))

    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT,
                username VARCHAR(50) NOT NULL,
                password VARCHAR(255) NOT NULL,
                email VARCHAR(100) NOT NULL,
                PRIMARY KEY (id)
            );
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS high_scores (
                id INT AUTO_INCREMENT,
                user_id INT NOT NULL,
                game_name VARCHAR(50) NOT NULL,
                score INT NOT NULL,
                PRIMARY KEY (id),
                FOREIGN KEY (user_id) REFERENCES users (id)
            );
        """)

        self.cnx.commit()

    def add_user(self, username, password, email):
        self.cursor.execute("""
            INSERT INTO users (username, password, email)
            VALUES (%s, %s, %s);
        """, (username, password, email))
        self.cnx.commit()

    def get_user(self, username, password):
        self.cursor.execute("""
            SELECT * FROM users
            WHERE username = %s AND password = %s;
        """, (username, password))
        return self.cursor.fetchone()

    def add_high_score(self, user_id, game_name, score):
        self.cursor.execute("""
            INSERT INTO high_scores (user_id, game_name, score)
            VALUES (%s, %s, %s);
        """, (user_id, game_name, score))
        self.cnx.commit()

    def get_high_scores(self, game_name):
        self.cursor.execute("""
            SELECT * FROM high_scores
            WHERE game_name = %s
            ORDER BY score DESC;
        """, (game_name,))
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.cnx.close()

# Example usage:
if __name__ == "__main__":
    db = Database()

    # Add a user
    db.add_user("john_doe", "password123", "john@example.com")

    # Get a user
    user = db.get_user("john_doe", "password123")
    print(user)

    # Add a high score
    db.add_high_score(1, "Space Invaders", 1000)

    # Get high scores
    high_scores = db.get_high_scores("Space Invaders")
    for score in high_scores:
        print(score)

    # Close the database connection
    db.close()

    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT,
                username VARCHAR(50) NOT NULL,
                password VARCHAR(255) NOT NULL,
                email VARCHAR(100) NOT NULL,
                PRIMARY KEY (id)
            );
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS high_scores (
                id INT AUTO_INCREMENT,
                user_id INT NOT NULL,
                game_name VARCHAR(50) NOT NULL,
                score INT NOT NULL,
                PRIMARY KEY (id),
                FOREIGN KEY (user_id) REFERENCES users (id)
            );
        """)

        self.cnx.commit()

    def add_user(self, username, password, email):
        self.cursor.execute("""
            INSERT INTO users (username, password, email)
            VALUES (%s, %s, %s);
        """, (username, password, email))
        self.cnx.commit()

    def get_user(self, username, password):
        self.cursor.execute("""
            SELECT * FROM users
            WHERE username = %s AND password = %s;
        """, (username, password))
        return self.cursor.fetchone()

    def add_high_score(self, user_id, game_name, score):
        self.cursor.execute("""
            INSERT INTO high_scores (user_id, game_name, score)
            VALUES (%s, %s, %s);
        """, (user_id, game_name, score))
        self.cnx.commit()

    def get_high_scores(self, game_name):
        self.cursor.execute("""
            SELECT * FROM high_scores
            WHERE game_name = %s
            ORDER BY score DESC;
        """, (game_name,))
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.cnx.close()

# Example usage:
if __name__ == "__main__":
    db = Database()

    # Add a user
    db.add_user("john_doe", "password123", "john@example.com")

    # Get a user
    user = db.get_user("john_doe", "password123")
    print(user)

    # Add a high score
    db.add_high_score(1, "Space Invaders", 1000)

    # Get high scores
    high_scores = db.get_high_scores("Space Invaders")
    for score in high_scores:
        print(score)

    # Close the database connection
    db.close()