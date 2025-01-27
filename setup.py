from setuptools import setup, find_packages

setup(
    name='oran-simulator',  # Replace with your project name
    version='0.1.0',  # Replace with your desired version
    packages=find_packages(),
    install_requires=[  # List any external dependencies here
        'numpy',
        'pytest',
        'scipy',
        'pyyaml',
        'sphinx',
        'matplotlib',
        'pandas'
        # ... other dependencies
    ],
)