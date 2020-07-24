import pytest
import datetime

from .context import Notifications
from .context import Msg

@pytest.fixture
def init():
    return None

def test_one():
    now = datetime.datetime.now()
    event_time = now + datetime.timedelta(hours=23)
    
    msg = Msg(event_time, "hello")
    r = msg.broadcast_or_not(now)

    assert r == "hello"
    

# def test_two():
#     now = datetime.datetime.now()
#     event_time = now + datetime.timedelta(hours=3)
    
#     msg = Msg(event_time, "hello")
#     r = msg.broadcast_or_not(now)
    
#     assert r == None

# def test_three():
#     now = datetime.datetime.now()
#     event_time = now + datetime.timedelta(hours=50)
    
#     msg = Msg(event_time, "hello")
#     r = msg.broadcast_or_not(now)
    
#     assert r == None

# def test_four():
#     now = datetime.datetime.now()
#     event_time = now + datetime.timedelta(hours=3)
    
#     msg = Msg(event_time, "hello")
#     r = msg.broadcast_or_not(now)
    
#     assert r == None

