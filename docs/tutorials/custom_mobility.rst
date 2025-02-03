.. _custom_mobility:

Implementing a Custom Mobility Model
====================================

This tutorial explains how to implement a custom mobility model in ORANSim.

1. **Create a new Python file (e.g., custom_mobility.py) in the oransim/core/mobility directory.**

2. **Define a new class that inherits from oransim.core.mobility.MobilityModel:**

    .. code-block:: python

        from oransim.core.mobility import MobilityModel

        class CustomMobilityModel(MobilityModel):
            # Add content here

3. **Implement the update_position method.**

4. **Use your custom mobility model in a simulation.**