from pymongo import MongoClient

from util.stringutil import validateString
from .basehandler import BaseHandler

class UserHandler(BaseHandler):

    def __init__(self,dbURL,dbName):
        '''
        Initialize the user handler object with a reference to the DB URL and the DB name
        :param dbURL: the URL to the momgo db deployment
        :param dbName: the name of the database to use
        '''
        super().__init__(dbURL,dbName,"users")

    def addUser(self,userName,password):
        '''
        Add a user to the database
        :param userName: the name of the new user
        :param password: the password for the new user
        :return: A tuple of boolean,string indicating success and a message to the user
        '''
        if(validateString(userName) == False or validateString(password)==False):
            return False,"Cannot insert a user with empty username or password"

        if(super().isConnected() == False):
            return False,"Internal server error"

        try:
            if(self.dbCollection.find_one({"username":userName})!= None):
                return False,"User already exists"
        except:
                return False,"Internal server error"

        objectId = None

        try:
            objectId = self.dbCollection.insert_one({"username":userName,"password": password})

        except:
            objectId = None

        if(objectId == None):
            return False,"Internal server error"

        return True,"User created succesfully"

    def authenticateUser(self,userName,password):
        '''
        Authenticate the user given the user/password combination
        :param userName:  the user name for the user
        :param password: the password
        :return: a tuple containing a boolean indicating auccess or error and a message to the user
        '''

        if(validateString(userName)== False or validateString(password)==False):
            return False, "Cannot authenticate a user with empty user name or password"

        if (super().isConnected() == False):
            return False,"Internal server errror"


        user = None
        try:
            user = self.dbCollection.find_one({"username": userName})
        except:
            user = None
            return False,"Internal server error"

        if(user == None):
            return False,"User does not exist"

        if(user["password"] == password):
            return True,"User authenticated successfully"

        return False,"Wrong username or password"


if __name__ == "__main__":
    pass



