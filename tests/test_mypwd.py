import mypwd
import unittest
import os

class TestMyPwd(unittest.TestCase):

    def testMyPwd(self):
        mypwd.set_filename("mypwd_test.json")
        self.assertEqual("john", mypwd.get_login("mypass"))
        self.assertEqual("myPa$$w0rd", mypwd.get_pwd("mypass"))
        self.assertEqual("Valid until end of month", mypwd.get_value("mypass", "note"))
        os.remove(mypwd.__get_path__()) 

if __name__ == "__main__":
    unittest.main()
