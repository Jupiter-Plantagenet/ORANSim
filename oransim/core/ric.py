from typing import Dict  
from oransim.data_models.policies import A1Policy  

class NearRTRIC:  
    def __init__(self):  
        self.xapps: Dict[str, callable] = {}          # xApp ID → function  
        self.active_policies: Dict[int, A1Policy] = {}  

    def add_xapp(self, xapp_id: str, xapp_func: callable = None):  
        self.xapps[xapp_id] = xapp_func  

    def enforce_policy(self, policy: A1Policy):  
        self.active_policies[policy.policy_id] = policy  

class NonRTRIC:  
    def __init__(self):  
        self.rapps: Dict[str, callable] = {}          # rApp ID → function  

    def publish_policy(self, near_rt_ric: NearRTRIC, policy: A1Policy):  
        near_rt_ric.enforce_policy(policy)  