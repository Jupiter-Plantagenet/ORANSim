import pytest  
from oransim.core.ric import NearRTRIC, NonRTRIC  
from oransim.data_models.policies import A1Policy  

class TestNearRTRIC:  
    def test_add_xapp(self):  
        ric = NearRTRIC()  
        ric.add_xapp("cell_switch")  
        assert "cell_switch" in ric.xapps  

    def test_enforce_a1_policy(self):  
        ric = NearRTRIC()  
        policy = A1Policy(policy_id=1, policy="prioritize_ue_category_5")  
        ric.enforce_policy(policy)  
        assert ric.active_policies[1] == policy  

class TestNonRTRIC:  
    def test_publish_policy_to_near_rt(self):  
        non_rt_ric = NonRTRIC()  
        near_rt_ric = NearRTRIC()  
        policy = A1Policy(policy_id=1, policy="enable_energy_saver_mode")  
        
        non_rt_ric.publish_policy(near_rt_ric, policy)  
        assert 1 in near_rt_ric.active_policies  