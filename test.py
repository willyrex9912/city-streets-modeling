import pickle
from typing import List


class Person:
    def __init__(self, name: str):
        self.name = name


class User:
    def __init__(self, username:str, password: str):
        self.person = Person(username)
        self.password = password


class GlobalData:
    def __init__(self):
        self.user = User("jessiel", "asdf@1234")


# object1 = Object('object1')
# object2 = Object('object2')
# object3 = Object('object4')
#
# objects = [object1, object2, object3]
#
# with open('data/project/objects.csm', 'wb') as file:
#     pickle.dump(GlobalData(), file)

with open('data/project/objects.csm', 'rb') as file:
    data: GlobalData = pickle.load(file)
    print(data.user.person.name)

