"""Setup script for the SignalHouse Python SDK."""

from setuptools import setup, find_packages

setup(
    name="signalhouse",
    version="1.0.2",
    description="Python SDK for the SignalHouse API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="SignalHouse LLC",
    author_email="support@signalhouse.io",
    url="https://github.com/bonzo-signalhouse/SignalHouseSDK-PY",
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[
        "requests>=2.28.0",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Communications :: Telephony",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="signalhouse sms mms 10dlc messaging telecom api sdk",
)
