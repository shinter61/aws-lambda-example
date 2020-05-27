import sys
sys.path.append('./')

import pytest
import json
import handler
from multiprocessing import Manager

@pytest.fixture
def returned_list():
    return Manager().list()

def test_syntax_error(returned_list):
    mail_address = 'aaaaaaa'
    expect_json = json.dumps({
        "statusCode": 500,
        "message": "syntax error",
        "mailAddress": mail_address
    })
    handler.check(mail_address, returned_list)
    assert returned_list[0] == expect_json

def test_none_of_dns(returned_list):
    mail_address = 'aaaaaaa@example.comm'
    expect_json = json.dumps({
        "statusCode": 500,
        "message": "None of DNS query names exist",
        "mailAddress": mail_address
    })
    handler.check(mail_address, returned_list)
    assert returned_list[0] == expect_json

def test_not_exists_address(returned_list):
    mail_address = 'shinter62@gmail.com'
    expect_json = json.dumps({
        "statusCode": 550,
        "message": "Address doesnt exists",
        "mailAddress": mail_address
    })
    handler.check(mail_address, returned_list)
    assert returned_list[0] == expect_json

def test_exists_address(returned_list):
    mail_address = 'shinter61@gmail.com'
    expect_json = json.dumps({
        "statusCode": 250,
        "message": "Address exists",
        "mailAddress": mail_address
    })
    handler.check(mail_address, returned_list)
    assert returned_list[0] == expect_json
