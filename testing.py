import pytest
@pytest.mark.parametrize("username , password",[("kill" , "kill"),("asd" , "asd")])
def test_method(username , password):
    assert username  == password