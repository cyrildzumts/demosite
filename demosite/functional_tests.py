from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()
    

    def tearDown(self):
        self.browser.quit()
    

    def testTitle(self):
        """
        Test if the Title defined and contains
        some defined words
        """
        strlist = ['Acceuille', 'Grand Village']
        self.browser.get('http://localhost:8000')
        for word in strlist:
           self.assertIn(word, self.browser.title)


    def testLogin(self):
        """
        Test if the user is able to log itself in
        """
        self.browser.get('http://localhost:8000')
        loginDialog = self.browser.find_element_by_id('loginBtn2')
        loginDialog.send_keys(Keys.ENTER)

if __name__ == '__main__':
    unittest.main(warnings='ignore')