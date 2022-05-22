import mypwd
import os
import pytest
from pytest import MonkeyPatch


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

VAULT_FILENAME = "mypwd_test.json"


@pytest.fixture(autouse=True, scope="module")
def setup():
    try:
        mypwd.impl.VAULT_FILENAME = VAULT_FILENAME
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


def test_new_entry(monkeypatch: MonkeyPatch):
    ENTRY = "New Entry"
    LOGIN = "mylogin"
    PASSWORD = "mypass"
    SERVER = "myserver"
    inputs = ["y", LOGIN, PASSWORD, SERVER]

    monkeypatch.setattr("builtins.input", lambda _: inputs.pop(0))

    # Enter new values
    login, password, server = mypwd.get_values(ENTRY, ["login", "password", "server"])
    assert LOGIN == login
    assert PASSWORD == password
    assert SERVER == server

    # Entry already exists
    login, password, server = mypwd.get_values(ENTRY, ["login", "password", "server"])
    assert LOGIN == login
    assert PASSWORD == password
    assert SERVER == server
