import mypwd
import os
import pytest


@pytest.fixture(autouse=True, scope="module")
def setup():
    try:
        mypwd.impl.FILENAME = "mypwd_test.json"
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
