import pytest

@pytest.fixture
def tester():
    username = "asd"
    password = "asd"
    return (username, password)


def test1(tester):
    username1 = "asd"
    assert tester[0] == username1


def test_2(tester):
    password_check = "asd"
    assert tester[1] == password_check