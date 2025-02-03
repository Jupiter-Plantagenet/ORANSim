.. _rapp_development:

Developing an rApp
==================

This tutorial guides you through the process of developing an rApp for ORANSim.

1. **Create a new Python file (e.g., my_rapp.py) in the oransim/xapp_rapp_framework directory.**

2. **Define a new class that inherits from oransim.xapp_rapp_framework.rapp.RApp:**

    .. code-block:: python

        from oransim.xapp_rapp_framework.rapp import RApp

        class MyRApp(RApp):
            # Add content here

3. **Implement methods to create, send, update, and delete A1 policies.**

4. **Optionally, implement methods to interact with an ML runtime.**

5. **Register your rApp with the Non-RT RIC in your simulation script.**