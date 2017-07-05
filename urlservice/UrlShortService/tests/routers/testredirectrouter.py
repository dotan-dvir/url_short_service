import unittest
import requests
import json
import time

class TestRedirectRouter(unittest.TestCase):
    '''
            To run the tests in this class you will need to have a running system. The tests assume the system is listening
            on port 8080 on the loopback interface
        '''

    def setUp(self):
        # Add a user
        self.userName = "test1234"+str(int(time.time()))
        self.password = "test"

        self.head = {'username': self.userName, 'password': self.password}
        self.payload = {'longform': 'www.tapuz.co.il', 'shortform': "tapuz"+self.userName}

        response = requests.post("http://localhost:8080/users",
                      data=json.dumps(self.head))
        self.assertEqual(response.status_code,200)

        response = requests.post("http://localhost:8080/urls", data=json.dumps(self.payload), headers=self.head)
        self.assertEqual(response.status_code,200)

    def testRedirect(self):
        # test a redirect from the URL we just created
        response = requests.get("http://localhost:8080/"+self.payload["shortform"],allow_redirects = False)
        self.assertEqual(response.status_code,302)

        # test against a none existent shortcut
        response = requests.get("http://localhost:8080/" + str(time.time()))
        self.assertEqual(response.status_code, 404)

    def tearDown(self):
        pass


if __name__=="__main__":
    unittest.main()