import unittest
import requests
import json
import time

class TestUserRouter(unittest.TestCase):
    '''
    To run the tests in this class you will need to have a running system. The tests assume the system is listening
    on port 8080 on the loopback interface
    '''
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testAddUser(self):

        userName = "test"+str(time.time())

        # test add user
        response = requests.post("http://localhost:8080/users",data=json.dumps({'username': userName,'password':'test'}))
        self.assertEqual(response.status_code, 200)

        # test add user a second time
        response = requests.post("http://localhost:8080/users",data=json.dumps({'username': userName, 'password': 'test'}))
        self.assertEqual(response.status_code, 400)

        response = requests.post("http://localhost:8080/users",
                                 data=json.dumps({'username': '', 'password': 'test'}))
        self.assertEqual(response.status_code, 400)

        response = requests.post("http://localhost:8080/users",
                                 data=json.dumps({'username': 'test', 'password': ''}))
        self.assertEqual(response.status_code, 400)

        response = requests.post("http://localhost:8080/users",
                                 data=json.dumps({'username': None, 'password': 'test'}))
        self.assertEqual(response.status_code, 400)

        response = requests.post("http://localhost:8080/users",
                                 data=json.dumps({'username': 'test', 'password': None}))
        self.assertEqual(response.status_code, 400)

if __name__=="__main__":
    unittest.main()