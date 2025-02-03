from setuptools import setup, find_packages

setup(
    name='oransim',
    version='0.1.0',  # edit with project's version number
    packages=find_packages(),
    install_requires=[
        'simpy>=4.0.1',
        'numpy>=1.21',
        'pyyaml>=6.0',
        'jsonschema>=4.0.0',
        'pydantic>=2.5.0',
        'pytest>=7.0',
        'matplotlib>=3.3.4',
    ],
    extras_require={
        'docs': [
            'sphinx>=5.0.0',
            # 'sphinx_rtd_theme>=1.0.0',  # Uncomment if you use the Read the Docs theme
        ],
        'visualization': [
            'plotly>=5.0.0',
        ],
        'database': [
            'influxdb-client>=1.20.0',  # Add if you implement InfluxDB integration
        ],
        'onnx': [
            'onnx>=1.10.0',
            'onnxruntime>=1.10.0',
        ],
        'tensorflow': [
            'tensorflow>=2.0.0',
        ],
        'pytorch': [
            'torch>=1.10.0',
        ],
        'dev': [
            'pytest>=7.0',  # Add any development-specific dependencies here
        ]
    },
    author='George Chidera Akor',  
    author_email='georgejupiter303@gmail.com, georgeakor@kumoh.ac.kr', 
    description='A 5G ORAN simulation library',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Jupiter-Plantagenet/ORANSim',  
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',  # Will evaluate appropriate license later
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        "Topic :: Scientific/Engineering",
        "Topic :: System :: Networking",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords='5g, oran, simulation, open ran, xapp, rapp, ric, network, wireless, research',
    python_requires='>=3.8',
)