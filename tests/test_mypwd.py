import mypwd
import os
import pytest


PWD_TEMPLATE = {
    "postgres": {
        mypwd.impl.LOGIN_KEY: "john",
        mypwd.impl.PASSWORD_KEY: "myPa$$w0rd",
        "note": "Valid until end of month"
    },
    "mongo": {
        mypwd.impl.LOGIN_KEY: "admin",
        mypwd.impl.PASSWORD_KEY: "myPa$$w0rd2"
    }
}


@pytest.fixture(autouse=True, scope="module")
def setup():
    try:
        mypwd.impl.VAULT_FILENAME = "mypwd_test.json"
        mypwd.impl.PWD_TEMPLATE = PWD_TEMPLATE
        yield mypwd
    finally:
        os.remove(mypwd.impl.get_vault_path())


def test_login():
    assert "john" == mypwd.get_login("postgres")


def test_pwd():
    assert "myPa$$w0rd" == mypwd.get_pwd("postgres")


def test_value():
    assert "Valid until end of month" == mypwd.get_value("postgres", "note")


def test_login_password():
    login, password = mypwd.get_login_password("postgres")
    assert "john" == login
    assert "myPa$$w0rd" == password


def test_login_password_note():
    login, password, note = mypwd.get_values("postgres", ["login", "password", "note"])
    assert "john" == login
    assert "myPa$$w0rd" == password
    assert "Valid until end of month" == note
