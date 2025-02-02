"""
The `tests/interfaces` subpackage contains unit tests and integration tests for 
the interface implementations in the ORANSim library.

These interfaces include:

- A1 interface (between Non-RT RIC and Near-RT RIC)
- E2 interface (between Near-RT RIC and O-DUs/O-CUs)
- O1 interface (for management and configuration)
- F1 interface (between O-CU and O-DU)
- Xn interface (between peer gNBs)
- X2 interface (between peer eNBs)
- Open Fronthaul interface (between O-RU and O-DU)

The tests in this subpackage verify the correct behavior of the interface 
implementations, including message passing, policy handling, configuration 
management, and other interactions.
"""

# This __init__.py file can be kept empty. 
# Its main purpose is to mark the 'tests/interfaces' directory as a Python package.