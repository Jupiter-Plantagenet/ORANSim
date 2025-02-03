import pytest
from oransim.interfaces.e2 import E2Interface
from oransim.simulation.scheduler import ORANScheduler
from queue import Queue

# Mock NearRTRIC and Scheduler for testing
class MockNearRTRIC:
    def __init__(self):
        self.received_messages = []

    def receive_e2_message(self, message, node_id):
        self.received_messages.append((message, node_id))

class MockScheduler:
    def add_event(self, delay, callback, *args):
        callback(*args)  # Execute immediately for testing

# Test Data and Fixtures
@pytest.fixture
def scheduler():
    return MockScheduler()

@pytest.fixture
def near_rt_ric():
    return MockNearRTRIC()

@pytest.fixture
def e2_interface(near_rt_ric, scheduler):
    return E2Interface(near_rt_ric, scheduler)

@pytest.fixture
def sample_message():
    return {"message_type": "TEST", "content": "Test message content"}

# Test Cases
def test_e2_interface_initialization(e2_interface, near_rt_ric, scheduler):
    assert e2_interface.near_rt_ric == near_rt_ric
    assert e2_interface.scheduler == scheduler
    assert isinstance(e2_interface.message_queue, Queue)
    assert e2_interface.e2_subscribers == {}

def test_e2_interface_send_message(e2_interface, near_rt_ric, sample_message):
    e2_interface.send_message(sample_message, "du_1")
    assert near_rt_ric.received_messages[0] == (sample_message, "du_1")

def test_e2_interface_subscribe_unsubscribe(e2_interface):
    def test_callback(message, node_id):
        pass

    e2_interface.subscribe("xapp_1", test_callback)
    assert "xapp_1" in e2_interface.e2_subscribers

    e2_interface.unsubscribe("xapp_1")
    assert "xapp_1" not in e2_interface.e2_subscribers

def test_e2_interface_send_indication(e2_interface, sample_message):
    received_messages = []

    def test_callback(message, du_id):
        received_messages.append((message, du_id))

    e2_interface.subscribe("xapp_1", test_callback)
    e2_interface.send_indication(sample_message, "du_1")
    assert len(received_messages) == 1
    assert received_messages[0] == (sample_message, "du_1")

def test_e2_interface_subscribe_invalid_input(e2_interface):
    with pytest.raises(TypeError):
        e2_interface.subscribe(123, lambda x, y: None)  # Invalid subscriber_id type
    with pytest.raises(TypeError):
        e2_interface.subscribe("xapp_1", "not_a_function")  # Invalid callback type
    
def test_e2_interface_unsubscribe_nonexistent_subscriber(e2_interface, caplog):
    e2_interface.unsubscribe("nonexistent_xapp")
    assert "Attempted to unsubscribe unknown xApp" in caplog.text

def test_e2_interface_send_message_invalid_node(e2_interface, sample_message):
    with pytest.raises(ValueError):
        e2_interface.send_message(sample_message, "invalid_source", "du_1")
    with pytest.raises(ValueError):
        e2_interface.send_message(sample_message, "o_du", "invalid_dest")