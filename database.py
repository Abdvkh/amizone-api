import os
import json

DATABASE_PATH = os.getenv('JSON_DATABASE_PATH', 'database/')


class JSONDatabase:

    @staticmethod
    def store_user(username, information):
        if not os.path.exists(DATABASE_PATH):
            os.makedirs(DATABASE_PATH)

        file = open(DATABASE_PATH + username + '.json', 'w+')

        json.dump(information, file)

    @staticmethod
    def information_exists(username):
        return os.path.exists(DATABASE_PATH + username + '.json')

    @staticmethod
    def get(username, key):
        file = open(DATABASE_PATH + username + '.json', 'r')
        return json.load(file).get(key)

    @staticmethod
    def set(username, key, value):
        filename = DATABASE_PATH + username + '.json'

        file = open(filename, 'r')

        data = json.load(file)
        data[key] = value
        json.dump(data, open(filename, 'w+'))
