from setuptools import setup


setup(
    name="vnpy_akshare",
    version="1.0.0",
    description="AkShare datafeed adapter for VeighNa quant trading framework",
    author="VeighNa Community",
    author_email="veighna@foxmail.com",
    license="MIT",
    url="https://github.com/vnpy/vnpy_akshare",
    packages=["vnpy_akshare"],
    keywords=[
        "quant",
        "quantitative",
        "investment",
        "trading",
        "algotrading",
        "datafeed",
        "akshare",
    ],
    python_requires=">=3.8",
    install_requires=[
        "vnpy>=3.0.0",
        "akshare>=1.12.0",
        "pandas>=1.5.0",
        "importlib-metadata",
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Office/Business :: Financial :: Investment",
    ],
)
