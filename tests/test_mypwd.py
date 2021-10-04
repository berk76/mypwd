import mypwd
import unittest
import os


class TestMyPwd(unittest.TestCase):

    def testMyPwd(self):
        mypwd.filename = "mypwd_test.json"
        self.assertEqual("john", mypwd.get_login("postgres"))
        self.assertEqual("myPa$$w0rd", mypwd.get_pwd("postgres"))
        self.assertEqual("Valid until end of month", mypwd.get_value("postgres", "note"))

        login, password = mypwd.get_login_password("postgres")
        self.assertEqual("john", login)
        self.assertEqual("myPa$$w0rd", password)

        login, password, note = mypwd.get_values("postgres", ["login", "password", "note"])
        self.assertEqual("john", login)
        self.assertEqual("myPa$$w0rd", password)
        self.assertEqual("Valid until end of month", note)

        os.remove(mypwd.__get_path__())


if __name__ == "__main__":
    unittest.main()
