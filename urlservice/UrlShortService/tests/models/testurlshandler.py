import unittest
from models.urlshandler import UrlsHandler
from models.userhandler import UserHandler
from pymongo import MongoClient

class TestUrlsHandler(unittest.TestCase):
    def setUp(self):
        self.urlHandler = UrlsHandler("mongodb://localhost:27017","testdb")
        self.urlHandler.connectToDatabase()
        self.userHandler = UserHandler("mongodb://localhost:27017","testdb")
        self.userHandler.connectToDatabase()

        self.userHandler.addUser("testUser","testPassword")
        self.userHandler.addUser("testUser1","testPassword")


    def testInsertUrl(self):
        '''
        Test various parameters to the insertURL method
        :return:
        '''

        # Test a good insertion
        status,message = self.urlHandler.insertURL("testUser","http://www.yahoo.com","yahoo")
        self.assertTrue(status)

        # test double insertions of short form
        status, message = self.urlHandler.insertURL("testUser", "http://www.yahoo.com", "yahoo")
        self.assertFalse(status)

        # test inserting with empty strings
        status, message = self.urlHandler.insertURL("testUser", "http://www.yahoo.com", "")
        self.assertFalse(status)

        status, message = self.urlHandler.insertURL("testUser", "", "yahoo")
        self.assertFalse(status)

        # test inserting with None values
        status, message = self.urlHandler.insertURL("testUser", "http://www.yahoo.com", None)
        self.assertFalse(status)

        status, message = self.urlHandler.insertURL("testUser", None, "yahoo")
        self.assertFalse(status)

        # test adding with none existent user
        status, message = self.urlHandler.insertURL("newUser", "http://www.yahoo.com", "yahoo")
        self.assertFalse(status)

    def testRetrieveUrlLongForm(self):

        self.urlHandler.insertURL("testuser","http://www.google.com","google")
        # test good lookup
        status,longForm = self.urlHandler.retrieveURLLongForm("google")
        self.assertTrue(status)

        # Check a none existent lookup
        status, longForm = self.urlHandler.retrieveURLLongForm("yahoo1")
        self.assertFalse(status)

        # test with empty value
        status, longForm = self.urlHandler.retrieveURLLongForm("")
        self.assertFalse(status)

        # test with None value
        status, longForm = self.urlHandler.retrieveURLLongForm(None)
        self.assertFalse(status)


    def testRetrieveAllUrlsForUser(self):
        self.urlHandler.insertURL("testuser","http://www.ynet.co.il","ynet")

        # test retrievimg the URLs for testuser
        status,urls = self.urlHandler.retrieveURLsForUser("testuser")
        self.assertTrue(status)
        self.assertGreater(len(urls),0)

        # test retrieving for none existing user
        status,urls = self.urlHandler.retrieveURLsForUser("testuser2")
        self.assertEqual(len(urls),0)

        # test with bad values
        status,urls = self.urlHandler.retrieveURLsForUser(None)
        self.assertFalse(status)

        status, urls = self.urlHandler.retrieveURLsForUser("")
        self.assertFalse(status)

    def testRetrieveUrlForUser(self):
        self.urlHandler.insertURL("testuser","http://www.meow.com","meow")

        # test normal case
        status, url = self.urlHandler.retrieveURLForUser("testuser","meow")
        self.assertTrue(status)

        # test none existent URL
        status, url = self.urlHandler.retrieveURLForUser("testuser", "cat")
        self.assertFalse(status)

        # test none existent user
        status, url = self.urlHandler.retrieveURLForUser("testuser2", "meow")
        self.assertFalse(status)

        # test existing URL but wrong user
        status, url = self.urlHandler.retrieveURLForUser("testuser1", "meow")
        self.assertFalse(status)

    def tearDown(self):
        client = MongoClient("mongodb://localhost:27017")
        client.drop_database("testdb")




if __name__=="__main__":
    unittest.main()