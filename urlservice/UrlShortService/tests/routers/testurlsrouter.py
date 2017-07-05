import unittest
import requests
import json
import time

class TestUrlsRouter(unittest.TestCase):
    '''
        To run the tests in this class you will need to have a running system. The tests assume the system is listening
        on port 8080 on the loopback interface
    '''

    def setUp(self):
        # Add a user
        self.userName = "test" + str(time.time())
        self.password = "test"

        requests.post("http://localhost:8080/users", data=json.dumps({'username': self.userName, 'password': self.password}))

    def tearDown(self):
        pass

    def testAddUrl(self):
        head = {'username':self.userName,'password':self.password}
        payload = {'longform':'www.tapuz.co.il','shortform':'tapuz'+self.userName}

        # Test adding a URL
        response = requests.post("http://localhost:8080/urls",data=json.dumps(payload),headers=head)
        self.assertEqual(response.status_code,200)

        # Test adding a URL a second time
        response = requests.post("http://localhost:8080/urls", data=json.dumps(payload), headers=head)
        self.assertEqual(response.status_code, 400)

        # Test adding a URL
        payload = {'longform': self.userName+'.tapuz.co.il'}
        response = requests.post("http://localhost:8080/urls", data=json.dumps(payload), headers=head)
        self.assertEqual(response.status_code, 200)

    def testListUrlsForUser(self):
        head = {'username': self.userName, 'password': self.password}

        # test getting URLs for test user
        response = requests.get("http://localhost:8080/urls",headers=head)
        self.assertEqual(response.status_code,200)

        # test retrieving URLs for a none existing user name
        head = {'username': "me", 'password': self.password}
        response = requests.get("http://localhost:8080/urls", headers=head)
        self.assertEqual(response.status_code, 403)

    def testGetUrlInfo(self):
        head = {'username': self.userName, 'password': self.password}
        payload = {'longform': 'www.tapuz.co.il', 'shortform': 'orange' + self.userName}

        # Add a URL for testing
        response = requests.post("http://localhost:8080/urls", data=json.dumps(payload), headers=head)
        self.assertEqual(response.status_code, 200)

        # test getting the info
        response = requests.get("http://localhost:8080/urls/"+"orange" + self.userName,headers=head)
        self.assertEqual(response.status_code, 200)

        # Test none existing URL
        response = requests.get("http://localhost:8080/urls/"+"dog" + self.userName,headers=head)
        self.assertEqual(response.status_code, 404)


if __name__=="__main__":
    unittest.main()