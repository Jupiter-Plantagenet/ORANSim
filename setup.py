from setuptools import setup, find_packages

setup(
    name="oransim",  # Must match your package directory name
    version="0.1.0",
    packages=find_packages(include=["oransim", "oransim.*"]),  # Explicitly include submodules
    install_requires=[
        "simpy>=4.0",
        "pydantic>=2.0",
        "numpy>=1.21",
        "gymnasium>=0.28",
    ],
    author="Jupiter Plantagenet",
    author_email="georgejupiter303@gmail.com",
    description="A 5G ORAN simulation library for AI-driven RAN testing",
    url="https://github.com/Jupiter-Plantagenet/ORANSim",
    python_requires=">=3.8",
)