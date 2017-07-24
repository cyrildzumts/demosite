from selenium import webdriver
import unittest

class NewVisitor(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()
    
    def tearDown(self):
        self.browser.quit()
    
    def testTitle(self):
        strlist = ['Acceuille', 'Grand Village']
        self.browser.get('http://localhost:8000')
        for word in strlist:
           self.assertIn(word, self.browser.title)

if __name__ == '__main__':
    unittest.main(warnings='ignore')