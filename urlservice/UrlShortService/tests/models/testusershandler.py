import unittest
from pymongo import MongoClient

from models.userhandler import UserHandler

class TestUserHandler(unittest.TestCase):
    def setUp(self):
        self.userHandler = UserHandler("mongodb://localhost:27017","testdb")
        self.userHandler.connectToDatabase()

    def tearDown(self):
        client = MongoClient("mongodb://localhost:27017")
        client.drop_database("testdb")

    def testaddUser(self):

        # test user insertion
        status, message = self.userHandler.addUser("testuser","password")
        self.assertTrue(status)

        # try adding same user again
        status, message = self.userHandler.addUser("testuser", "password")
        self.assertFalse(status)

        # try witn bad values
        status, message = self.userHandler.addUser("", "password")
        self.assertFalse(status)

        status, message = self.userHandler.addUser("testuser", "")
        self.assertFalse(status)

        status, message = self.userHandler.addUser(None, "password")
        self.assertFalse(status)

        status, message = self.userHandler.addUser("testuser",None)
        self.assertFalse(status)

    def testAuthenticateUser(self):
        self.userHandler.addUser("sample","password")

        # test with right password
        status, message = self.userHandler.authenticateUser("sample","password")
        self.assertTrue(status)

        # test with wrong password
        status, message = self.userHandler.authenticateUser("sample", "password1")
        self.assertFalse(status)

        # test with wrong user
        status, message = self.userHandler.authenticateUser("sample1", "password")
        self.assertFalse(status)

        # test with bad values

        status, message = self.userHandler.authenticateUser("", "password")
        self.assertFalse(status)

        status, message = self.userHandler.authenticateUser("sample1", "")
        self.assertFalse(status)

        status, message = self.userHandler.authenticateUser(None, "password")
        self.assertFalse(status)

        status, message = self.userHandler.authenticateUser("sample1", None)
        self.assertFalse(status)



if __name__=="__main__":
    unittest.main()
