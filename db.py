""" hnadle db communications """
import sqlite3

class DBSQL():
    def __init__(self):
        self.conn = self.connectDB()
        self.createTable()
    def connectDB(self):
        conn = None
        try:
            conn = sqlite3.connect('password_app.db')
        except Exception as e:
            print(e)
        return conn

    def createTable(self):
        """ create user table, password table"""
        user_stmt = """CREATE TABLE IF NOT EXISTS users (
            username CHAR(20) NOT NULL,
            password TEXT NOT NULL,
            email CHAR(50)
        );
        """
        password_stmt = """CREATE TABLE IF NOT EXISTS passwords (
            site TEXT NOT NULL,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            note TEXT,
            remainder TEXT,
            user_id INT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (rowid)
        );
        """
        c = self.conn.cursor()
        c.execute(user_stmt)
        c.execute(password_stmt)
        return True
    def createNewUser(self, **kwargs):
        """ insert new user data to data """
        stmt = """INSERT INTO users (username, password, email) VALUES(?,?,?)"""
        cur = self.conn.cursor()
        cur.execute(stmt, (kwargs['username'], kwargs['password'],kwargs.get('email')))
        self.conn.commit()
        return cur.lastrowid
    def getUserId(self, username, password):
        """ fecth user using cred """
        stmt = "SELECT rowid FROM users WHERE username=? AND password=? LIMIT 1"
        cur = self.conn.cursor()
        cur.execute(stmt, (username,password))
        row = cur.fetchone()
        return row
    def createNewPassword(self, user_id, data):
        """ insert new user data to data """
        stmt = """INSERT INTO passwords (site, username, password, note, remainder, user_id) VALUES (?,?,?,?,?,?)"""
        cur = self.conn.cursor()
        cur.execute(stmt, (data.get('site'),data.get('username'),data.get('password'), data.get('note'),data.get('reminder',""),user_id))
        self.conn.commit()
        return cur.lastrowid
    def getAllUserPassword(self,user_id):
        """ get password for user with user_id """
        stmt = """SELECT `rowid`, `site`, `username`,`password`, `note`, `remainder` FROM passwords WHERE user_id=?"""
        cur = self.conn.cursor()
        cur.execute(stmt, (user_id,))
        rows = cur.fetchall()
        passwords = {}
        for row in rows:
            mapped = {
                'site':row[1],
                'username':row[2],
                'password':row[3],
                'note':row[4],
                'remainder':row[5]
            }
            passwords[str(row[0])] = mapped
        return passwords
    def getPasswordDetail(self, user_id, psw_id):
        """ retrive user password with matching psw_id"""
        passwords = self.getAllUserPassword(user_id)
        if len(passwords)>0:
            return passwords.get(psw_id)
        return None
    def updatePassword(self, user_id, psw_id, data):
        """ update password for user if it exit """
        vals = []
        temp = ""
        for key,val in data.items():
            if len(temp):
                temp += ", "
            temp += f"{key}=?"
            vals.append(val)
        vals.extend([user_id,psw_id])
        stmt = f"""UPDATE passwords SET {temp} WHERE user_id=? AND rowid=?"""
        cur = self.conn.cursor()
        cur.execute(stmt, tuple(vals))
        self.conn.commit()
        return cur.lastrowid
    def deletePassword(self, user_id, psw_id):
        """ update password for user if it exit """
        stmt = 'DELETE FROM passwords WHERE rowid=? AND user_id=?'
        cur = self.conn.cursor()
        cur.execute(stmt, (psw_id, user_id))
        self.conn.commit()
        return True





if __name__ == '__main__':
    db = DBSQL()
    print(db.conn)
