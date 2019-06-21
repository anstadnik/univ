from role import Role
from user import User

from PySide2.QtWidgets import QApplication
from edit_file import EditFile
import sys
from role import Role

class System():

    """This class represents the whole system"""

    def __init__(self):
        """Initialize the empty system """
        self.roles = {}
        self.users = {}
        self.files = {}

    def create_default(self):
        """Create the default roles and users
        Returns: TODO

        """
        self.roles = {
            'Admin': Role(
                name     = 'Admin',
                add_role   = True,
                del_role   = True,
                add_user = True,
                del_user = True,
                add_f    = False,
                view_f   = False,
                edit_f   = False,
                del_f    = False,
            ),
            'Manager': Role(
                name     = 'Manager',
                add_role   = False,
                del_role   = False,
                add_user = False,
                del_user = False,
                add_f    = True,
                view_f   = True,
                edit_f   = True,
                del_f    = True,
            ),
            'Editor': Role(
                name     = 'Editor',
                add_role   = False,
                del_role   = False,
                add_user = False,
                del_user = False,
                add_f    = False,
                view_f   = True,
                edit_f   = True,
                del_f    = False,
            ),
            'Operator': Role(
                name     = 'Operator',
                add_role   = False,
                del_role   = False,
                add_user = False,
                del_user = False,
                add_f    = True,
                view_f   = False,
                edit_f   = False,
                del_f    = False,
            )
        }

        self.users = {
            'a': User('a', 'a', self.roles['Admin']),
            'o': User('o', 'o', self.roles['Operator']),
            'e': User('e', 'e', self.roles['Editor'])
        }

        self.files = {
            'potato': ''
        }

    def run(self):
        """Wrapper for the loop

        """
        try:
            while 42:
                ret = self.loop()
                if ret != -1:
                    exit(ret)
        except KeyboardInterrupt:
            print("Bye")
            exit(0)

    def loop(self):
        """The main function that's doing all the work
        Returns: TODO

        """
        while 42:
            user = self.login()
            if user:
                break
        while 42:
            while 42:
                action = self.prompt(user)
                if action:
                    break
            if action == '1':
                name, role = self.add_role()
                self.roles[name] = role
            if action == '2':
                self.delete_role()
            if action == '3':
                self.add_user()
            if action == '4':
                self.del_user()
            if action == '5':
                self.add_file()
            if action == '6':
                self.view_file()
            if action == '7':
                self.edit_file()
            if action == '8':
                self.del_file()
            if action == '9':
                return -1

    def prompt(self, user: User):
        print('What would you like to do?')
        print()
        possible_opts = set()
        if user.role.add_role:
            print('Choose 1 to add group')
            possible_opts.add('1')
        if user.role.del_role:
            print('Choose 2 to delete group')
            possible_opts.add('2')
        if user.role.add_user:
            print('Choose 3 to add user')
            possible_opts.add('3')
        if user.role.del_user:
            print('Choose 4 to delete user')
            possible_opts.add('4')
        if user.role.add_f:
            print('Choose 5 to add file')
            possible_opts.add('5')
        if user.role.view_f:
            print('Choose 6 to view file')
            possible_opts.add('6')
        if user.role.edit_f:
            print('Choose 7 to edit file')
            possible_opts.add('7')
        if user.role.del_f:
            print('Choose 8 to delete file')
            possible_opts.add('8')
        print('Choose 9 to change user')
        possible_opts.add('9')
        inp = input()
        if inp in possible_opts:
            return inp
        return None

    def login(self) -> User:
        log = input('login:')
        pas = input('Password:')
        if log in self.users.keys():
            print(self.users)
            user = self.users[log]
            if pas == user.pas:
                return user
        print("Wrong login or password")
        return None

    def add_role(self):
        name = input('role name: ')
        while 42:
            add_role = input('Permission to add roles: ')
            if add_role == 'False':
                add_role = False
                break
            if add_role == 'True':
                add_role = True
                break
            print('The value should be either True or False')
        while 42:
            del_role = input('Permission to delele roles: ')
            if del_role == 'False':
                del_role = False
                break
            if del_role == 'True':
                del_role = True
                break
            print('The value should be either True or False')
        while 42:
            add_user = input('Permission to add users: ')
            if add_user == 'False':
                add_user = False
                break
            if add_user == 'True':
                add_user = True
                break
            print('The value should be either True or False')
        while 42:
            del_user = input('Permission to del users: ')
            if del_user == 'False':
                del_user = False
                break
            if del_user == 'True':
                del_user = True
                break
            print('The value should be either True or False')
        while 42:
            add_f = input('Permission to add files: ')
            if add_f == 'False':
                add_f = False
                break
            if add_f == 'True':
                add_f = True
                break
            print('The value should be either True or False')
        while 42:
            view_f = input('Permission to view files: ')
            if view_f == 'False':
                view_f = False
                break
            if view_f == 'True':
                view_f = True
                break
            print('The value should be either True or False')
        while 42:
            edit_f = input('Permission to edit files: ')
            if edit_f == 'False':
                edit_f = False
                break
            if edit_f == 'True':
                edit_f = True
                break
            print('The value should be either True or False')
        while 42:
            del_f = input('Permission to del files: ')
            if del_f == 'False':
                del_f = False
                break
            if del_f == 'True':
                del_f = True
                break
            print('The value should be either True or False')
            self.roles[name] = Role(name=name, add_role=add_role, del_role=del_role, add_user=add_user,
                                    del_user=del_user, add_f=add_f, view_f=view_f, edit_f=edit_f, del_f=del_f)

    def delete_role(self):
        print('List of roles:')
        for role in self.roles.keys():
            print(role)
        role = input('Choose the role: ')
        if role in self.roles.keys():
            del self.roles[role]
        else:
            print('Wrong role name')

    def add_user(self):
        log = input('login: ')
        pas = input('pas: ')
        role = input('role: ')
        print(self.roles)
        if role in self.roles.keys():
            self.users[log] = User(log, pas, self.roles[role])
        else:
            print('Wrong role')
        
    def del_user(self):
        print('List of users:')
        for user in self.users.keys():
            print(user)
        user = input('Choose the user: ')
        if user in self.users.keys():
            del self.users[user]
        else:
            print('Wrong user name')

    def add_file(self):
        name = input('file name: ')
        self.files[name] = ''

    def view_file(self):
        print('Files:')
        print()
        for f in self.files.keys():
            print(f)
        name = input('file name: ')
        if name in self.files.keys():
            app = QApplication(sys.argv)

            widget = EditFile(False)
            widget.resize(800, 600)
            widget.show()

            print(app.exec_())
            del app
    
    def edit_file(self):
        print('Files:')
        print()
        for f in self.files.keys():
            print(f)
        name = input('file name: ')
        if name in self.files.keys():
            app = QApplication(sys.argv)

            widget = EditFile(True)
            widget.resize(800, 600)
            widget.show()

            print(app.exec_())
            self.files[name] = EditFile.text
            del app

    def del_file(self):
        print('Files:')
        print()
        for f in self.files.keys():
            print(f)
        name = input('file name: ')
        if name in self.files.keys():
            del self.files[name]
        
