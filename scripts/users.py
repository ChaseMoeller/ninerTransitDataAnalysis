users_array = []

class user():
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

#add root user
users_array.append(user("root", "root"))

def add_user(f_name, l_name):
    users_array.append(user(str(f_name), str(l_name)))

def print_users():
    for i in range(0, len(users_array)):
        print(users_array[i].first_name + " " + users_array[i].last_name)

def validate_user(f_name, l_name):
    for i in range(0, len(users_array)):
        if users_array[i].first_name == str(f_name):
            return True
    return False



