""" hnadle db communications """


class DB():
    """ simulate db or db wrapper """
    def __init__(self, *args, **kwargs):
        self.users = { #dummy data
                        "100":{
                            "username": "Janet Jackson",
                            "password": "janetjackson"
                        },
                        "101":{
                            "username": "Charlie D",
                            "password": "charlesdarwin"
                        }
                    }
        self.passwords = {
            "1":{
                "site": 'google.com',
                "username":"janetjackson",
                "password":"janetjackson",
                "note": "google acount One",
                "reminder": "01-28-2022",
                "user":"100"
            },
            "2":{
                "site": 'yahoo.com',
                "username":"janetjackson",
                "password":"yahoojacksonpsw",
                "note": "",
                "reminder": "03-09-2023",
                "user":"100"
            },
            "3":{
                "site": 'home wifi',
                "username":"localhost",
                "password":"0101000",
                "note": "telus provider",
                "reminder": "05-01-2021",
                "user":"100"
            },
            "4":{
                "site": 'safe locker',
                "username":"",
                "password":"0-8-1",
                "note": "for work",
                "reminder": "",
                "user":"101"
            }
        }
    def getUserId(self, username, password):
        """ fecth user using cred """
        for _id, detail in self.users.items():
            if detail['username'] == username and detail['password'] == password:
                return _id
        return None
    def getUserInfo(self, _id):
        """ get user from data using _id"""
        return self.users.get(_id, {})

    def createNewUser(self, username, password):
        """ insert new user data to data """
        _id = str(100+len(self.users))
        self.users.update({
                _id : {
                    'username': username,
                    'password': password
                }
        })
        return _id
    def createNewPassword(self, user_id, data):
        """ insert new user data to data """
        _id = str(len(self.passwords)+1)
        self.passwords.update({
                _id : {**data, 'user':user_id},
        })
        return _id

    def getAllUserPassword(self,user_id):
        """ get password for user with user_id """
        passwords = {}
        for _id, password_detail in self.passwords.items():
            if password_detail.get('user') == user_id:
                passwords[_id] = password_detail
        return passwords
    def getPasswordDetail(self, user_id, psw_id):
        """ retrive user password with matching psw_id"""
        passwords = self.getAllUserPassword(user_id)
        return passwords.get(psw_id, {})
    def updatePassword(self, user_id, psw_id, data):
        """ update password for user if it exit """
        passwords = self.getAllUserPassword(user_id)
        password = passwords.get(psw_id, {})
        if password:
            self.passwords.update({
                psw_id : {**data, 'user':user_id},
        })
        return psw_id
    def deletePassword(self, user_id, psw_id):
        """ update password for user if it exit """
        passwords = self.getAllUserPassword(user_id)
        password = passwords.get(psw_id, {})
        if password:
            del self.passwords[psw_id]
        return psw_id
