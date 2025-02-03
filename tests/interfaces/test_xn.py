import pytest
from oransim.interfaces.xn import XnInterface
from oransim.simulation.scheduler import ORANScheduler

# Mock nodes for testing
class MockNode:
    def __init__(self, node_id):
        self.node_id = node_id
        self.received_messages = []

    def receive_xn_message(self, message, source_node_id):
        self.received_messages.append((message, source_node_id))

# Mock Scheduler
class MockScheduler:
    def add_event(self, delay, callback, *args):
        callback(*args)

# Test Fixtures
@pytest.fixture
def scheduler():
    return MockScheduler()

@pytest.fixture
def xn_interface(scheduler):
    return XnInterface(scheduler)

@pytest.fixture
def node_a():
    return MockNode("node_a")

@pytest.fixture
def node_b():
    return MockNode("node_b")

# Test Cases
def test_xn_interface_initialization(xn_interface, scheduler):
    assert xn_interface.scheduler == scheduler
    assert xn_interface.nodes == {}

def test_xn_interface_register_node(xn_interface, node_a):
    xn_interface.register_node("node_a", node_a)
    assert "node_a" in xn_interface.nodes
    assert xn_interface.nodes["node_a"] == node_a

def test_xn_interface_register_node_already_registered(xn_interface, node_a, caplog):
    xn_interface.register_node("node_a", node_a)
    xn_interface.register_node("node_a", node_a)
    assert "already registered" in caplog.text

def test_xn_interface_unregister_node(xn_interface, node_a):
    xn_interface.register_node("node_a", node_a)
    xn_interface.unregister_node("node_a")
    assert "node_a" not in xn_interface.nodes

def test_xn_interface_unregister_node_not_found(xn_interface, caplog):
    xn_interface.unregister_node("node_a")
    assert "not found" in caplog.text

def test_xn_interface_send_message(xn_interface, node_a, node_b):
    xn_interface.register_node("node_a", node_a)
    xn_interface.register_node("node_b", node_b)
    message = {"key": "value"}
    xn_interface.send_message(message, "node_a", "node_b")
    assert len(node_b.received_messages) == 1
    assert node_b.received_messages[0] == (message, "node_a")

def test_xn_interface_send_message_source_not_registered(xn_interface, node_b):
    xn_interface.register_node("node_b", node_b)
    message = {"key": "value"}
    with pytest.raises(ValueError):
        xn_interface.send_message(message, "node_a", "node_b")

def test_xn_interface_send_message_destination_not_registered(xn_interface, node_a):
    xn_interface.register_node("node_a", node_a)
    message = {"key": "value"}
    with pytest.raises(ValueError):
        xn_interface.send_message(message, "node_a", "node_b")