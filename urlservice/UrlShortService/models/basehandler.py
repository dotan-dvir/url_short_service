from pymongo import MongoClient

class BaseHandler(object):
    def __init__(self,dbURL,dbName,collectionName):
        self.dbURL = dbURL
        self.dbName = dbName
        self.dbClient = None
        self.collectionName = collectionName
        self.dbConnection = None
        self.dbCollection = None

    def connectToDatabase(self):
        '''
        Initialize the database connection
        :return: void
        '''

        if(self.isConnected()):
            return
        try:
            self.dbClient = MongoClient(self.dbURL)
            self.dbConnection = self.dbClient[self.dbName]
            self.dbCollection = self.dbConnection[self.collectionName]
        except:
            self.dbClient = None
            self.dbConnnection = None
            self.dbCollection = None


    def isConnected(self):
        '''

        :return: True if connected to database and False otherwise
        '''
        return self.dbCollection != None and self.dbCollection != None
