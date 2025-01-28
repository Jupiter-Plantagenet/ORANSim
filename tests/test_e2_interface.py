from oransim.core.interfaces.e2 import E2Termination  

class TestE2Termination:  
    def test_pub_sub(self):  
        e2 = E2Termination()  
        received_messages = []  

        def mock_xapp(msg):  
            received_messages.append(msg)  

        e2.subscribe("xapp1", mock_xapp)  
        e2.publish({"ue_id": 5, "rsrp": -80})  
        assert len(received_messages) == 1  