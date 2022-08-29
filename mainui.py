""" Simulate Ui With terminal prompts"""
from db import DBSQL
from pprint import pprint



def getAndValidateInput(prompt, validators, optional=False):
    """
        get input and validate using the validators
        validators ->
            [
                [function, error_message], ...
            ]
    """

    while True:
        value = input(f"{prompt}: ")
        if not value and optional:
            return ""
        errors = [val[1] for val in validators if not val[0](value)]
        if not errors:
            return value
        print(", ".join(errors))

class UI(object):
    """ Simulate Ui With terminal prompts"""
    def __init__(self, *args, **kwargs) -> None:
        """ init app ui """
        self.user = None  #set user to none
        self.state = 'home'
        self.db = DBSQL()
    def signIn(self):
        """ get username and password and get user from data if it exit"""
        while True:
            username = getAndValidateInput(prompt = "Enter your Username", validators=[
                [lambda x: len(x) > 3, "Username must be 3 characters or more"]
            ])
            password = getAndValidateInput(prompt = "Enter password", validators=[
                [lambda x: len(x) > 3, "Password must be 3 characters or more"]
            ])
            self.user = self.db.getUserId(username, password)[0]
            if self.user:
                print(f"Welcome {username} !")
                return
            print(" Wrong Username or password!. Please Try Again")

    def signUp(self):
        username = getAndValidateInput(prompt = "Enter your prefer Username", validators=[
            [lambda x: len(x) > 3, "Username must be 3 characters or more"]
        ])
        password1 = getAndValidateInput(prompt = "Enter password", validators=[
            [lambda x: len(x) > 3, "Password must be 3 characters or more"]
        ])
        password2 = getAndValidateInput(prompt = "Confirm password", validators=[
            [lambda x: x == password1, "Password must match"]
        ])
        self.user = self.db.createNewUser(username=username, password=password2)
        print("Your account has been created!", self.user)

    def signOut(self):
        """ sign out user by setting app user to none """
        self.user = None
        self.state = 'home'
        print("You've successfully signed Out")
        return

    def addNewPassword(self):
        """ get new password info"""
        site = getAndValidateInput(prompt = "Enter Password site(url) or name", validators=[], optional=True)
        username = getAndValidateInput(prompt = "Enter Username", validators=[], optional=True)
        password1 = getAndValidateInput(prompt = "Enter password", validators=[
            [lambda x: len(x) > 3, "Password must be 3 characters or more"]
        ])
        password2 = getAndValidateInput(prompt = "Confirm password", validators=[
            [lambda x: x == password1, "Password must match"]
        ])
        notes = getAndValidateInput(prompt = "Notes or Descriptions", validators=[], optional=True)
        reset_reminder = getAndValidateInput(prompt = "Enter reset reminder date (dd-mm-yyyy)", validators=[
            [
                lambda x: len(x.split('-'))==3 and len(x.split('-')[0])==2 and len(x.split('-')[1])==2 and len(x.split('-')[2])==4,
                "Please Check Your Date format, and try again"
            ]
        ], optional=True)
        new_psw_id = self.db.createNewPassword(user_id=self.user, data={
                "site": site,
                "username":username,
                "password":password2,
                "note": notes,
                "reminder": reset_reminder
            })
        if new_psw_id:
            print("New Password Successfully Added!")
    def listPassword(self):
        psw_ids = self.db.getAllUserPassword(self.user).keys()
        for psw_id, psw_detail in self.db.getAllUserPassword(self.user).items():
            print(f"==============Press {psw_id} for more detail ==================")
            print(psw_detail.get('site') or psw_detail.get('note') or "No Name")
            print("================================================================")
        action = input("Or Press (e) to go back to HOME page: ")
        if action in psw_ids:
            self.state = 'detail'
            self.getPasswordDetail(action)
            pass
        elif action == 'e':
            self.state = 'home'
    def getPasswordDetail(self, psw_id):
        """ get password record using psw_id """
        print("================================")
        pprint(self.db.getPasswordDetail(self.user, psw_id))
        print("================================")
        action = input("Press (e) to Edit This Password, Or Press (d) to Delete This Password, Or Press (l) to go back to LIST page, Or Press (h) to go back to HOME page: ")
        if not self.inputHandler(action):
            if action == 'd':
                self.deletePassword(psw_id)
            elif action == 'e':
                self.editPassword(psw_id)
    def deletePassword(self, psw_id):
        """ verify and delete password record """
        action = input("Are You Sure You Want To Delete This Password? Press (c) to Confirm, Or Press (l) to Cancel: ")
        if not self.inputHandler(action):
            deleted = self.db.deletePassword(self.user, psw_id)
            if deleted:
                print("Record Successfully Deleted!")
                self.inputHandler('l')

    def editPassword(self, psw_id):
        """ update password info for psw_id"""
        new_values = {}
        for key,value in self.db.getPasswordDetail(self.user, psw_id).items():
            if key!='user':
                new_values[key] = input(f"""Enter new {key} Or Press Enter to Leave as [current: {value}]: """) or value
        upd = self.db.updatePassword(user_id=self.user, psw_id=psw_id, data=new_values)
        if upd:
            print("password successfully updated!")
        self.state = 'detail'
        self.getPasswordDetail(psw_id)

    def inputHandler(self, inp):
        """ act as router base on user input """
        if inp == 'h':
            self.state = 'home'
            return True
        elif inp == 'l':
            self.state = 'list'
            self.listPassword()
            return True
        elif inp == 'x':
            self.signOut()
            return True
        return False

    def screen(self):
        """ prompt and act as ui/screen """
        if self.state == 'home':
            if self.user:
                action = input("Press (x) to Sign Out or Press (a) to Add New Password or (l) to list all your passwords: ")
                if not self.inputHandler(action):
                    if action == 'a':
                        return self.addNewPassword()
            else:
                action = input("Press (1) to Sign Up or Press (2) to Login: ")
                if action == '1':
                    self.signUp()
                elif action == '2':
                    self.signIn()

    def __str__(self) -> str:
        return "Please Sign In or Sign Up To Continue" if not self.user else f"Hello {self.db.getUserInfo(self.user).get('username')}"

if __name__ == "__main__":
    app = UI()
    print(app)
    while True:
        app.screen()
