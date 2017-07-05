import unittest
from models.urlshandler import UrlsHandler
from models.urlshistoryhandler import UrlsHistoryHandler
from pymongo import MongoClient


class TestUrlsHistoryHandler(unittest.TestCase):

    def setUp(self):
        self.urlsHistoryHandler = UrlsHistoryHandler("mongodb://localhost:27017","testdb")
        self.urlsHistoryHandler.connectToDatabase()

    def tearDown(self):
        client = MongoClient("mongodb://localhost:27017")
        client.drop_database("testdb")


    def testInsertUrlVisit(self):
        result = self.urlsHistoryHandler.insertURLVisit("meow")
        self.assertTrue(result)

        # test with bad values
        result = self.urlsHistoryHandler.insertURLVisit("")
        self.assertFalse(result)

        result = self.urlsHistoryHandler.insertURLVisit(None)
        self.assertFalse(result)

    def testCountUrlVisits(self):
        status,count = self.urlsHistoryHandler.countUrlVisits("woof")
        self.assertTrue(status)
        self.assertEqual(count,0)

        self.urlsHistoryHandler.insertURLVisit("woof")

        status, count = self.urlsHistoryHandler.countUrlVisits("woof")
        self.assertTrue(status)
        self.assertEqual(count, 1)

        # test with bad values
        status, count = self.urlsHistoryHandler.countUrlVisits("")
        self.assertFalse(status)
        self.assertEqual(count, -1)

        status, count = self.urlsHistoryHandler.countUrlVisits(None)
        self.assertFalse(status)
        self.assertEqual(count, -1)

if __name__=="__main__":
    unittest.main()