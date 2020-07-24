import pytest

from .context import Notifications
from .context import Msg

@pytest.fixture
def init():
    notifi = Notifications()
    return notifi

def test_one(init):
    assert init.size() == 15

def test_parse_with_valid_cmd(init):
    r = Notifications.parse('/rina notify "hello world" 20 30')
    assert r == 'notify "hello world" 20 30'

def test_parse_with_invalid_cmd_1(init):
    r = Notifications.parse('notify "Hello world" 4/26 15:00')
    assert r == None

def test_parse_with_invalid_cmd_2(init):
    r = Notifications.parse('/test notify "hello world" 20 30')
    assert r == None

def test_parse_with_invalid_cmd_3(init):
    r = Notifications.parse('テストテスト')
    assert r == None

def test_parse_with_invalid_cmd_4(init):
    r = Notifications.parse('/rina help')
    assert r == 'help'

def test_parse_with_notify_cmd(init):
    r = Notifications.parse_notify('notify "Hello world" 4/26 15:00')
    assert r == ('Hello world', '4/26', '15:00')

def test_execute(init):
    r = init.execute("/rina help")
    assert r == "私、天王寺璃奈。どっちでも好きな方つかっていいよ//"

def test_add_and_notify(init):
    r = init.execute('/rina notify "Hello world" 7/25 5:00')
    
