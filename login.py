import mysql.connector

class login:
    def __init__(self,db):
        self.host = 'localhost'
        self.username = 'root'
        self.password = 'glenelric'
        self.database = 'game_arcade'

        self.cnx = mysql.connector.connect(
            user=self.username,
            password=self.password,
            host=self.host,
            database=self.database
        )

        self.cursor = self.cnx.cursor()

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