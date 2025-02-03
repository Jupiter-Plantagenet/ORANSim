.. _xapp_development:

Developing an xApp
==================

This tutorial guides you through the process of developing an xApp for ORANSim.

1. **Create a new Python file (e.g., my_xapp.py) in the oransim/xapp_rapp_framework directory.**

2. **Define a new class that inherits from oransim.xapp_rapp_framework.xapp.XApp:**

    .. code-block:: python

        from oransim.xapp_rapp_framework.xapp import XApp

        class MyXApp(XApp):
            # Add content here

3. **Implement the receive_indication method to handle E2 messages.**

4. **Optionally, implement methods to send control messages or interact with an ML runtime.**

5. **Register your xApp with the Near-RT RIC in your simulation script.**