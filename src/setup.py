from setuptools import find_packages, setup


setup(
    name="viera2mqtt",
    version="0.2.0",
    packages=find_packages(),
    install_requires=[
        "click>=8.0",
        "panasonic_viera",
        'aiohttp',
        'paho-mqtt',
        'requests',
        "python-consul"
    ],
    extras_require={"test": ["pytest", "pytest-mock"]},
    author="Ernest Czerwonka",
    author_email="ernest@czerwe.net",
    description="Specific commands to Viera TV",
    entry_points={
        'console_scripts': [
            'viera2mqtt = viera2mqtt.entrypoints:cli'
        ]
    }
)
